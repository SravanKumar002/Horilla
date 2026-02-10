from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_company', 'is_active', 'created_by', 'modified_by')
    list_filter = ('is_active', 'parent_company')
    search_fields = ('name',)
    fields = ('name', 'parent_company', 'is_active')

    readonly_fields = ('created_by', 'modified_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
