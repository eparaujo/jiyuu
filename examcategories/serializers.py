from rest_framework import serializers
from examcategories.models import ExamCategory


class ExamCategoriesSerializers(serializers.ModelSerializer):
     name = serializers.CharField(
        source="name_category",
        read_only=True
    )

class Meta:
        model = ExamCategory
        fields = [
            "id",
            "name",
            "name_category",
            "description",
        ]