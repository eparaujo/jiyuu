from rest_framework import serializers
from datetime import date

from .models import Invoice


class InvoiceDashboardSerializer(serializers.ModelSerializer):

    karateca_name = serializers.CharField(
        source="karateca.name",
        read_only=True
    )

    age = serializers.SerializerMethodField()

    graduation = serializers.CharField(
        source="karateca.graduation",
        read_only=True
    )

    dojo = serializers.CharField(
        source="karateca.dojo",
        read_only=True
    )

    birth_date = serializers.DateField(
        source="karateca.birth_date",
        read_only=True
    )

    status = serializers.SerializerMethodField()

    days_remaining = serializers.SerializerMethodField()

    days_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Invoice

        fields = [
            "id",

            "karateca_name",
            "age",
            "graduation",
            "dojo",
            "birth_date",

            "total_amount",

            "due_date",

            "paid",

            "status",

            "days_remaining",

            "days_overdue",
        ]

    # ================= AGE =================

    def get_age(self, obj):

        return obj.karateca.age

    # ================= STATUS =================

    def get_status(self, obj):

        today = date.today()

        if obj.paid:
            return "PAGO"

        if obj.due_date < today:
            return "ATRASADO"

        diff = (obj.due_date - today).days

        if diff <= 5:
            return "VENCENDO"

        return "PENDENTE"

    # ================= DAYS REMAINING =================

    def get_days_remaining(self, obj):

        if obj.paid:
            return 0

        today = date.today()

        diff = (obj.due_date - today).days

        return diff if diff > 0 else 0

    # ================= DAYS OVERDUE =================

    def get_days_overdue(self, obj):

        if obj.paid:
            return 0

        today = date.today()

        diff = (today - obj.due_date).days

        return diff if diff > 0 else 0