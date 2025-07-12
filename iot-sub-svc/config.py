import configparser
import os
from typing import List, Optional

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        # 优先级: 环境变量 > 生产路径 > 开发路径
        config_path = os.getenv('IOT_CONFIG_PATH') or \
                     '/etc/iot-sub-svc/iot-sub-svc.conf' if os.path.exists('/etc/iot-sub-svc/iot-sub-svc.conf') else \
                     os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'iot-sub-svc.conf')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")
        
        # 新增配置文件变更自动重载
        self._config_mtime = os.path.getmtime(config_path)
        config = configparser.ConfigParser()
        config.read(config_path)
        
        # MQTT Configuration
        self.mqtt_host = config.get('mqtt', 'host', fallback='114.92.179.98')
        self.mqtt_port = config.getint('mqtt', 'port', fallback=1883)
        self.mqtt_username = config.get('mqtt', 'username', fallback='riot_pub_dev')
        self.mqtt_password = config.get('mqtt', 'password', fallback='rent@kil2025')
        self.mqtt_client_id = config.get('mqtt', 'client_id', fallback='iot_sub_client_1')
        
        # Handle topics (empty string means subscribe to all with '#')
        topics_str = config.get('mqtt', 'topics', fallback='')
        self.mqtt_topics: List[str] = [t.strip() for t in topics_str.split(',') if t.strip()] if topics_str else []
        
        # Database Configuration
        self.db_url = config.get('database', 'url', fallback='sqlite:////var/lib/iot-sub-svc/messages.db')
        
        # Logging Configuration
        self.log_file = config.get('logging', 'log_file', fallback='/var/log/iot_sub_svc.log')
        self.log_level = config.get('logging', 'level', fallback='INFO')
        
        # Security Configuration
        self.aes_key = config.get('security', 'aes_key', fallback='AQRTYUOIFSRBFCEG')
        self.aes_iv = config.get('security', 'aes_iv', fallback='AQRTYUOIFSRBFCEG')
