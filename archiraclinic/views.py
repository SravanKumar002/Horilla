from django.shortcuts import render
from .models import Company

def company_list(request):
    companies = Company.objects.filter(is_active=True).order_by('name')
    return render(request, 'archiraclinic/company_list.html', {'companies': companies})
