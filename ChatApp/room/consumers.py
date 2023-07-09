import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from time import strftime

from django.contrib.auth.models import User

from .models import Message, Room
from .templatetags.chatextras import initials

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Recieve message from WebSocket (frontend)
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        ini = initials(username)

        new_message = await self.save_message(username, room, message)

        # Send message to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
                'initials': ini,
                'created_at': strftime("%H:%M"),
            }
        )
    
    async def chat_message(self, event):
        # Send message to the WebSocket (frontend)
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'room': event['room'],
            'initials': event['initials'],
            'created_at': event['created_at']
        }))

    @sync_to_async  # talk to database
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        message = Message.objects.create(sent_by=user, content=message)

        room.messages.add(message)

        return message