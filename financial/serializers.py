from rest_framework import serializers


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