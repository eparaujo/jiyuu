from rest_framework import serializers
from examcategories.models import ExamCategory


class ExamCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamCategory
        fields = '__all__'