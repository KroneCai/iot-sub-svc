import pytest
import paho.mqtt.client as mqtt
import time
import json
from iot_sub_svc.mqtt_client import MQTTSubscriber
from iot_sub_svc.config import Config
from iot_sub_svc.encryption import AESCipher

@pytest.fixture
def test_config():
    config = Config()
    config.mqtt_host = "test.mosquitto.org"
    config.mqtt_port = 1883
    config.mqtt_topics = ["iot-sub-svc-test"]
    return config

def test_mqtt_connection(test_config):
    subscriber = MQTTSubscriber(test_config)
    
    connected = False
    def on_connect(client, userdata, flags, rc):
        nonlocal connected
        connected = True
    
    subscriber.client.on_connect = on_connect
    subscriber.start()
    
    # Wait for connection
    time.sleep(2)
    assert connected is True

def test_message_reception(test_config):
    test_messages = []
    
    def callback(msg):
        test_messages.append(msg)
    
    # Setup subscriber
    subscriber = MQTTSubscriber(test_config)
    subscriber.add_callback(callback)
    subscriber.start()
    
    # Wait for connection
    time.sleep(1)
    
    # Publish test message
    cipher = AESCipher(test_config.aes_key, test_config.aes_iv)
    test_payload = cipher.encrypt(json.dumps({"test": "value"}))
    
    publisher = mqtt.Client()
    publisher.connect(test_config.mqtt_host, test_config.mqtt_port)
    publisher.publish(test_config.mqtt_topics[0], test_payload)
    publisher.disconnect()
    
    # Wait for message
    time.sleep(2)
    
    assert len(test_messages) > 0
    assert test_messages[0]['topic'] == test_config.mqtt_topics[0]
