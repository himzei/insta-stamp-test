from django.db import models

class InstaStampResult(models.Model):     
    created_at = models.DateTimeField(auto_now_add=True)
    total_insta = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_friends = models.IntegerField(default=0)

class InstaKeywords(models.Model): 
    created_at =  models.DateTimeField(auto_now_add=True)
    keywords =    models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.keywords
    
    class Meta:
        verbose_name_plural = "인스타 키워드"