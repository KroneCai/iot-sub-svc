import pytest
import os
from sqlalchemy import inspect
from iot_sub_svc.database import Database
from iot_sub_svc.models import MQTTMessage
import datetime

@pytest.fixture
def test_db(tmp_path):
    db_url = f"sqlite:///{tmp_path}/test.db"
    db = Database(db_url)
    db.init_db()
    yield db
    db.session.close()

def test_table_creation(test_db):
    inspector = inspect(test_db.engine)
    assert 'mqtt_messages' in inspector.get_table_names()
    
    columns = inspector.get_columns('mqtt_messages')
    column_names = [c['name'] for c in columns]
    expected_columns = [
        'id', 'client_id', 'topic', 'original_payload',
        'decrypted_payload', 'mqtt_timestamp', 'qos',
        'retain', 'payload_length', 'message_id', 'system_time'
    ]
    
    for col in expected_columns:
        assert col in column_names

def test_message_insertion(test_db):
    test_msg = MQTTMessage(
        client_id='test_client',
        topic='test/topic',
        original_payload='encrypted_data',
        decrypted_payload='decrypted_data',
        mqtt_timestamp=datetime.datetime.now(),
        qos=1,
        retain=False,
        payload_length=100,
        message_id=12345
    )
    
    test_db.session.add(test_msg)
    test_db.session.commit()
    
    result = test_db.session.query(MQTTMessage).first
