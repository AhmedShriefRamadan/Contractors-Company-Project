from django.urls import path

from .views import create_new_excel,download_excel

urlpatterns = [
    path('excel/', create_new_excel, name='create_excel'),
    path('download/<int:id>/', download_excel, name='download'),
]