import os

from sqlalchemy_utils import database_exists, create_database


def create_database_if_not_exists():
    db_path = "db"
    if not os.path.exists(db_path):
        os.makedirs(db_path)

    connection_url = "sqlite:///db/todo_list.sqlite3"
    if not database_exists(connection_url):
        create_database(connection_url)