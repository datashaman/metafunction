from metafunction.crud import Repository, UserRepository
from metafunction.credentials.models import Credential, CredentialCreate, CredentialUpdate
from metafunction.functions.models import Function, FunctionCreate, FunctionUpdate
from metafunction.users.models import User, UserCreate, UserUpdate


credentials = UserRepository[Credential, CredentialCreate, CredentialUpdate](Credential)
functions = UserRepository[Function, FunctionCreate, FunctionUpdate](Function)
users = Repository[User, UserCreate, UserUpdate](User)
