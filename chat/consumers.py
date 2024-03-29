# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Group, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        group_name = data['group_name']
        group = Group.objects.get(name=group_name)
        messages = Message.last_10_messages(group)
        content = {
            "command": "messages",
            "messages": self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_messsge(self, data):
        author = data["from"]
        author_user = User.objects.get(username=author)
        group_name = data["group_name"]
        group = Group.objects.get(name=group_name)
        message = data["message"]
        message = Message.objects.create(
            group=group,
            author=author_user,
            content=message)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.author.username,
            "author_id": message.author.id,
            "author_picture": message.author.profile.picture.url,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_messsge,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    # Send message to room group

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
