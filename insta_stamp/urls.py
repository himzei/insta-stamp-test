from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.Crawling.as_view()), 
]
