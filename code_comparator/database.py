import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_database():
  """Retrieves the database."""

  # Executes if the database is not already connected and stored in the g
  # object.
  if "database" not in g:

    # Connects to and stores the database in the g object.
    g.database = sqlite3.connect(current_app.config["DATABASE"],
      detect_types=sqlite3.PARSE_DECLTYPES)

    # Configures the database to return rows that behave like dictionaries.
    g.database.row_factory = sqlite3.Row

  # Returns the database.
  return g.database


def close_database(e=None):
  """Closes the database."""

  # Retrieves the database from the g object.
  database = g.pop("database", None)

  # Executes if the database exists.
  if database is not None:

    # Closes the database.
    database.close()


def initialize_database():
  """Initializes the database."""

  # Retrieves the database.
  database = get_database()

  # Opens the database schema.
  with current_app.open_resource("schema.sql") as database_schema:

    # Configures the database from the schema.
    database.executescript(database_schema.read().decode("utf8"))


@click.command("initialize-database")
@with_appcontext
def initialize_database_command():
  """Initializes the database from the command line."""

  # Initializes the database.
  initialize_database()

  # Outputs information to the CLI.
  click.echo("Initialized the database.")


def initialize_application(application):
  """Registers database commands with the application."""

  # Calls close_database at application cleanup.
  application.teardown_appcontext(close_database)

  # Makes initialize_database_command callable with the flask command.
  application.cli.add_command(initialize_database_command)