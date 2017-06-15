from rest_framework import serializers
from wsil.models import Language


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("name",)
