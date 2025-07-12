from Crypto.Cipher import AES
import base64
from config import Config

class AESCipher:
    def __init__(self, key=None, iv=None):
        cfg = Config()
        self.key = key or cfg.aes_key.encode('utf-8')
        self.iv = iv or cfg.aes_iv.encode('utf-8')
        self.block_size = AES.block_size

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = cipher.decrypt(base64.b64decode(enc))
        return self._unpad(dec).decode('utf-8')

    def _unpad(self, s):
        return s.rstrip(b'\x00')
