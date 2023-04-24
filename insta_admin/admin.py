from django.contrib import admin
from .models import InstaStampResult, InstaSetting


@admin.register(InstaStampResult)
class InstaStampResultAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "total_insta",
        "total_likes",
        "total_comments",
    )

@admin.register(InstaSetting)
class InstaSettingAdmin(admin.ModelAdmin): 
    list_display = (
        "events_name", 
        "events_date", 
        "hashtags_selected", 
    )