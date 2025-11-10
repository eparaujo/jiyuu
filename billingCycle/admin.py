from django.contrib import admin, messages
from django.utils import timezone
from .models import BillingCycle

@admin.register(BillingCycle)
class BillingCycleAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'start_date', 'end_date', 'closed', 'closed_at', 'created_at')
    list_filter = ('year', 'month', 'closed')
    ordering = ('-year', '-month')
    actions = ['close_selected_cycles', 'reset_selected_cycles']

    @admin.action(description="🔒 Fechar ciclo(s) selecionado(s)")
    def close_selected_cycles(self, request, queryset):
        closed_count = 0
        for cycle in queryset:
            if not cycle.closed:
                cycle.close_cycle()
                closed_count += 1
        if closed_count:
            messages.success(request, f"{closed_count} ciclo(s) fechado(s) com sucesso!")
        else:
            messages.info(request, "Nenhum ciclo foi fechado (todos já estavam fechados).")

    @admin.action(description="♻️ Limpar faturas e reabrir ciclo(s) selecionado(s)")
    def reset_selected_cycles(self, request, queryset):
        total_deleted = 0
        for cycle in queryset:
            try:
                deleted = cycle.reset_cycle(confirm=True)
                total_deleted += deleted
            except Exception as e:
                messages.error(request, f"Erro ao limpar ciclo {cycle}: {e}")
        messages.success(request, f"✅ {total_deleted} fatura(s) apagada(s) e ciclo(s) reaberto(s).")
