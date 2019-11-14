from django import forms
from inputform.models import UserForm

class UploadForm(forms.Form):
    email = forms.EmailField(label='Email:', widget=forms.EmailInput())
    file = forms.FileField(label='Archivo (pdf):')
    quarter = forms.CharField(label='Cuatrimestre:')
    students_ids = forms.CharField(label='Legajos:')
    students_names = forms.CharField(label='Nombres:')
    subject = forms.CharField(label='Materia:')
    year = forms.CharField(label='Año:')

