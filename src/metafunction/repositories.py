from typing import Generic, List, Optional, TypeVar

from sqlmodel import SQLModel
from sqlmodel.main import SQLModelMetaclass

from metafunction.credentials.models import Credential, CredentialCreate, CredentialUpdate
from metafunction.database import Session, select
from metafunction.functions.models import Function, FunctionCreate, FunctionUpdate
from metafunction.users.models import User, UserCreate, UserUpdate

T = TypeVar('T', bound=SQLModel)
TCreate = TypeVar('TCreate', bound=SQLModel)
TUpdate = TypeVar('TUpdate', bound=SQLModel)


class Repository(Generic[T, TCreate, TUpdate]):
    def __init__(self, model: SQLModelMetaclass):
        self.model = model

    def get_all(
        self,
        session: Session,
        user: User,
        offset: int = 0,
        limit: int = 10,
    ) -> List[T]:
        return list(session.exec(self.base_query(session, user).offset(offset).limit(limit)).all())

    def get(
        self,
        session: Session,
        user: User,
        model_id: int,
    ) -> Optional[T]:
        return session.exec(self.base_query(session, user).where(self.model.id == model_id)).first()

    def get_by_name(
        self,
        session: Session,
        user: User,
        name: str,
    ) -> Optional[T]:
        return session.exec(self.base_query(session, user).where(self.model.name == name)).first()

    def create(
        self,
        session: Session,
        user: User,
        data: TCreate,
    ) -> T:
        model = self.model.model_validate(self.prepare_data(user, data))
        session.add(model)
        session.commit()
        session.refresh(model)
        return model

    def update(
        self,
        session: Session,
        user: User,
        model: T,
        data: TUpdate,
    ) -> T:
        for key, value in data.model_dump().items():
            setattr(model, key, value)
        session.commit()
        session.refresh(model)
        return model

    def update_by_id(
        self,
        session: Session,
        user: User,
        model_id: int,
        data: TUpdate,
    ) -> Optional[T]:
        if model := self.get(session, user, model_id):
            return self.update(session, user, model, data)
        return None

    def delete(self, session: Session, user: User, model: T) -> T:
        session.delete(model)
        session.commit()
        return model

    def delete_by_id(self, session: Session, user: User, model_id: int) -> Optional[T]:
        if model := self.get(session, user, model_id):
            return self.delete(session, user, model)
        return None

    def base_query(self, session: Session, user: Optional[User] = None):
        return select(self.model)

    def prepare_data(self, user: User, data: TCreate) -> dict:
        return data.model_dump()


class UserRepository(Repository[T, TCreate, TUpdate]):
    def update(
        self,
        session: Session,
        user: User,
        model: T,
        data: TUpdate,
    ) -> T:
        self.check_user(user, model)
        return super().update(session, user, model, data)

    def delete(self, session: Session, user: User, model: T) -> T:
        self.check_user(user, model)
        return super().delete(session, user, model)

    def base_query(self, session: Session, user: Optional[User] = None):
        return super().base_query(session, user).where(self.model.user_id == user.id)

    def check_user(self, user: User, model: T):
        if model.user_id != user.id:
            msg = 'Model does not belong to user'
            raise ValueError(msg)

    def prepare_data(self, user: User, data: TCreate) -> dict:
        dump = super().prepare_data(user, data)
        dump['user_id'] = user.id
        return dump


credentials = UserRepository[Credential, CredentialCreate, CredentialUpdate](Credential)
functions = UserRepository[Function, FunctionCreate, FunctionUpdate](Function)
users = Repository[User, UserCreate, UserUpdate](User)
