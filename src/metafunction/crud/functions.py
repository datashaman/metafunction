from typing import List, Optional

from metafunction.database import (
    Function,
    FunctionCreate,
    FunctionUpdate,
    Session,
    select,
)


def get_all(session: Session, offset: int = 0, limit: int = 10) -> List[Function]:
    return list(session.exec(select(Function).offset(offset).limit(limit)).all())


def get(session: Session, function_id: int) -> Optional[Function]:
    return session.exec(select(Function).where(Function.id == function_id)).first()


def get_by_name(session: Session, name: str) -> Optional[Function]:
    return session.exec(select(Function).where(Function.name == name)).first()


def create(session: Session, data: FunctionCreate) -> Function:
    function = Function.model_validate(data)
    session.add(function)
    session.commit()
    session.refresh(function)
    return function


def update(session: Session, function: Function, data: FunctionUpdate) -> Function:
    for key, value in data.model_dump().items():
        setattr(function, key, value)
    session.commit()
    session.refresh(function)
    return function


def update_by_id(session: Session, function_id: int, data: FunctionUpdate) -> Optional[Function]:
    if function := get(session, function_id):
        return update(session, function, data)
    return None


def delete(session: Session, function: Function) -> Function:
    session.delete(function)
    session.commit()
    return function


def delete_by_id(session: Session, function_id: int) -> Optional[Function]:
    if function := get(session, function_id):
        return delete(session, function)
    return None
