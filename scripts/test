#!/bin/bash

# Test database setup
python -c "from iot_sub_svc.database import Database; db = Database('sqlite:////var/lib/iot-sub-svc/test.db'); db.init_db()"

# Test encryption
python -m pytest tests/test_encryption.py -v

# Test config loading
python -m pytest tests/test_config.py -v

# Test MQTT client (requires MQTT broker running)
python -m pytest tests/test_mqtt.py -v

# Test service startup
python run.py --test
