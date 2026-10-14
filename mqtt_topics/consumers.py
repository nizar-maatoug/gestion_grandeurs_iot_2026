from mqttasgi.consumers import MqttConsumer


class MqttTopicsConsumer(MqttConsumer):

    async def connect(self):
        print("Connecting to MQTT broker...")
        try:
            await self.subscribe("sensor/temperature",0)
        except Exception as e:
            print(f"Error occurred while subscribing to topic: {e}")
        print("Subscribed to topic: sensor/temperature")
        

    async def receive(self, mqtt_message):
        print(f"Received MQTT message at topic: {mqtt_message['topic']}")
        print(f"Message payload: {mqtt_message['payload'].decode()}")
        print(f"QoS level: {mqtt_message['qos']}")
        # Send message to room group
        
        

    async def disconnect(self):
        await self.unsubscribe('sensor/temperature')

    
        
              
