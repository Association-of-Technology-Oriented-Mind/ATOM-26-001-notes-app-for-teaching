/**
 * Vanilla JavaScript for Notes Application Client Interactions
 * Handles form validation, character counters, toggleable form, and delete confirmation.
 */

document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. New Note Form Toggle
    // ==========================================
    const toggleFormBtn = document.getElementById('toggle-note-form-btn');
    const newNoteCard = document.getElementById('new-note-card');
    const cancelFormBtn = document.getElementById('cancel-note-btn');

    if (toggleFormBtn && newNoteCard) {
        toggleFormBtn.addEventListener('click', () => {
            const isHidden = newNoteCard.style.display === 'none' || getComputedStyle(newNoteCard).display === 'none';
            if (isHidden) {
                newNoteCard.style.display = 'block';
                newNoteCard.classList.add('active');
                const titleInput = document.getElementById('note-title-input');
                if (titleInput) titleInput.focus();
            } else {
                newNoteCard.style.display = 'none';
                newNoteCard.classList.remove('active');
            }
        });
    }

    if (cancelFormBtn && newNoteCard) {
        cancelFormBtn.addEventListener('click', () => {
            newNoteCard.style.display = 'none';
            newNoteCard.classList.remove('active');
        });
    }

    // ==========================================
    // 2. Character Counter & Form Validation
    // ==========================================
    function setupInputValidation(titleInputId, contentInputId, titleCountId, contentCountId, formId) {
        const titleInput = document.getElementById(titleInputId);
        const contentInput = document.getElementById(contentInputId);
        const titleCounter = document.getElementById(titleCountId);
        const contentCounter = document.getElementById(contentCountId);
        const form = document.getElementById(formId);

        const MAX_TITLE_LEN = 100;

        if (titleInput && titleCounter) {
            titleInput.addEventListener('input', () => {
                const currentLen = titleInput.value.length;
                titleCounter.textContent = `${currentLen} / ${MAX_TITLE_LEN}`;
                if (currentLen >= MAX_TITLE_LEN) {
                    titleCounter.classList.add('limit-reached');
                } else {
                    titleCounter.classList.remove('limit-reached');
                }
            });
        }

        if (contentInput && contentCounter) {
            contentInput.addEventListener('input', () => {
                const currentLen = contentInput.value.length;
                contentCounter.textContent = `${currentLen} chars`;
            });
        }

        if (form) {
            form.addEventListener('submit', (e) => {
                const titleVal = titleInput ? titleInput.value.trim() : '';
                const contentVal = contentInput ? contentInput.value.trim() : '';

                if (!titleVal) {
                    e.preventDefault();
                    alert('Note title cannot be empty!');
                    if (titleInput) titleInput.focus();
                    return;
                }

                if (!contentVal) {
                    e.preventDefault();
                    alert('Note content cannot be empty!');
                    if (contentInput) contentInput.focus();
                    return;
                }
            });
        }
    }

    // Initialize validation for New Note form & Edit Note form
    setupInputValidation('note-title-input', 'note-content-input', 'title-char-count', 'content-char-count', 'add-note-form');
    setupInputValidation('edit-title-input', 'edit-content-input', 'edit-title-count', 'edit-content-count', 'edit-note-form');

    // ==========================================
    // 3. Delete Confirmation Modal
    // ==========================================
    const deleteModal = document.getElementById('delete-modal');
    const modalCancelBtn = document.getElementById('modal-cancel-btn');
    const modalConfirmBtn = document.getElementById('modal-confirm-btn');
    let activeDeleteForm = null;

    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            activeDeleteForm = form;
            if (deleteModal) {
                deleteModal.classList.add('active');
            } else if (confirm('Are you sure you want to delete this note?')) {
                form.submit();
            }
        });
    });

    if (modalCancelBtn && deleteModal) {
        modalCancelBtn.addEventListener('click', () => {
            deleteModal.classList.remove('active');
            activeDeleteForm = null;
        });
    }

    if (modalConfirmBtn && deleteModal) {
        modalConfirmBtn.addEventListener('click', () => {
            if (activeDeleteForm) {
                activeDeleteForm.submit();
            }
            deleteModal.classList.remove('active');
        });
    }

    // Close modal on backdrop click
    if (deleteModal) {
        deleteModal.addEventListener('click', (e) => {
            if (e.target === deleteModal) {
                deleteModal.classList.remove('active');
                activeDeleteForm = null;
            }
        });
    }

    // ==========================================
    // 4. Flash Message Dismissal
    // ==========================================
    document.querySelectorAll('.flash-close').forEach(btn => {
        btn.addEventListener('click', () => {
            const flashMsg = btn.closest('.flash-message');
            if (flashMsg) {
                flashMsg.remove();
            }
        });
    });
});
