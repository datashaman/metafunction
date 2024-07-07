from sqlalchemy.types import TypeDecorator, String
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import JSON
from cryptography.fernet import Fernet
import base64
import json

from api.security import crypt


class EncryptedJSON(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value_str = json.dumps(value)
            encrypted_value = crypt.encrypt(value_str.encode("utf-8"))
            return base64.b64encode(encrypted_value).decode("utf-8")
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            encrypted_value = base64.b64decode(value.encode("utf-8"))
            decrypted_value = crypt.decrypt(encrypted_value).decode("utf-8")
            return json.loads(decrypted_value)
        return value

    def copy_value(self, value):
        return MutableDict.coerce(value, self.impl)
