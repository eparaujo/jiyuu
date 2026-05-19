from rest_framework import serializers


"""
O objetivo destas classes, é controlar a parte financeira, inadimplência, pagamentos etc.
"""

class FinancialTransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()
    category = serializers.CharField()
    date = serializers.DateField()
    value = serializers.FloatField()


class FinancialChartSerializer(serializers.Serializer):
    day = serializers.IntegerField()
    value = serializers.FloatField()


class FinancialDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    total = serializers.FloatField()
    chart = FinancialChartSerializer(many=True)
    transactions = FinancialTransactionSerializer(many=True)

class DelinquentItemSerializer(serializers.Serializer):
    type = serializers.CharField()
    description = serializers.CharField()
    amount = serializers.FloatField()
    due_date = serializers.DateField()


class DelinquentStudentSerializer(serializers.Serializer):
    karateca_id = serializers.IntegerField()
    name = serializers.CharField()
    dojo = serializers.CharField()
    graduation = serializers.CharField(allow_null=True)

    invoice_id = serializers.IntegerField()
    total_amount = serializers.FloatField()

    overdue_days = serializers.IntegerField()

    items = DelinquentItemSerializer(many=True)