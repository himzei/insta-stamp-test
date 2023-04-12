from rest_framework import serializers
from .models import InstaStampList

class InstaStampListSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = InstaStampList
        fields = (
            "created_at", 
            "insta_name", 
            "insta_url",
            "insta_ref", 
            "insta_date", 
            "insta_stamp",
            "phone", 
            "likes_cnt", 
            "comments_cnt", 
            "friends_cnt",
            ) 
     
        