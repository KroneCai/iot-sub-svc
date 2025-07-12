import pytest
import os
import configparser
from iot_sub_svc.config import Config

@pytest.fixture
def create_test_config(tmp_path):
    config_path = tmp_path / "test_config.conf"
    
    config = configparser.ConfigParser()
    config['mqtt'] = {
        'host': 'test.mqtt.server',
        'port': '1883',
        'username': 'test_user',
        'password': 'test_pass',
        'client_id': 'test_client',
        'topics': 'topic1, topic2'
    }
    
    config['database'] = {'url': 'sqlite:///test.db'}
    config['logging'] = {'log_file': '/tmp/test.log', 'level': 'DEBUG'}
    config['security'] = {'aes_key': 'TESTKEY123456789', 'aes_iv': 'TESTIV123456789'}
    
    with open(config_path, 'w') as f:
        config.write(f)
    
    return config_path

def test_config_loading(create_test_config, monkeypatch):
    monkeypatch.setenv('IOT_CONFIG_PATH', str(create_test_config))
    
    cfg = Config()
    
    assert cfg.mqtt_host == 'test.mqtt.server'
    assert cfg.mqtt_port == 1883
    assert cfg.mqtt_username == 'test_user'
    assert cfg.mqtt_password == 'test_pass'
    assert cfg.mqtt_client_id == 'test_client'
    assert cfg.mqtt_topics == ['topic1', 'topic2']
    assert cfg.db_url == 'sqlite:///test.db'
    assert cfg.log_file == '/tmp/test.log'
    assert cfg.log_level == 'DEBUG'
    assert cfg.aes_key == 'TESTKEY123456789'
    assert cfg.aes_iv == 'TESTIV123456789'

def test_default_values(tmp_path, monkeypatch):
    config_path = tmp_path / "empty_config.conf"
    config_path.touch()
    monkeypatch.setenv('IOT_CONFIG_PATH', str(config_path))
    
    cfg = Config()
    
    assert cfg.mqtt_host == '114.92.179.98'
    assert cfg.mqtt_port == 1883
    assert cfg.mqtt_username == 'riot_pub_dev'
    assert cfg.mqtt_password == 'rent@kil2025'
    assert cfg.db_url == 'sqlite:////var/lib/iot-sub-svc/messages.db'
    assert cfg.log_file == '/var/log/iot_sub_svc.log'
