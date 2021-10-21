import mysql.connector
from mysql.connector import Error
from barmaid.settings.common import (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD,
                                     MYSQL_DATABASE)


def create_db_connection(host_name=MYSQL_HOST, user_name=MYSQL_USER,
                         user_password=MYSQL_PASSWORD, db_name=MYSQL_DATABASE):
    """
    Connects with database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print('Database connection successful')
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    """
    Create a new schema;
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('DB schema created successfully')
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query successful')
    except Error as err:
        print(f"Error: '{err}'")


class DBQueries:
    """
    Implements Database query methods.
    """

    @staticmethod
    def query_users(*args):
        query = '''
        SELECT * from users;
        '''

    @staticmethod
    def init_tables():
        con = create_db_connection()

        create_user_query = '''
        CREATE TABLE User (
            user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            discord_id VARCHAR(25) NOT NULL,
            coins REAL
        )
        '''

        create_purchases_query = '''
        CREATE TABLE Purchases (
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            items BLOB,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES User (user_id)
        )
        '''

        create_item_query = '''
        CREATE TABLE Items (
            item_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            value INT NOT NULL,
            description VARCHAR(255),
            sell_count INT DEFAULT 0,
            sprite_path VARCHAR(500)
        )
        '''
        execute_query(con, create_user_query)
        execute_query(con, create_purchases_query)
        execute_query(con, create_item_query)
