from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class ChatRoomsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/index.html')


chat_rooms_view = ChatRoomsView.as_view()


class ChatView(LoginRequiredMixin, View):
    def get(self, request, room_name):
        return render(request, 'chat/room.html', {
            'room_name': room_name
        })


chat_view = ChatView.as_view()

