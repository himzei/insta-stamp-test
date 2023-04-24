from django.db import models

class InstaSetting(models.Model): 
    official_url = models.CharField(max_length=255)
    events_name = models.CharField(max_length=120)
    events_date = models.CharField(max_length=120)
    hashtags_selected = models.IntegerField(default=1)
    hashtags = models.ManyToManyField(
      "InstaKeywords", 
      related_name="insta_events"
    )

    def __str__(self): 
        return self.events_name
      

class InstaStampResult(models.Model):     
    created_at = models.DateTimeField(auto_now_add=True)
    total_insta = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_friends = models.IntegerField(default=0)
    hashtags = models.ForeignKey(
        "InstaKeywords", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="insta_admin"
        )

class InstaKeywords(models.Model): 
    created_at =  models.DateTimeField(auto_now_add=True)
    keywords =    models.CharField(max_length=255, blank=True, null=True)
    insta_setting_ref = models.ForeignKey(
        "InstaSetting", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="insta_keywords",
        )

    def __str__(self):
        return self.keywords
    
    class Meta:
        verbose_name_plural = "인스타 키워드"