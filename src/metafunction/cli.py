import typer
from cryptography.fernet import Fernet
from typing_extensions import Annotated

try:
    from metafunction._version import version
except ImportError:
    version = 'dev'

from metafunction.credentials.models import CredentialType
from metafunction.database import get_session, select
from metafunction.users.models import User


def version_callback(*, value: bool) -> None:
    if value:
        typer.echo(version)
        raise typer.Exit()


app = typer.Typer()


@app.command()
def create_user(name: str, email: str, password: str, *, is_admin: bool = False) -> None:
    session = next(get_session())
    user = User(name=name, email=email, password=password, is_admin=is_admin)
    session.add(user)
    session.commit()
    typer.echo(f'User {name} created')


@app.command()
def list_users() -> None:
    session = next(get_session())
    users = session.exec(select(User).order_by(User.name)).all()
    for user in users:
        typer.echo(f'{user.name} - {user.email}')


@app.command()
def generate_key() -> None:
    key = Fernet.generate_key()
    typer.echo(key.decode())


@app.command()
def seed_data() -> None:
    session = next(get_session())
    credential_types = [
        CredentialType(id='token', name='API Key / Token'),
        CredentialType(id='basic', name='Basic Auth'),
        CredentialType(id='oauth', name='OAuth Token'),
    ]
    session.add_all(credential_types)
    session.commit()


@app.callback()
def main(
    version: Annotated[bool, 'Show the version and exit'] = typer.Option(None, '--version', callback=version_callback),
):
    if version:
        raise typer.Exit()


if __name__ == '__main__':
    app()
