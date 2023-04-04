from django.db import models


class InstaStampList(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    insta_name = models.CharField(max_length=50) 
    insta_url = models.CharField(max_length=255)
    insta_ref = models.CharField(max_length=255, unique=True)
    insta_date = models.CharField(max_length=50, blank=True, null=True)
    insta_stamp = models.BooleanField(default=True)
    phone = models.CharField(max_length=50, blank=True, null=True) 
    likes_cnt = models.IntegerField(default=0, blank=True, null=True)
    comments_cnt = models.IntegerField(default=0, blank=True, null=True)
    friends_cnt = models.IntegerField(default=0, blank=True, null=True)





