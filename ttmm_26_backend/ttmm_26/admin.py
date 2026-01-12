from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Investor, Startup, Funding, PortalControl

class InvestorAdmin(ImportExportModelAdmin):
    search_fields = ["name"]

admin.site.register(Investor, InvestorAdmin)
admin.site.register(Startup)
admin.site.register(Funding)
admin.site.register(PortalControl)