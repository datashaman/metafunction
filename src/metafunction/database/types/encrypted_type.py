import base64
from typing import Optional

from sqlalchemy.engine import Dialect
from sqlalchemy.types import String, TypeDecorator

from metafunction.security import crypt


class EncryptedType(TypeDecorator[Optional[str]]):
    impl = String

    def process_bind_param(self, value: Optional[str], dialect: Dialect) -> Optional[str]:
        if value is None:
            return None
        encrypted_value = crypt.encrypt(value.encode('utf-8'))
        return base64.b64encode(encrypted_value).decode('utf-8')

    def process_result_value(self, value: Optional[str], dialect: Dialect) -> Optional[str]:
        if value is None:
            return None
        encrypted_value = base64.b64decode(value.encode('utf-8'))
        return crypt.decrypt(encrypted_value).decode('utf-8')
