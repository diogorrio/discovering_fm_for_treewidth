import ast

import mysql.connector
import networkx as nx


def create_db(db_name, host, user, password):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
    )
    cursor = db.cursor()

    stmt = "CREATE DATABASE IF NOT EXISTS {}".format(db_name)

    cursor.execute(stmt)

    db.close()
    print("Database", db_name, "has been created.")


def create_table(table_name, db_name, host, user, password):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    cursor = db.cursor()

    stmt = (
        "CREATE TABLE IF NOT EXISTS {} "
        "(id INT AUTO_INCREMENT PRIMARY KEY, minors TEXT)"
    ).format(table_name)

    cursor.execute(stmt)

    db.commit()
    db.close()

    print("Table", table_name, "has been created.")


def insert_fm(minor_to_add, table_name, db_name, host, user, password):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    cursor = db.cursor()

    stmt = (
        "INSERT INTO {} (minors)"
        "VALUES (%s)"
    ).format(table_name)
    data = (minor_to_add,)

    cursor.execute(stmt, data)

    db.commit()
    db.close()

    print("Minor", minor_to_add, "has been inserted into", table_name)


def remove_fm(minor_to_remove, table_name, db_name, host, user, password):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    cursor = db.cursor()

    stmt = (
        "DELETE FROM {} WHERE minors = %s"
    ).format(table_name)
    data = (minor_to_remove,)

    cursor.execute(stmt, data)

    db.commit()
    db.close()

    print("Minor", minor_to_remove, "has been removed from", table_name, ".")


def retrieve_entries(table_name, db_name, host, user, password):
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
    )
    cursor = db.cursor()

    stmt = "SELECT minors FROM {}".format(table_name)
    print("Retrieving entries from table '{}' in database '{}'...".format(table_name, db_name))
    cursor.execute(stmt)
    rows = cursor.fetchall()

    entries = [row[0] for row in rows]
    n_entries = []

    for i, entry in enumerate(entries):
        entries[i] = ast.literal_eval(entry)
        n_entry = nx.Graph()
        n_entry.add_edges_from(entries[i])
        n_entries.append(n_entry)

    db.close()

    print("Entries retrieved successfully.")

    return entries, n_entries
