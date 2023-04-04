from django.urls import path

from jobs import jobs 
from . import views


urlpatterns = [
    path("", views.AdminInstaStampList.as_view()),
    path("result/", views.AdminInataStampResult.as_view()),
]
