from django.contrib import admin
from .models import InstaStampList
from insta_admin.models import InstaKeywords

@admin.register(InstaStampList)
class InstaStampAdmin(admin.ModelAdmin): 
    list_display = ( 
        "insta_url", 
        "insta_name",
        "insta_date",
        "created_at", 
        "insta_stamp", 
        "hashtags", 
    )

@admin.register(InstaKeywords)
class InstaKeywordsAdmin(admin.ModelAdmin):
    list_display = (
        "pk", 
        "created_at", 
        "keywords",
    )