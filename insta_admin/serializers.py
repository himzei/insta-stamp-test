from rest_framework import serializers
from .models import InstaStampResult

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