import signal
import sys
import time
import logging
from typing import Optional, Callable
from mqtt_client import MQTTSubscriber
from config import Config
from utils import setup_logging

logger = logging.getLogger(__name__)

class Service:
    def __init__(self):
        setup_logging()
        self.cfg = Config()
        self.subscriber: Optional[MQTTSubscriber] = None
        self.running = False
        
    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
        
    def add_message_callback(self, callback: Callable):
        if self.subscriber:
            self.subscriber.add_callback(callback)
        
    def start(self):
        try:
            # Register signal handlers
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            # Initialize database
            from database import Database
            db = Database()
            db.init_db()
            
            # Create and start MQTT subscriber
            self.subscriber = MQTTSubscriber(self.cfg)
            self.subscriber.start()
            
            self.running = True
            logger.info("Service started successfully")
            
            # Main loop
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Service startup failed: {str(e)}")
            raise
            
    def stop(self):
        if self.subscriber:
            self.subscriber.stop()
        self.running = False
        logger.info("Service stopped")
