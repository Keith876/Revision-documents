from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .models import Document
from .forms import DocumentForm

# Home page view to list uploaded documents
def home(request):
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'Ppapers/home.html', {'documents': documents})

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid login credentials")
    return render(request, 'Ppapers/login.html')

# User logout
def user_logout(request):
    logout(request)
    return redirect('home')

# Document upload view (only accessible to logged-in users)
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'Ppapers/upload_document.html', {'form': form})

