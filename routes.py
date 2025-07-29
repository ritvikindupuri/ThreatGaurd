from models import BlockList, Threat
from models import AllowedEmailEndings
from models import AllowList, db
from flask import render_template, jsonify, url_for, request, redirect, session
from flask import current_app as app
import logging
from datetime import datetime

def register_routes(app):
    @app.route("/")
    def home_route():
        # Get all threats for the dashboard
        recent_threats = Threat.query.order_by(Threat.created_at.desc()).all()
        return render_template("home.html", title="Home", recent_threats=recent_threats)

    @app.route("/submit-threat")
    def submit_threat_route():
        return render_template("submit_threat.html", title="Submit Threat")

    @app.route("/threat-location/<int:threat_id>")
    def threat_location_route(threat_id):
        threat = Threat.query.get_or_404(threat_id)
        return render_template("threat_location.html", title="Threat Location", threat=threat)

    @app.route("/api/threats/create", methods=["POST"])
    def create_threat():
        try:
            data = request.json
            if not all(key in data for key in ['ip_address', 'timestamp', 'threat_type']):
                return jsonify({"status": "error", "message": "Missing required fields"}), 400

            # Fetch geolocation data
            import requests
            try:
                geo_response = requests.get(f'https://ipapi.co/{data["ip_address"]}/json/').json()
            except Exception as geo_error:
                logging.warning(f"Geolocation lookup failed for IP {data['ip_address']}: {geo_error}")
                geo_response = {}
                # Add more detailed logging for troubleshooting
                if 'error' in geo_response:
                    logging.warning(f"Geolocation API error: {geo_response.get('reason', 'Unknown error')}")

            # Create new threat
            new_threat = Threat(
                ip_address=data['ip_address'],
                timestamp=datetime.fromisoformat(data['timestamp']),
                threat_type=data['threat_type'],
                description=data.get('description', ''),
                analyst_email=session['user']['email'],
                country=geo_response.get('country_name'),
                city=geo_response.get('city'),
                latitude=geo_response.get('latitude'),
                longitude=geo_response.get('longitude'),
                region=geo_response.get('region')
            )

            db.session.add(new_threat)
            db.session.commit()

            return jsonify({"status": "success", "message": "Threat submitted successfully", "threat_id": new_threat.id})
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating threat: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/company-admins")
    def company_admins_route():
        allowed_emails = AllowList.query.all()
        allowed_endings = AllowedEmailEndings.query.all()
        blocked_emails = BlockList.query.all()
        
        for email in allowed_emails:
            email.is_blocked = any(blocked.email == email.email for blocked in blocked_emails)
            email.role = "Owner" if email.id == 1 else email.role
        
        return render_template("company_admins.html", title="Company Admins", allowed_emails=allowed_emails, allowed_endings=allowed_endings)

    @app.route("/api/delete_admin/<int:admin_id>", methods=["DELETE"])
    def delete_admin(admin_id):
        try:
            if admin_id == 1:
                return jsonify({"status": "error", "message": "You are not allowed to delete the super admin."}), 403
            admin = AllowList.query.get(admin_id)
            if admin:
                if admin.email == session['user']['email']:
                    return jsonify({"status": "error", "message": "You are not allowed to delete yourself as an admin."}), 403
                db.session.delete(admin)
                db.session.commit()
                return jsonify({"status": "success", "message": "Admin deleted successfully"})
            else:
                return jsonify({"status": "error", "message": "Admin not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route("/api/company_admins/create", methods=["POST"])
    def api_create_company_admin():
        email = request.json.get('email')
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        
        try:
            new_email = AllowList(email=email)
            db.session.add(new_email)
            db.session.commit()
            return jsonify({"status": "success", "message": "Email added to allow list successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route("/api/allowed_email_endings/create", methods=["POST"])
    def api_create_allowed_email_ending():
        email_ending = request.json.get('email_ending')
        if not email_ending:
            return jsonify({"status": "error", "message": "Email ending is required"}), 400
        # Remove '@' if it's included in the email ending
        email_ending = email_ending.lstrip('@')
        
        try:
            new_ending = AllowedEmailEndings(email_ending=email_ending)
            db.session.add(new_ending)
            db.session.commit()
            return jsonify({"status": "success", "message": "Email ending added successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
            

    @app.route("/api/delete_email_ending/<int:ending_id>", methods=["DELETE"])
    def delete_email_ending(ending_id):
        try:
            ending = AllowedEmailEndings.query.get(ending_id)
            if ending:
                db.session.delete(ending)
                db.session.commit()
                return jsonify({"status": "success", "message": "Email ending deleted successfully"})
            else:
                return jsonify({"status": "error", "message": "Email ending not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
        
    @app.route("/api/block_admin/<int:admin_id>", methods=["POST"])
    def block_admin(admin_id):
        try:
            admin = AllowList.query.get(admin_id)
            if admin:
                if admin.email == session['user']['email']:
                    return jsonify({"status": "error", "message": "You cannot block yourself"}), 403
                blocked = BlockList(email=admin.email)
                db.session.add(blocked)
                db.session.commit()
                return jsonify({"status": "success", "message": "Admin blocked successfully"})
            else:
                return jsonify({"status": "error", "message": "Admin not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route("/api/unblock_admin/<int:admin_id>", methods=["POST"])
    def unblock_admin(admin_id):
        try:
            admin = AllowList.query.get(admin_id)
            if admin:
                blocked = BlockList.query.filter_by(email=admin.email).first()
                if blocked:
                    db.session.delete(blocked)
                    db.session.commit()
                    return jsonify({"status": "success", "message": "Admin unblocked successfully"})
                else:
                    return jsonify({"status": "error", "message": "Admin was not blocked"}), 400
            else:
                return jsonify({"status": "error", "message": "Admin not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
            
    @app.route("/api/threat_location/<int:threat_id>")
    def get_threat_location(threat_id):
        try:
            threat = Threat.query.get(threat_id)
            if threat:
                if threat.latitude and threat.longitude:
                    return redirect(url_for('threat_location_route', threat_id=threat_id))
                return jsonify({
                    "status": "success",
                    "country": threat.country,
                    "city": threat.city,
                    "region": threat.region,
                    "latitude": threat.latitude,
                    "longitude": threat.longitude
                })
            return jsonify({"status": "error", "message": "Threat not found"}), 404
        except Exception as e:
            logging.error(f"Error retrieving threat location: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
            
    @app.route("/api/delete_threat/<int:threat_id>", methods=["DELETE"])
    def delete_threat(threat_id):
        try:
            threat = Threat.query.get(threat_id)
            if threat:
                db.session.delete(threat)
                db.session.commit()
                return jsonify({"status": "success", "message": "Threat deleted successfully"})
            else:
                return jsonify({"status": "error", "message": "Threat not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for('home_route'))

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('unauthorized.html'), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
        return render_template('500.html'), 500