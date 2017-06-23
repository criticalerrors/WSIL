from rest_framework import serializers
from wsil.models import Language, RepositoryUsingIt, InterestOverTimeLanguage, InterestByRegionLanguage


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


class InterestByRegionSerializer(serializers.Serializer):
    interest_rate = serializers.IntegerField()
    region = serializers.CharField()


class InterestOverTimeFwSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    interest_rate = serializers.IntegerField()


class InterestByRegionFwSerializer(serializers.Serializer):
    interest_rate = serializers.IntegerField()
    region = serializers.CharField()



