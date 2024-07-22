from typing import List, Optional

from metafunction.database import Session, User, UserCreate, UserUpdate, select


def get_all(session: Session, offset: int = 0, limit: int = 10) -> List[User]:
    return list(session.exec(select(User).offset(offset).limit(limit)).all())


def get(session: Session, user_id: int) -> Optional[User]:
    return session.exec(select(User).where(User.id == user_id)).first()


def get_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def create(session: Session, data: UserCreate) -> User:
    user = User.model_validate(data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update(session: Session, user: User, data: UserUpdate) -> User:
    for key, value in data.model_dump().items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


def update_by_id(session: Session, user_id: int, data: UserUpdate) -> Optional[User]:
    user = get(session, user_id)
    if user:
        return update(session, user, data)
    return None


def delete(session: Session, user: User) -> User:
    session.delete(user)
    session.commit()
    return user


def delete_by_id(session: Session, user_id: int) -> Optional[User]:
    if user := get(session, user_id):
        return delete(session, user)
    return user
