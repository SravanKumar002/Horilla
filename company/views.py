from django.shortcuts import render

# Create your views here.
from django.urls import path
from base.models import Company
from horilla.decorators import (
    login_required,
    permission_required,
)
from horilla.methods import get_horilla_model_class

def _build_company_hierarchy(company_list):
    """
    Return a nested structure of companies and their children for template rendering.
    """
    nodes = {
        company.id: {"company": company, "children": []} for company in company_list
    }
    roots = []

    for company in company_list:
        parent_id = company.parent_company_id
        node = nodes[company.id]
        if parent_id and parent_id in nodes:
            nodes[parent_id]["children"].append(node)
        else:
            roots.append(node)

    # Sort children alphabetically for consistent UI
    def sort_children(node):
        node["children"].sort(key=lambda child: child["company"].company.lower())
        for child in node["children"]:
            sort_children(child)

    for root in roots:
        sort_children(root)

    roots.sort(key=lambda root: root["company"].company.lower())
    return roots


@login_required
@permission_required("base.view_company")
def company_index(request):
    # Get filtered companies for this user only
    # This ensures users from Company A (e.g., visko) never see Company B (e.g., Igniculuss)
    company_qs = Company.get_companies_for_user(request.user).select_related(
        "parent_company"
    )

    # Force evaluation of queryset to ensure filtering is applied
    company_list = list(company_qs)
    
    # Build hierarchy only from the filtered companies
    company_hierarchy = _build_company_hierarchy(company_list)
    EmployeeWorkInformation = get_horilla_model_class(
    app_label="employee", model="employeeworkinformation"
    )
    for company in company_list:
        # 1. Employee count (active employees only)
        company.employee_count = EmployeeWorkInformation.objects.filter(
        company_id_id=company,
        employee_id__is_active=True,
        ).count()
        print("employee_count",company.employee_count)
        # 2. Sub-company count
        company.sub_company_count = sum(
        1 for c in company_list if c.parent_company_id == company.id
        )
        # OR:
        # company.sub_company_count = sum(1 for c in company_list if c.parent_company_id == company.id)
        print("sub_company_count",company.sub_company_count)

    return render(
        request,
        "company/companies_card.html",
        {
            "companies": company_list,
            "company_hierarchy": company_hierarchy,
            "model": Company(),
        },
    )

