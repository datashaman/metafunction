import typer
from cryptography.fernet import Fernet

from metafunction.database import (
    create_tables,
    get_session,
    select,
    Session,
    CredentialType,
    User,
)


app = typer.Typer()


@app.command()
def create_user(name: str, email: str, password: str, is_admin: bool = False) -> None:
    session = next(get_session())
    user = User(name=name, email=email, password=password, is_admin=is_admin)
    session.add(user)
    session.commit()
    typer.echo(f"User {name} created")


@app.command()
def list_users() -> None:
    session = next(get_session())
    users = session.exec(select(User).order_by(User.name)).all()
    for user in users:
        typer.echo(f"{user.name} - {user.email}")


@app.command()
def generate_key() -> None:
    key = Fernet.generate_key()
    typer.echo(key.decode())


@app.command()
def seed_data() -> None:
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
