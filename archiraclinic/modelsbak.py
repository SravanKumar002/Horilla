from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Company Name"))
    parent_company = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_companies',
        verbose_name=_("Headquarter Company"),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name='archiraclinic_created_companies',
        verbose_name=_("Created By"),
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name='archiraclinic_modified_companies',
        verbose_name=_("Modified By"),
    )
    horilla_history = AuditlogHistoryField()
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.name


# Register auditlog for the Company model
auditlog.register(Company, serialize_data=True)
