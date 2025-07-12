#!/bin/bash

# Install prerequisites
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git

# Create project directory
sudo mkdir -p /srv/iot-sub-svc
sudo chown $(whoami):$(whoami) /srv/iot-sub-svc
cd /srv/iot-sub-svc

# Clone repository
git clone https://github.com/KroneCai/iot-sub-svc.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create config directory
# 新增配置目录创建和权限设置
sudo mkdir -p /etc/iot-sub-svc/
sudo cp $PROJECT_DIR/iot-sub-svc.conf /etc/iot-sub-svc/
sudo chown root:root /etc/iot-sub-svc/iot-sub-svc.conf
sudo chmod 644 /etc/iot-sub-svc/iot-sub-svc.conf

# Create database directory
sudo mkdir -p /var/lib/iot-sub-svc
sudo chown $(whoami):$(whoami) /var/lib/iot-sub-svc

# Create log file
sudo touch /var/log/iot_sub_svc.log
sudo chown $(whoami):$(whoami) /var/log/iot_sub_svc.log

# Create systemd service
sudo tee /etc/systemd/system/iot-sub-svc.service <<EOF
[Unit]
Description=IoT MQTT Subscription Service
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=/srv/iot-sub-svc
Environment="PATH=/srv/iot-sub-svc/venv/bin"
ExecStart=/srv/iot-sub-svc/venv/bin/python /srv/iot-sub-svc/run.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload and enable service
sudo systemctl daemon-reload
sudo systemctl enable iot-sub-svc.service
sudo systemctl start iot-sub-svc.service

echo "Deployment completed!"
