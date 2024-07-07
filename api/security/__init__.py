from cryptography.fernet import Fernet
from api.settings import SECRET_KEY


crypt = Fernet(SECRET_KEY.encode())
