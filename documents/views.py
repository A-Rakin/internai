from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def list(request, pk=None, internship_id=None):
    return render(request, 'documents/document_list.html')
