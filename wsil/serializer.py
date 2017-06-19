from rest_framework import serializers
from wsil.models import Language, RepositoryUsingIt, InterestOverTimeLanguage


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("name", "id",)


class Top10Serializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryUsingIt
        fields = ("language", "repository_count",)


class InterestOverTimeSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    interest_rate = serializers.IntegerField()
