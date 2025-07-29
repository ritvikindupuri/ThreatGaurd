from models import AllowedEmailEndings, BlockList

from abilities import flask_app_authenticator
from models import AllowList
from flask import Flask, request, url_for, session, abort
from routes import register_routes
import os
from abilities import apply_sqlite_migrations


# The app initialization must be done in this module to avoid circular dependency problems.

def create_initialized_flask_app():
    # DO NOT INSTANTIATE THE FLASK APP IN ANOTHER MODULE.
    app = Flask(__name__, static_folder='static')

    # Set a secret key for session management
    app.secret_key = os.urandom(24)

    # Initialize database
    from models import db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
    db.init_app(app)
    # DO NOT INITIALIZE db IN ANOTHER MODULE.

    # Initialize migrations
    # Just write SQL queries for example to add a column to an existing table if missing

    register_routes(app)

    # Add before_request handler for authentication
    # Set up authentication
    @app.before_request
    def consolidated_auth_check():
        if request.endpoint == 'static' or request.endpoint == 'logout':
            return None
        
        # Flask-App-Authenticator check
        auth_result = flask_app_authenticator(
            allowed_domains=None,
            allowed_users=None,
            logo_path=url_for('static', filename='company_logo.png', _external=True),
            app_title="ThreatGuard: Security Intelligence Platform",
            custom_styles={
                "global": "font-family: 'Inter', sans-serif; background-color: #0a192f;",
                "card": "border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); background-color: #112240;",
                "logo": "max-width: 180px; height: auto; border-radius: 8px;",
                "title": "font-size: 1.5rem; font-weight: 700; color: #64ffda; text-transform: uppercase;",
                "input": "border-radius: 6px; border: 1px solid #233554; padding: 0.5rem 1rem; background-color: #112240; color: #64ffda;",
                "button": "background-color: #64ffda; color: #0a192f; border-radius: 6px; padding: 0.75rem 1.25rem; font-weight: 600; transition: all 0.3s ease;",
                "google_button": "border: 1px solid #233554; border-radius: 6px; padding: 0.75rem 1.25rem; transition: all 0.3s ease; color: #64ffda; background-color: transparent;"
            },
            session_expiry=None
        )()
        
        if auth_result is not None:
            return auth_result
        
        # Check allowed list
        if 'user' in session and 'email' in session['user']:
            user_email = session['user']['email']
            allowed_list = AllowList.query.all()
            block_list = BlockList.query.all()
            allowed_endings = AllowedEmailEndings.query.all()
            email_ending = user_email.split('@')[-1]
            
            if BlockList and user_email in [item.email for item in block_list]:
                abort(401)
                
            if (allowed_list and user_email in [item.email for item in allowed_list]):
                return None
            elif not allowed_list and not allowed_endings:
                new_allowed = AllowList(email=user_email)
                db.session.add(new_allowed)
                db.session.commit()
                return None
            elif (allowed_list and user_email not in [item.email for item in allowed_list]) and not allowed_endings:
                abort(401)
            elif (allowed_endings and email_ending not in [item.email_ending for item in allowed_endings]):
                abort(401)
            elif (allowed_endings and email_ending in [item.email_ending for item in allowed_endings]):
                new_allowed = AllowList(email=user_email, from_allowed_ending=True)
                db.session.add(new_allowed)
                db.session.commit()
                return None
        
        abort(401)

    # Apply database migrations
    with app.app_context():
        apply_sqlite_migrations(db.engine, db.Model, 'migrations')


    return app