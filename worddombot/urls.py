from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('bot.urls')),
    path('dashboard/', admin.site.urls),
]
