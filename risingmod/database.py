import sqlite3
from sqlite3 import Error

sql_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id NOT NULL PRIMARY KEY,
                                    discord_id integer NOT NULL,
                                    muted integer NOT NULL DEFAULT 0,
                                    temp_mute_stamp integer DEFAULT 0,
                                    suggestions integer DEFAULT 0,
                                    reports integer DEFAULT 0,
                                    warnings integer DEFAULT 0,
                                    excempt integer DEFAULT 0
                                ); """

sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS channels (
                                audit_log integer PRIMARY KEY,
                                superior_audit_log text NOT NULL,
                                suggestions_feed integer,
                                bugs_feed integer,
                                reports_feed integer,
                                
                            );"""


def setup():
    print("nothing")


def create_connection(db):
    """ Initiate a connection using the db statement (path expected)
    :param db: Sqlite3 DB file path
    :return:
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
