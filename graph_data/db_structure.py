import mysql.connector
import numpy as np


def create_db(db_name, host, user, password):

    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
    )
    # Cursor to execute SQL queries
    cursor = db.cursor()

    # Create the db - IF it does NOT exist already
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    db.close()
    print(f"Database '{db_name}' has been created.")


def create_table(table_name, db_name, host, user, password):

    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = db.cursor()

    # Create the table - IF it does NOT exist already
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, minor TEXT)")

    db.commit()
    db.close()

    print(f"Table '{table_name}' has been created.")


def insert_fm(minor, table_name, db_name, host, user, password):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    cursor = db.cursor()

    # Adjacency matrix to string (db-compatible format)
    cursor.execute(f"INSERT INTO {table_name} (minor) VALUES (%s)", (np.array2string(minor),))

    db.commit()
    db.close()

    print(f"Minor '{minor}' has been inserted into '{table_name}'.")
