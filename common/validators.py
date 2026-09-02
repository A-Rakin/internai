"""
============================================================
Common File & Media Security Validators
============================================================
Provides strict file extension and MIME type validation to prevent
malicious script/executable uploads across all application panels.
============================================================
"""

import os
from django.core.exceptions import ValidationError

# Allowed file extensions per category
ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp']
ALLOWED_RESUME_EXTENSIONS = ['.pdf', '.doc', '.docx']
ALLOWED_GENERAL_DOC_EXTENSIONS = ['.pdf', '.doc', '.docx', '.png', '.jpg', '.jpeg', '.webp']

# Explicitly forbidden dangerous extensions
DANGEROUS_EXTENSIONS = [
    '.exe', '.bat', '.cmd', '.sh', '.php', '.py', '.js', '.vbs', '.dll',
    '.scr', '.msi', '.jar', '.apk', '.html', '.htm', '.asp', '.aspx', '.pl',
    '.cgi', '.ps1', '.reg', '.vbe', '.wsf', '.wsh', '.pif', '.application'
]


def validate_image_file(uploaded_file):
    """
    Validate that an uploaded file is strictly a valid image format.
    Allowed extensions: .png, .jpg, .jpeg, .webp
    """
    if not uploaded_file:
        return

    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext in DANGEROUS_EXTENSIONS:
        raise ValidationError(f"Security Alert: Executable or script files ({ext}) are strictly prohibited.")

    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        allowed_str = ", ".join(ALLOWED_IMAGE_EXTENSIONS)
        raise ValidationError(f"Invalid image format ({ext}). Please upload an image file ({allowed_str}).")

    # Content type check if available
    content_type = getattr(uploaded_file, 'content_type', '')
    if content_type and not content_type.startswith('image/'):
        raise ValidationError("Uploaded file is not a valid image format.")


def validate_resume_file(uploaded_file):
    """
    Validate that an uploaded resume/CV is strictly PDF or Word document.
    Allowed extensions: .pdf, .doc, .docx
    """
    if not uploaded_file:
        return

    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext in DANGEROUS_EXTENSIONS:
        raise ValidationError(f"Security Alert: Executable or script files ({ext}) are strictly prohibited.")

    if ext not in ALLOWED_RESUME_EXTENSIONS:
        allowed_str = ", ".join(ALLOWED_RESUME_EXTENSIONS)
        raise ValidationError(f"Invalid resume format ({ext}). Please upload a PDF or Word document ({allowed_str}).")


def validate_document_file(uploaded_file, doc_type='other'):
    """
    Validate document vault uploads based on document category.
    """
    if not uploaded_file:
        return

    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext in DANGEROUS_EXTENSIONS:
        raise ValidationError(f"Security Alert: Executable or script files ({ext}) are strictly prohibited.")

    if doc_type == 'formal_photo':
        validate_image_file(uploaded_file)
    elif doc_type in ['resume', 'cover_letter']:
        validate_resume_file(uploaded_file)
    else:
        if ext not in ALLOWED_GENERAL_DOC_EXTENSIONS:
            allowed_str = ", ".join(ALLOWED_GENERAL_DOC_EXTENSIONS)
            raise ValidationError(f"Invalid document format ({ext}). Allowed formats: {allowed_str}.")
