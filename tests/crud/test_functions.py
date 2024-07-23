from metafunction.crud import functions
from metafunction.database import (
    Function,
    FunctionCreate,
    FunctionUpdate,
    Session,
)


def test_get_all(session: Session):
    functions_list = functions.get_all(session)
    assert len(functions_list) == 0


def test_get_all_with_rows(session: Session, test_function: Function):
    functions_list = functions.get_all(session)
    assert len(functions_list) == 1
    assert functions_list[0].id == test_function.id


def test_get(session: Session, test_function: Function):
    assert test_function.id is not None
    function = functions.get(session, test_function.id)
    assert function is not None
    assert function.id == test_function.id


def test_get_not_found(session: Session):
    function = functions.get(session, 1)
    assert function is None


def test_create(session: Session):
    function = functions.create(
        session,
        FunctionCreate.model_validate(
            {
                'name': 'Test function 1',
                'specification': {},
            }
        ),
    )
    assert function.id is not None


def test_update(session: Session, test_function: Function):
    function = functions.update(
        session,
        test_function,
        FunctionUpdate.model_validate(
            {
                'name': 'Test function 2',
                'specification': test_function.specification,
            }
        ),
    )
    assert function.name == 'Test function 2'


def test_update_by_id(session: Session, test_function: Function):
    assert test_function.id is not None
    function = functions.update_by_id(
        session,
        test_function.id,
        FunctionUpdate.model_validate(
            {
                'name': 'Test function 2',
                'specification': test_function.specification,
            }
        ),
    )
    assert function is not None
    assert function.name == 'Test function 2'


def test_update_by_unknown_id(session: Session):
    function = functions.update_by_id(
        session,
        1,
        FunctionUpdate.model_validate(
            {
                'name': 'Test function 2',
                'specification': {},
            }
        ),
    )
    assert function is None


def test_delete(session: Session, test_function: Function):
    function = functions.delete(session, test_function)
    assert test_function.id is not None
    assert function is not None
    assert function.id == test_function.id
    assert functions.get(session, test_function.id) is None


def test_delete_by_id(session: Session, test_function: Function):
    assert test_function.id is not None
    function = functions.delete_by_id(session, test_function.id)
    assert function is not None
    assert function.id == test_function.id
    assert functions.get(session, test_function.id) is None


def test_delete_by_unknown_id(session: Session):
    function = functions.delete_by_id(session, 1)
    assert function is None
