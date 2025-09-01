import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Location
from bus.models import BusRoute, Assignment
from users.models import User
from bus.notifications import notify_users_on_bus_active


class LiveTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.route_number = self.scope['url_route']['kwargs']['route_number']
        self.room_group_name = f'live_tracking_{self.route_number}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send initial locations
        locations = await self.get_locations_for_route(self.route_number)
        await self.send(text_data=json.dumps({
            'type': 'initial_locations',
            'locations': locations
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        pass

    async def location_update(self, event):
        # Send location update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'location': event['location']
        }))

    @database_sync_to_async
    def get_locations_for_route(self, route_number):
        locations = Location.objects.filter(bus_route__route_number=route_number).order_by('-timestamp')[:10]
        return [{
            'id': loc.id,
            'driver': loc.driver.full_name,
            'driver_id': loc.driver.id,
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'timestamp': loc.timestamp.isoformat(),
            'bus_route': loc.bus_route.route_number
        } for loc in locations]


class DriverLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.driver_id = self.scope['url_route']['kwargs']['driver_id']
        self.room_group_name = f'driver_location_{self.driver_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming location updates from driver
        data = json.loads(text_data)
        if data['type'] == 'location_update':
            await self.update_location(data['location'])

    async def location_broadcast(self, event):
        # Send location to driver's WebSocket
        await self.send(text_data=json.dumps({
            'type': 'location_broadcast',
            'location': event['location']
        }))

    @database_sync_to_async
    def update_location(self, location_data):
        try:
            driver = User.objects.get(id=self.driver_id)
            bus_route = BusRoute.objects.get(route_number=location_data['bus_route'])
            
            location = Location(
                driver=driver,
                bus_route=bus_route,
                latitude=location_data['latitude'],
                longitude=location_data['longitude']
            )
            location.save()

            # Send notification to users on this route
            eta = 'N/A'  # Placeholder, can be enhanced with ETA calculation
            notify_users_on_bus_active(bus_route.route_number, eta, driver)
            
            # Broadcast to live tracking group
            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()
            
            async def broadcast():
                await channel_layer.group_send(
                    f'live_tracking_{bus_route.route_number}',
                    {
                        'type': 'location_update',
                        'location': {
                            'id': location.id,
                            'driver': driver.full_name,
                            'driver_id': driver.id,
                            'latitude': location.latitude,
                            'longitude': location.longitude,
                            'timestamp': location.timestamp.isoformat(),
                            'bus_route': bus_route.route_number
                        }
                    }
                )
            
            import asyncio
            asyncio.create_task(broadcast())
            
        except Exception as e:
            print(f"Error updating location: {e}")
