from django.contrib import admin
from .models import InstaStampResult


@admin.register(InstaStampResult)
class InstaStampResultAdmin(admin.ModelAdmin):
    list_display = (
        
"created_at",
"total_insta",
"total_likes",
"total_comments",
    )