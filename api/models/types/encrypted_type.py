from sqlalchemy.types import TypeDecorator, String
from cryptography.fernet import Fernet
import base64

from api.security import crypt

class EncryptedType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            encrypted_value = crypt.encrypt(value.encode('utf-8'))
            return base64.b64encode(encrypted_value).decode('utf-8')
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            encrypted_value = base64.b64decode(value.encode('utf-8'))
            return crypt.decrypt(encrypted_value).decode('utf-8')
        return value
