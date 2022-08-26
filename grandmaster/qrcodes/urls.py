from django.urls import path

from .views import ForPartnersView, ForEventsView

urlpatterns = [
    path('for_partners/', ForPartnersView.as_view()),
    path('for_events/', ForEventsView.as_view()),
]
