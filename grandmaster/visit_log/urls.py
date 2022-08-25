from django.urls import path

from .views import ScheduleView, make_report

urlpatterns = [
    path('', ScheduleView.as_view()),
    path('report/', make_report)
]
