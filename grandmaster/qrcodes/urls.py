from django.urls import path

from .views import ForPartnersView, ForEventsView, UserDetailsView

urlpatterns = [
    path('users/<int:pk>/', UserDetailsView.as_view()),
    path('for_partners/', ForPartnersView.as_view()),
    path('for_events/', ForEventsView.as_view()),
]
