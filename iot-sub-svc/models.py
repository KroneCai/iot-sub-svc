from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class MQTTMessage(Base):
    __tablename__ = 'mqtt_messages'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(String(100))
    topic = Column(String(255))
    original_payload = Column(String)
    decrypted_payload = Column(String)
    mqtt_timestamp = Column(DateTime)
    qos = Column(Integer)
    retain = Column(Boolean)
    payload_length = Column(Integer)
    message_id = Column(Integer)
    system_time = Column(DateTime, default=datetime.datetime.utcnow)
