#!/bin/bash

# Initialize the virtual environment
source /srv/iot-sub-svc/venv/bin/activate

# Initialize the database
python -c "from iot_sub_svc.database import Database; db = Database(); db.init_db()"

# Set proper permissions
sudo chown -R iot-sub-svc:iot-sub-svc /var/lib/iot-sub-svc
sudo chown -R iot-sub-svc:iot-sub-svc /var/log/iot_sub_svc.log
sudo chown -R iot-sub-svc:iot-sub-svc /etc/iot-sub-svc

# Reload systemd
sudo systemctl daemon-reload

echo "Post-deployment tasks completed"
