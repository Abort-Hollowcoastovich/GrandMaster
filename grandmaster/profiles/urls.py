from django.urls import path

from .views import UserDetails, DocumentsDetails, UserList

urlpatterns = [
    path('documents/<int:pk>/', DocumentsDetails.as_view(), name='documents-detail'),
    path('<int:pk>/', UserDetails.as_view(), name='user-detail'),
    path('', UserList.as_view()),
]
