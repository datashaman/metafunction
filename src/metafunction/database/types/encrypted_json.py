import base64
import json
from typing import Any, Optional

from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.types import String, TypeDecorator

from metafunction.security import crypt

JSONDict = MutableDict[str, Any]


class EncryptedJSON(TypeDecorator[Optional[JSONDict]]):
    impl = String

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return None
        value_str = json.dumps(value)
        encrypted_value = crypt.encrypt(value_str.encode('utf-8'))
        return base64.b64encode(encrypted_value).decode('utf-8')

    def process_result_value(self, value: Optional[str], dialect: Dialect) -> Optional[JSONDict]:
        if value is None:
            return None
        encrypted_value = base64.b64decode(value.encode('utf-8'))
        decrypted_value = crypt.decrypt(encrypted_value).decode('utf-8')
        return MutableDict(**json.loads(decrypted_value))

    def copy_value(self, value: Any) -> Optional[JSONDict]:
        return MutableDict.coerce(value, self.impl)
