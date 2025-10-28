from django.contrib import admin
from . import models

# Register your models here.
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'amount', 'item_type', 'due_date', )
    search_fields = ('invoice',)

admin.site.register(models.InvoiceItem, InvoiceItemAdmin)