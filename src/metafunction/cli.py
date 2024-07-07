import typer
from cryptography.fernet import Fernet

from metafunction.models import (
    create_tables,
    get_session,
    Session,
    CredentialType,
    User,
)


app = typer.Typer()


@app.command()
def create_user(name: str, email: str, password: str, is_admin: bool = False):
    session = next(get_session())
    user = User(name=name, email=email, password=password, is_admin=is_admin)
    session.add(user)
    session.commit()
    typer.echo(f"User {name} created")


@app.command()
def generate_key():
    key = Fernet.generate_key()
    typer.echo(key.decode())


@app.command()
def seed_data():
    session = next(get_session())

    credential_types = [
        CredentialType(name="API Key"),
        CredentialType(name="Basic Auth"),
        CredentialType(name="OAuth Token"),
    ]

    session.add_all(credential_types)
    session.commit()


if __name__ == "__main__":
    create_tables()
    app()
