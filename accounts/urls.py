from django.urls import path, include

from accounts.views import MyProfileView

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('profile/<int:pk>/', MyProfileView.as_view({'get': 'retrieve', 'put': 'update'}), name='profile'),
]