import paho.mqtt.client as mqtt
from database import Database
from encryption import AESCipher
import logging
from models import MQTTMessage
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class MQTTSubscriber:
    def __init__(self, config):
        # 新增重试配置
        self.max_retries = 3  # 最大重试次数
        self.retry_delay = 5  # 初始重试延迟(秒)
        self.retry_backoff = 2  # 重试延迟倍数
        self.current_retry = 0

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.current_retry = 0  # 重置重试计数器
            logger.info("Connected to MQTT Broker!")
            self.config = config
            self.client = mqtt.Client(client_id=config.mqtt_client_id)
            self.client.username_pw_set(config.mqtt_username, config.mqtt_password)
            self.db = Database(config.db_url)
            self.cipher = AESCipher()
            self.callbacks = []

        def add_callback(self, callback):
            self.callbacks.append(callback)

        def on_connect(self, client, userdata, flags, rc):
            if rc == 0:
                self.current_retry = 0  # 重置重试计数器
                logger.info("Connected to MQTT Broker!")
                topics = self.config.mqtt_topics or ['#']
                for topic in topics:
                    client.subscribe(topic.strip())
                    logger.info(f"Subscribed to topic: {topic}")
            else:
                self.current_retry += 1
                if self.current_retry <= self.max_retries:
                    delay = self.retry_delay * (self.retry_backoff ** (self.current_retry-1))
                    logger.error(f"Failed to connect (attempt {self.current_retry}/{self.max_retries}), retrying in {delay} seconds...")
                    time.sleep(delay)
                    try:
                        client.reconnect()
                    except Exception as e:
                        logger.error(f"Reconnect failed: {str(e)}")
                else:
                    logger.critical(f"Max retries ({self.max_retries}) exceeded. Giving up.")
                    # 可添加优雅降级逻辑

    def on_message(self, client, userdata, msg):
        try:
            logger.debug(f"Received message on topic {msg.topic}, QoS: {msg.qos}, Length: {len(msg.payload)}")
            
            mqtt_msg = {
                'client_id': self.config.mqtt_client_id,
                'topic': msg.topic,
                'original_payload': str(msg.payload),
                'decrypted_payload': self.cipher.decrypt(msg.payload),
                'mqtt_timestamp': datetime.now(),
                'qos': msg.qos,
                'retain': msg.retain,
                'payload_length': len(msg.payload),
                'message_id': msg.mid
            }
            
            # Save to database
            try:
                db_message = MQTTMessage(**mqtt_msg)
                self.db.session.add(db_message)
                self.db.session.commit()
                logger.debug(f"Message saved to database, ID: {db_message.id}")
            except Exception as db_error:
                logger.error(f"Database error: {str(db_error)}")
                logger.debug(f"Failed message details: {mqtt_msg}")
                self.db.session.rollback()
            
            # Execute callbacks
            for callback in self.callbacks:
                try:
                    callback(mqtt_msg)
                except Exception as cb_error:
                    logger.error(f"Callback error: {str(cb_error)}")
                    
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            logger.debug(f"Raw message payload: {msg.payload}")

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.config.mqtt_host, self.config.mqtt_port)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.db.session.close()
