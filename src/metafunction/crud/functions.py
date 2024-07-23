from typing import List, Optional

from metafunction.database import (
    Function,
    FunctionCreate,
    FunctionUpdate,
    Session,
    User,
    select,
)


def get_all(
    session: Session,
    user: User,
    offset: int = 0,
    limit: int = 10,
) -> List[Function]:
    return list(session.exec(select(Function).where(Function.user_id == user.id).offset(offset).limit(limit)).all())


def get(
    session: Session,
    user: User,
    function_id: int,
) -> Optional[Function]:
    return session.exec(select(Function).where(Function.user_id == user.id).where(Function.id == function_id)).first()


def get_by_name(
    session: Session,
    user: User,
    name: str,
) -> Optional[Function]:
    return session.exec(select(Function).where(Function.user_id == user.id).where(Function.name == name)).first()


def create(
    session: Session,
    user: User,
    data: FunctionCreate,
) -> Function:
    dump = data.model_dump()
    dump['user_id'] = user.id
    function = Function.model_validate(dump)
    session.add(function)
    session.commit()
    session.refresh(function)
    return function


def update(
    session: Session,
    user: User,
    function: Function,
    data: FunctionUpdate,
) -> Function:
    if function.user_id != user.id:
        msg = 'Function does not belong to user'
        raise ValueError(msg)

    for key, value in data.model_dump().items():
        setattr(function, key, value)
    session.commit()
    session.refresh(function)
    return function


def update_by_id(
    session: Session,
    user: User,
    function_id: int,
    data: FunctionUpdate,
) -> Optional[Function]:
    if function := get(session, user, function_id):
        return update(session, user, function, data)
    return None


def delete(
    session: Session,
    user: User,
    function: Function,
) -> Function:
    if function.user_id != user.id:
        msg = 'Function does not belong to user'
        raise ValueError(msg)

    session.delete(function)
    session.commit()
    return function


def delete_by_id(
    session: Session,
    user: User,
    function_id: int,
) -> Optional[Function]:
    if function := get(session, user, function_id):
        return delete(session, user, function)
    return None
