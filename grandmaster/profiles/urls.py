from django.urls import path

from .views import ProfileDetails, ProfileList, DocumentsDetails

urlpatterns = [
    path('documents/<int:pk>/', DocumentsDetails.as_view(), name='documents-detail'),
    path('<int:pk>/', ProfileDetails.as_view(), name='userprofile-detail'),
    path('', ProfileList.as_view()),
]
