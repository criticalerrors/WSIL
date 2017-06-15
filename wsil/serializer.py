from rest_framework import serializers
from wsil.models import Language, RepositoryUsingIt


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("name",)


class Top10Serializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryUsingIt
        fields = ("language", "repository_count",)
