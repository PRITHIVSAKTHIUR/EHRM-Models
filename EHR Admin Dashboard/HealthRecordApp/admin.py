from django.contrib import admin
from .models import HealthRecord
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(HealthRecord)

class IEAdmin(ImportExportModelAdmin):
    pass