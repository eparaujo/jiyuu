from django.contrib import admin
from . import models

# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('karateca', 'billing_cycle', 'due_date', 'total_amount', 'paid', 'paid_at', 'created_at',)
    search_fields = ('billing_cycle',)

admin.site.register (models.Invoice, InvoiceAdmin)