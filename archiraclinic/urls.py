from django.urls import path
from . import views

app_name = 'archiraclinic'

urlpatterns = [
    path('companies/', views.company_list, name='company_list'),
]
