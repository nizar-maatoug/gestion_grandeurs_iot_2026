from mqttasgi.consumers import MqttConsumer


class MqttTopicsConsumer(MqttConsumer):

    async def connect(self):
        print("Connecting to MQTT broker...")
        await self.subscribe("sensor/temperature",qos=0)
        print("Subscribed to topic: sensor/temperature")

    async def receive(self, mqtt_message):
        print(f"Received MQTT message at topic: {mqtt_message['topic']}")
        print(f"Message payload: {mqtt_message['payload'].decode()}")
        print(f"QoS level: {mqtt_message['qos']}")

    async def disconnect(self):
        await self.unsubscribe("sensor/temperature")
              
