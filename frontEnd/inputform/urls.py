from django.urls import path

from . import views

app_name = 'upload_form'
urlpatterns = [
    path('', views.index, name='index'),
]