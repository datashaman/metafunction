import typer
from cryptography.fernet import Fernet

from api.models import get_db, Session, UserModel

app = typer.Typer()


@app.command()
def create_user(name: str, email: str, password: str, is_admin: bool = False):
    db = next(get_db())
    user = UserModel(name=name, email=email, password=password, is_admin=is_admin)
    db.add(user)
    db.commit()
    typer.echo(f"User {name} created")


@app.command()
def generate_key():
    key = Fernet.generate_key()
    typer.echo(key.decode())


if __name__ == "__main__":
    app()
