from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import loader
from .forms import UploadForm
from inputform import exportUserForm

# Create your views here.

def index(request):
    if request.method == 'GET':
        uploadForm = UploadForm()
        return render(request, 'forms/index.html', {'uploadForm': uploadForm})
    elif request.method == 'POST':
         form = UploadForm(request.POST, request.FILES)
         print(form.errors)
         if form.is_valid():
            print(form.cleaned_data)
            return redirect('./')
         return render(request, 'forms/index.html')
