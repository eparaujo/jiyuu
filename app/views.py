import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import metrics


@login_required(login_url='login')
def home(request):

    dojo_metrics = metrics.get_karateca_metrics()
    revenue_metrics = metrics.get_revenue_metrics()
    daily_expenses_data = metrics.get_expense_data()
    daily_revenues_data = metrics.get_revenues_data()
 
    context = { 
        'dojo_metrics': dojo_metrics, 
        'revenue_metrics':revenue_metrics,
        'daily_expenses_data': json.dumps(daily_expenses_data),
        'daily_revenues_data': json.dumps(daily_revenues_data), #transforma um dicionário em json
    }
    return render(request, 'home.html', context=context) 