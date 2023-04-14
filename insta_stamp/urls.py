from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.Crawling.as_view()), 
    path("csv-result/", views.CSVDownloadView.as_view()),
    path("ranking/", views.RankingList.as_view()),
    path("data-insert", views.DataForceInsert.as_view()),
]
