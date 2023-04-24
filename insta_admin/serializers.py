from rest_framework import serializers
from .models import InstaStampResult, InstaKeywords, InstaSetting



class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstaKeywords
        fields = (
            "pk",
            "created_at", 
            "keywords",
            "insta_setting_ref",
        )


class InstaSettingSerializer(serializers.ModelSerializer):
    
    hashtags = KeywordsSerializer(many=True, read_only=True)

    class Meta:
        model = InstaSetting
        fields = (
            "id",
            "official_url", 
            "events_name", 
            "events_date", 
            "hashtags_selected",
            "hashtags",
        )

class InstaStampResultSerializer(serializers.ModelSerializer):
    class Meta: 
        model = InstaStampResult
        fields = (
            "created_at",
            "total_insta", 
            "total_likes", 
            "total_comments", 
            "total_friends",
            "hashtags",
        )


