from django.urls import path

from .views import chat_rooms_view, chat_view

app_name = "chat"
urlpatterns = [
    path('', chat_rooms_view, name='index'),
    path('<str:room_name>/', chat_view, name='room'),
]