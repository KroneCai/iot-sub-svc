#!/usr/bin/env python
import logging
from iot_sub_svc.config import Config
from iot_sub_svc.mqtt_client import MQTTSubscriber
from iot_sub_svc.database import Database
import argparse
import sys

def setup_logging(config):
    logging.basicConfig(
        level=config.log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()

    config = Config()
    setup_logging(config)

    if args.test:
        print("Running in test mode...")
        db = Database(config.db_url)
        db.init_db()
        print("Database initialized successfully!")
        return

    try:
        subscriber = MQTTSubscriber(config)
        subscriber.start()
        logging.info("Service started successfully")
        
        # Keep the service running
        while True:
            pass
    except KeyboardInterrupt:
        subscriber.stop()
        logging.info("Service stopped")
    except Exception as e:
        logging.error(f"Service failed: {str(e)}")
        raise

if __name__ == '__main__':
    main()
