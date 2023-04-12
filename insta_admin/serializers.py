from rest_framework import serializers
from .models import InstaStampResult, InstaKeywords


class InstaStampResultSerializer(serializers.ModelSerializer):
    class Meta: 
        model = InstaStampResult
        fields = (
            "created_at",
            "total_insta", 
            "total_likes", 
            "total_comments", 
            "total_friends",
        )


class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstaKeywords
        fields = (
            "pk",
            "created_at", 
            "keywords",
        )