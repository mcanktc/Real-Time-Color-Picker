from channels.generic.websocket import AsyncJsonWebsocketConsumer
import re
import asyncio

HEX_PATTERN = re.compile(r"^#([A-Fa-f0-9]{6})$")
RGB_PATTERN = re.compile(r"^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$")

class ColorConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room = self.scope["url_route"]["kwargs"].get("room_id", "default")
        self.group = f"color_{self.room}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        color = content.get("color")
        if not color:
            return
        
        if HEX_PATTERN.match(color):
            normalized = color.upper()

        elif RGB_PATTERN.match(color):
            r, g, b = map(int, RGB_PATTERN.match(color).groups())
            if any(x>255 for x in (r, g, b)):
                return
            
            normalized = f"#{r:02X}{g:02X}{b:02X}"
        
        else:
            return
        
        await asyncio.sleep(0.02)

        await self.channel_layer.group_send(
            self.group,
            {
                "type" : "color.update",
                "color" : normalized
            }
        )


    async def color_update(self, event):
        await self.send_json({"color" : event["color"]})

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)
        return await super().disconnect(code)