from sqlalchemy.types import TypeDecorator, String
from cryptography.fernet import Fernet
from decouple import config
import base64

# Load the encryption key from the environment variable
key = config('SECRET_KEY').encode()
cipher_suite = Fernet(key)

class EncryptedType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            encrypted_value = cipher_suite.encrypt(value.encode('utf-8'))
            return base64.b64encode(encrypted_value).decode('utf-8')
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            encrypted_value = base64.b64decode(value.encode('utf-8'))
            return cipher_suite.decrypt(encrypted_value).decode('utf-8')
        return value
