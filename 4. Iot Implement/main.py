import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT endpoint and credentials
endpoint = "your-iot-endpoint.amazonaws.com"
rootCAPath = "path/to/rootCA.pem"
certificatePath = "path/to/certificate.pem.crt"
privateKeyPath = "path/to/private.pem.key"

# MQTT topic to subscribe and publish
topic = "your/topic"

# Callback function when message is received
def on_message(client, userdata, message):
    print("Received message:", message.payload)

# Create MQTT client
client = AWSIoTMQTTClient("myClientID")
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# Configure MQTT client connection
client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 seconds
client.configureMQTTOperationTimeout(5)  # 5 seconds

# Connect to AWS IoT
client.connect()

# Subscribe to MQTT topic
client.subscribe(topic, 1, on_message)

# Loop forever and publish sensor values
while True:
    sensor_value = read_sensor()  # Replace with your sensor reading code
    client.publish(topic, str(sensor_value), 1)
    time.sleep(1)
