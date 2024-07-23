from metafunction.crud import users
from metafunction.database import Session, User, UserCreate, UserUpdate


def test_get_all(session: Session):
    users_list = users.get_all(session)
    assert len(users_list) == 0


def test_get_all_with_users(session: Session, test_user: User):
    users_list = users.get_all(session)
    assert len(users_list) == 1
    assert users_list[0].id == test_user.id


def test_get(session: Session, test_user: User):
    assert test_user.id is not None
    user = users.get(session, test_user.id)
    assert user is not None
    assert user.id == test_user.id


def test_get_not_found(session: Session):
    user = users.get(session, 1)
    assert user is None


def test_create(session: Session):
    user = users.create(
        session,
        UserCreate.model_validate(
            {
                'email': 'test1@example.com',
                'name': 'Test User 1',
                'password': 'password',
            }
        ),
    )
    assert user.id is not None


def test_update(session: Session, test_user: User):
    user = users.update(
        session,
        test_user,
        UserUpdate.model_validate(
            {
                'email': 'test2@example.com',
                'name': 'Test User 2',
            }
        ),
    )
    assert user.email == 'test2@example.com'
    assert user.name == 'Test User 2'


def test_update_by_id(session: Session, test_user: User):
    assert test_user.id is not None
    user = users.update_by_id(
        session,
        test_user.id,
        UserUpdate.model_validate(
            {
                'email': 'test2@example.com',
                'name': 'Test User 2',
            }
        ),
    )
    assert user is not None
    assert user.email == 'test2@example.com'
    assert user.name == 'Test User 2'


def test_update_by_unknown_id(session: Session):
    user = users.update_by_id(
        session,
        1,
        UserUpdate.model_validate(
            {
                'email': 'test2@example.com',
                'name': 'Test User 2',
            }
        ),
    )
    assert user is None


def test_delete(session: Session, test_user: User):
    user = users.delete(session, test_user)
    assert test_user.id is not None
    assert user is not None
    assert user.id == test_user.id
    assert users.get(session, test_user.id) is None


def test_delete_by_id(session: Session, test_user: User):
    assert test_user.id is not None
    user = users.delete_by_id(session, test_user.id)
    assert user is not None
    assert user.id == test_user.id
    assert users.get(session, test_user.id) is None


def test_delete_by_unknown_id(session: Session):
    user = users.delete_by_id(session, 1)
    assert user is None
