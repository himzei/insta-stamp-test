from django.contrib import admin
from .models import InstaStampList

@admin.register(InstaStampList)
class InstaStampAdmin(admin.ModelAdmin): 
    list_display = ( "insta_url", "insta_name","insta_date","created_at", "insta_stamp" )