from cryptography.fernet import Fernet
from metafunction.settings import SECRET_KEY


crypt = Fernet(SECRET_KEY.encode())
