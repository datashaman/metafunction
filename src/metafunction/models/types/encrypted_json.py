import base64
import json
from typing import Any, Optional

from cryptography.fernet import Fernet
from sqlalchemy import JSON
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.types import TypeDecorator, String

from metafunction.security import crypt


class EncryptedJSON(TypeDecorator[Optional[MutableDict[str, Any]]]):
    impl = String

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is not None:
            value_str = json.dumps(value)
            encrypted_value = crypt.encrypt(value_str.encode("utf-8"))
            return base64.b64encode(encrypted_value).decode("utf-8")
        return None

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[MutableDict[str, Any]]:
        if value is not None:
            encrypted_value = base64.b64decode(value.encode("utf-8"))
            decrypted_value = crypt.decrypt(encrypted_value).decode("utf-8")
            return MutableDict(**json.loads(decrypted_value))
        return None

    def copy_value(self, value: Any) -> Optional[MutableDict[str, Any]]:
        return MutableDict.coerce(value, self.impl)
