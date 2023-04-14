from django.urls import path
from jobs import jobs 
from . import views


urlpatterns = [
    path("", views.AdminInstaStampList.as_view()),
    path("result/", views.AdminInataStampResult.as_view()),
    path("csv-result/", views.CSVDownloadView.as_view()),
    path("edit-keywords/", views.KeywordsUpdate.as_view()),
    path("chart-result/", views.ChartView.as_view()),
    path("schedule-test/", jobs.schedule_api, name="schedule"),
]
