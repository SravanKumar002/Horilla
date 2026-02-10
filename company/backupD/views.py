from django.shortcuts import render

# Create your views here.
from django.urls import path
from base.models import Company
from horilla.decorators import (login_required,permission_required,)



@login_required
@permission_required("base.view_company")
def company_index(request):
    companies = Company.objects.all()
    return render(request, "company/companies_card.html",{"companies": companies, "model": Company()},)

