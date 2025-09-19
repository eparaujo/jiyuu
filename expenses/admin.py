from django.contrib import admin
from . import models

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duedate', 'paid',)
    search_fields = ('name',)

admin.site.register(models.Expense, ExpenseAdmin)

