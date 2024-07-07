from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator, String
from typing import Any, Optional
from cryptography.fernet import Fernet
import base64

from metafunction.security import crypt


class EncryptedType(TypeDecorator):
    impl = String

    def process_bind_param(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[str]:
        if value is not None:
            encrypted_value = crypt.encrypt(value.encode("utf-8"))
            return base64.b64encode(encrypted_value).decode("utf-8")
        return value

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[str]:
        if value is not None:
            encrypted_value = base64.b64decode(value.encode("utf-8"))
            return crypt.decrypt(encrypted_value).decode("utf-8")
        return value
