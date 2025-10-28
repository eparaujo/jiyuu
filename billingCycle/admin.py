from django.contrib import admin
from . import models


class BillingCycleAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'closed',)
    search_fields = ('month',)

admin.site.register(models.BillingCycle, BillingCycleAdmin) 