function showModal(message, callback) {
    const modal = document.getElementById('custom-modal');
    const modalMessage = document.getElementById('custom-modal-message');
    modalMessage.textContent = message;
    modal.style.display = 'block';
    modal.callback = callback;
}

function closeModal() {
    const modal = document.getElementById('custom-modal');
    modal.style.display = 'none';
    if (modal.callback) {
        modal.callback();
        modal.callback = null;
    }
}

function showConfirmationModal(message, onConfirm, onCancel) {
    const modal = document.getElementById('confirmation-modal');
    const modalMessage = document.getElementById('confirmation-modal-message');
    const confirmButton = document.getElementById('confirmation-modal-confirm');
    const cancelButton = document.getElementById('confirmation-modal-cancel');

    modalMessage.textContent = message;
    modal.style.display = 'block';

    confirmButton.onclick = () => {
        modal.style.display = 'none';
        onConfirm();
    };

    cancelButton.onclick = () => {
        modal.style.display = 'none';
        if (onCancel) onCancel();
    };
}

// Expose the showModal and showConfirmationModal functions globally
window.showModal = showModal;
window.showConfirmationModal = showConfirmationModal;