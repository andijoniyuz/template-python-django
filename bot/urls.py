from django.urls import path
from .views import process_telegram_updates

urlpatterns = [
    path('<str:bot_token>/', process_telegram_updates)
]
