from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from chatalexia.chat.models import Room


class ChatRoomsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/index.html')


chat_rooms_view = ChatRoomsView.as_view()


class ChatView(LoginRequiredMixin, View):
    def get(self, request, room_name):
        room, created = Room.objects.get_or_create(name=room_name)
        messages = room.messages.all()
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'username': request.user.username,
            'msgs': messages
        })


chat_view = ChatView.as_view()

