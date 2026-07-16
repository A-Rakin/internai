/**
 * ============================================================
 * InternAI - Form Validation & Enhancement
 * ============================================================
 * Client-side form validation, file upload preview,
 * password strength meter, and dynamic form helpers.
 * ============================================================
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // 1. PASSWORD VISIBILITY TOGGLE
    // ============================================================

    // Find all password toggle buttons
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');

    // Add click handler to each toggle button
    togglePasswordBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            // Find the associated password input (previous sibling or within wrapper)
            const input = this.closest('.input-icon-wrapper').querySelector('input');

            // Toggle between 'password' and 'text' type
            if (input.type === 'password') {
                input.type = 'text';                   // Show password
                this.innerHTML = '<i class="fas fa-eye-slash"></i>'; // Change icon
            } else {
                input.type = 'password';               // Hide password
                this.innerHTML = '<i class="fas fa-eye"></i>';      // Change icon
            }
        });
    });

    // ============================================================
    // 2. PASSWORD STRENGTH METER
    // ============================================================

    // Find password input with strength meter
    const passwordInput = document.getElementById('password');
    const strengthFill = document.querySelector('.password-strength-fill');
    const strengthText = document.querySelector('.password-strength-text');

    // Only run if password input and strength meter exist
    if (passwordInput && strengthFill) {
        passwordInput.addEventListener('input', function() {
            // Get the current password value
            const password = this.value;

            // Calculate password strength score (0-4)
            let score = 0;

            // Check password length (minimum 8 characters)
            if (password.length >= 8) score++;

            // Check for lowercase letters
            if (/[a-z]/.test(password)) score++;

            // Check for uppercase letters
            if (/[A-Z]/.test(password)) score++;

            // Check for numbers
            if (/[0-9]/.test(password)) score++;

            // Check for special characters
            if (/[^A-Za-z0-9]/.test(password)) score++;

            // Map score to strength level
            const levels = {
                0: { class: '', text: '' },
                1: { class: 'weak', text: 'Weak' },
                2: { class: 'fair', text: 'Fair' },
                3: { class: 'good', text: 'Good' },
                4: { class: 'strong', text: 'Strong' },
                5: { class: 'strong', text: 'Very Strong' },
            };

            // Get the appropriate level
            const level = levels[score] || levels[0];

            // Remove all existing strength classes
            strengthFill.className = 'password-strength-fill';

            // Add the new strength class
            if (level.class) {
                strengthFill.classList.add(level.class);
            }

            // Update the text indicator
            if (strengthText) {
                strengthText.textContent = level.text;
            }
        });
    }

    // ============================================================
    // 3. FILE UPLOAD PREVIEW
    // ============================================================

    // Find all file input elements
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            // Get the selected file
            const file = this.files[0];

            // Find the associated preview element
            const previewEl = document.querySelector(
                '[data-preview="' + this.id + '"]'
            );

            // If no file selected or no preview element, exit
            if (!file || !previewEl) return;

            // Check if it's an image file
            if (file.type.startsWith('image/')) {
                // Create a FileReader to read the image
                const reader = new FileReader();

                // When the file is loaded, update the preview
                reader.onload = function(e) {
                    previewEl.src = e.target.result;    // Set image source
                    previewEl.style.display = 'block';  // Show preview
                };

                // Read the file as a data URL (base64)
                reader.readAsDataURL(file);
            } else {
                // For non-image files, show file name and size
                const fileName = file.name;
                const fileSize = (file.size / 1024).toFixed(1) + ' KB';

                // Update the preview element with file info
                if (previewEl.tagName === 'SPAN' || previewEl.tagName === 'P') {
                    previewEl.textContent = fileName + ' (' + fileSize + ')';
                }
            }
        });
    });

    // ============================================================
    // 4. DRAG AND DROP FILE UPLOAD
    // ============================================================

    // Find all upload areas
    const uploadAreas = document.querySelectorAll('.upload-area');

    uploadAreas.forEach(function(area) {
        // Find the associated file input
        const fileInput = area.querySelector('input[type="file"]') ||
                          document.getElementById(area.dataset.input);

        // Click to upload
        area.addEventListener('click', function() {
            if (fileInput) fileInput.click();
        });

        // Drag over - add visual feedback
        area.addEventListener('dragover', function(e) {
            e.preventDefault();                         // Required for drop
            this.classList.add('drag-over');             // Add highlight class
        });

        // Drag leave - remove visual feedback
        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');          // Remove highlight
        });

        // Drop - handle dropped file
        area.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');

            // Get the dropped files
            const files = e.dataTransfer.files;

            // If a file input exists, set its files
            if (fileInput && files.length > 0) {
                fileInput.files = files;
                // Trigger change event for preview
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    });

    // ============================================================
    // 5. FORM VALIDATION
    // ============================================================

    // Find all forms with the 'needs-validation' class
    const forms = document.querySelectorAll('.needs-validation');

    // Add validation handler to each form
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            // Check if the form is valid using HTML5 validation
            if (!form.checkValidity()) {
                // Prevent form submission
                event.preventDefault();
                event.stopPropagation();
            }

            // Add Bootstrap validation classes for visual feedback
            form.classList.add('was-validated');
        });
    });

    // ============================================================
    // 6. SKILL TAG INPUT
    // ============================================================

    // Find skill input fields
    const skillInput = document.getElementById('skillInput');
    const skillsContainer = document.getElementById('skillsContainer');
    const skillsHidden = document.getElementById('skillsHidden');

    // Only run if skill input exists
    if (skillInput && skillsContainer) {
        // Listen for Enter key or comma in skill input
        skillInput.addEventListener('keydown', function(e) {
            // Check for Enter key (13) or comma key (188)
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();

                // Get the trimmed skill text
                const skill = this.value.trim().replace(',', '');

                // Add skill if not empty
                if (skill) {
                    addSkillTag(skill);
                    this.value = '';                     // Clear input
                }
            }
        });
    }

    /**
     * Add a skill tag to the skills container.
     *
     * @param {string} skill - The skill text to add
     */
    function addSkillTag(skill) {
        // Create the tag element
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.innerHTML = skill +
            ' <span class="remove-tag" onclick="this.parentElement.remove(); updateSkillsHidden();">' +
            '<i class="fas fa-times"></i></span>';

        // Add the tag to the container
        skillsContainer.appendChild(tag);

        // Update the hidden input with all skills
        updateSkillsHidden();
    }

    // ============================================================
    // 7. MULTI-STEP FORM NAVIGATION
    // ============================================================

    // Find multi-step form elements
    const formSteps = document.querySelectorAll('.form-step');
    const stepIndicators = document.querySelectorAll('.step-indicator');
    const stepConnectors = document.querySelectorAll('.step-connector');
    let currentStep = 0;

    // Next step buttons
    const nextBtns = document.querySelectorAll('.btn-next-step');
    nextBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            // Validate current step before moving
            if (validateStep(currentStep)) {
                goToStep(currentStep + 1);
            }
        });
    });

    // Previous step buttons
    const prevBtns = document.querySelectorAll('.btn-prev-step');
    prevBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            goToStep(currentStep - 1);
        });
    });

    /**
     * Navigate to a specific form step.
     *
     * @param {number} stepIndex - The step to navigate to (0-indexed)
     */
    function goToStep(stepIndex) {
        // Bounds checking
        if (stepIndex < 0 || stepIndex >= formSteps.length) return;

        // Hide all steps
        formSteps.forEach(function(step) {
            step.style.display = 'none';
        });

        // Show the target step
        formSteps[stepIndex].style.display = 'block';

        // Update step indicators
        stepIndicators.forEach(function(indicator, index) {
            indicator.classList.remove('active', 'completed');
            if (index < stepIndex) {
                indicator.classList.add('completed');
            } else if (index === stepIndex) {
                indicator.classList.add('active');
            }
        });

        // Update step connectors
        stepConnectors.forEach(function(connector, index) {
            connector.classList.remove('active', 'completed');
            if (index < stepIndex) {
                connector.classList.add('completed');
            } else if (index === stepIndex) {
                connector.classList.add('active');
            }
        });

        // Update current step tracker
        currentStep = stepIndex;
    }

    /**
     * Validate all required fields in the current step.
     *
     * @param {number} stepIndex - The step to validate
     * @returns {boolean} - Whether the step is valid
     */
    function validateStep(stepIndex) {
        const step = formSteps[stepIndex];
        if (!step) return true;

        // Find all required inputs in this step
        const requiredFields = step.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(function(field) {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });

        return isValid;
    }

}); // End DOMContentLoaded

/**
 * Update the hidden skills input with all current skill tags.
 * Called when skills are added or removed.
 */
function updateSkillsHidden() {
    // Get the hidden input and skills container
    const skillsHidden = document.getElementById('skillsHidden');
    const skillsContainer = document.getElementById('skillsContainer');

    if (skillsHidden && skillsContainer) {
        // Get all skill tags
        const tags = skillsContainer.querySelectorAll('.skill-tag');
        // Extract text content from each tag (excluding the remove button)
        const skills = Array.from(tags).map(function(tag) {
            return tag.textContent.trim().replace('×', '').trim();
        });
        // Join with commas and set as hidden input value
        skillsHidden.value = skills.join(', ');
    }
}
