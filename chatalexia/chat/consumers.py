import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import make_aware

from chatalexia.chat.models import Room, Message


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.room_name = None
        self.room_group_name = None
        self.user = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room, created = Room.objects.get_or_create(name=self.room_name)
        if created:
            self.room.save()

        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            return

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_from = text_data_json['user_from']
        time = make_aware(datetime.now())

        m = Message.objects.create(from_user=self.user, text=message, sent=time)
        m.save()
        self.room.messages.add(m)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user_from': user_from
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['user_from']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_from': username
        }))
