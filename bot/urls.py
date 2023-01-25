from django.urls import path

from .views import web_hook

urlpatterns = [
    path(f'bot/<str:token>/', web_hook),
]