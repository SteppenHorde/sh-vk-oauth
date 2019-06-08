from django.urls import path

from . import views



urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('get_users/', views.GetUsers.as_view(), name='get_users'),
]
