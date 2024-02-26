import typer

from api.db import create_db_from_scheema, get_db_session
from api import models

cli = typer.Typer()

db = typer.Typer()


@db.command()
def reflect():
    create_db_from_scheema()

@db.command()
def add_fake_data():
    session = get_db_session()
    user1 = models.User(name="User1")
    session.add(user1)
    session.add(models.Post(title="first post", content="some stuff", user=user1))
    session.commit()


cli.add_typer(db, name="db")


if __name__ == "__main__":
    cli()
