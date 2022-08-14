from django.urls import path

from .views import ForPartnersView

urlpatterns = [
    path('for_partners/', ForPartnersView.as_view()),
    # path('for_events/', UserList.as_view()),
]
