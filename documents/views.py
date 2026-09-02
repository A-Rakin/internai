"""
============================================================
Documents Views - File & Document Repository
============================================================
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from documents.models import Document, ActivityLog


@login_required
def list(request):
    """List and upload documents for the current user."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        doc_type = request.POST.get('doc_type', 'other')
        description = request.POST.get('description', '').strip()
        uploaded_file = request.FILES.get('file')

        if not title or not uploaded_file:
            messages.error(request, 'Document title and file are required.')
        else:
            try:
                from common.validators import validate_document_file
                validate_document_file(uploaded_file, doc_type)
            except Exception as ve:
                messages.error(request, str(ve).strip("['']"))
                return redirect('documents:list')

            doc = Document.objects.create(
                user=request.user,
                title=title,
                doc_type=doc_type,
                description=description,
                file=uploaded_file,
                file_size=uploaded_file.size,
            )
            ActivityLog.objects.create(
                user=request.user,
                action='document_upload',
                description=f'Uploaded document "{doc.title}"',
            )
            messages.success(request, f'Document "{doc.title}" uploaded successfully!')
            return redirect('documents:list')

    docs = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    context = {'documents': docs}
    return render(request, 'documents/document_list.html', context)


@login_required
def delete_document(request, pk):
    """Delete a document owned by the user."""
    doc = get_object_or_404(Document, pk=pk, user=request.user)
    title = doc.title
    doc.delete()
    messages.success(request, f'Document "{title}" deleted successfully.')
    return redirect('documents:list')
