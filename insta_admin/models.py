from django.db import models

class InstaStampResult(models.Model): 
    
    created_at = models.DateTimeField(auto_now_add=True)
    total_insta = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_friends = models.IntegerField(default=0)
