import pytest
from iot_sub_svc.encryption import AESCipher
from iot_sub_svc.config import Config
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

@pytest.fixture
def cipher():
    cfg = Config()
    return AESCipher(cfg.aes_key, cfg.aes_iv)

def test_aes_decryption(cipher):
    # Test data
    original_data = '{"sensor": "temperature", "value": 23.5}'
    
    # Manually encrypt
    aes = AES.new(cipher.key, AES.MODE_CBC, cipher.iv)
    encrypted = aes.encrypt(pad(original_data.encode('utf-8'), AES.block_size))
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
    
    # Test decryption
    decrypted = cipher.decrypt(encrypted_b64)
    assert decrypted == original_data

def test_invalid_input(cipher):
    with pytest.raises(Exception):
        cipher.decrypt('invalid_base64')
    
    with pytest.raises(Exception):
        cipher.decrypt(base64.b64encode(b'short').decode('utf-8'))

def test_different_padding(cipher):
    # Test with zero padding (as per requirements)
    data = 'test' * 10
    aes = AES.new(cipher.key, AES.MODE_CBC, cipher.iv)
    padded = data.encode('utf-8') + b'\x00' * (AES.block_size - len(data) % AES.block_size)
    encrypted = base
