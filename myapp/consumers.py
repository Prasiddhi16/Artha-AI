import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            # Create a group name unique to this user
            self.group_name = f"notifications_{user.id}"

            # Add this connection to the user-specific group
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            # Reject connection if not logged in
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # 👇 This must be indented inside the class
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "type": event.get("notification_type", "info"),
        }))