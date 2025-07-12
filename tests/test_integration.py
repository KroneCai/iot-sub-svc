import pytest
import time
import json
import paho.mqtt.client as mqtt
from iot_sub_svc.service import Service
from iot_sub_svc.database import Database
from iot_sub_svc.config import Config
import tempfile

@pytest.fixture
def test_service(tmp_path):
    # Create temp config
    config_path = tmp_path / "test_config.conf"
    
    config = configparser.ConfigParser()
    config['mqtt'] = {
        'host': 'test.mosquitto.org',
        'port': '1883',
        'client_id': 'integration_test',
        'topics': 'iot-sub-svc/integration-test'
    }
    config['database'] = {'url': f'sqlite:///{tmp_path}/integration.db'}
    config['logging'] = {'log_file': f'{tmp_path}/integration.log', 'level': 'DEBUG'}
    config['security'] = {'aes_key': 'INTEGRATIONKEY123', 'aes_iv': 'INTEGRATIONIV123'}
    
    with open(config_path, 'w') as f:
        config.write(f)
    
    # Override config path
    service = Service()
    service.cfg = Config()
    service.cfg._load_config = lambda: config.read(config_path)
    
    yield service
    service.stop()

def test_end_to_end_flow(test_service, tmp_path):
    received_messages = []
    
    def callback(msg):
        received_messages.append(msg)
    
    test_service.add_message_callback(callback)
    test_service.start()
    
    # Wait for service to connect
    time.sleep(2)
    
    # Publish test message
    test_payload = {
        "sensor": "integration_test",
        "value": 42,
        "timestamp": int(time.time())
    }
    
    cipher = AESCipher('INTEGRATIONKEY123', 'INTEGRATIONIV123')
    encrypted = cipher.encrypt(json.dumps(test_payload))
    
    pub_client = mqtt.Client()
    pub_client.connect('test.mosquitto.org', 1883)
    pub_client.publish('iot-sub-svc/integration-test', encrypted)
    pub_client.disconnect()
    
    # Wait for message processing
    time.sleep(3)
    
    # Verify message was received and stored
    assert len(received_messages) == 1
    assert received_messages[0]['topic'] == 'iot-sub-svc/integration-test'
    
    # Verify database entry
    db = Database(f'sqlite:///{tmp_path}/integration.db')
    msg = db.session.query(MQTTMessage).first()
    assert msg is not None
    assert msg.topic == 'iot-sub-svc/integration-test'
    assert 'integration_test' in msg.decrypted_payload
