from rest_framework import serializers
from wsil.models import Suggestion


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("keyword", "suggested_keyword")