import json
import mysql.connector
from mysql.connector import Error
from barmaid.settings.common import (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD,
                                     MYSQL_DATABASE, ITEM_REGISTRATION_FILE)


class DBQueries:
    """
    Implements Database query statements.
    """
    @staticmethod
    def create_schema(name):
        return f'CREATE SCHEMA {name};'

    @staticmethod
    def use_schema(name):
        return f'USE {name};'

    @staticmethod
    def create_user_table():
        query = '''
        CREATE TABLE User (
            user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            discord_id VARCHAR(255) UNIQUE NOT NULL,
            coins REAL DEFAULT 0.0
        )
        '''
        return query

    @staticmethod
    def create_purchases_table():
        query = '''
        CREATE TABLE Purchases (
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            items VARCHAR(500),
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES User (user_id)
        )
        '''
        return query

    @staticmethod
    def create_items_table():
        query = '''
        CREATE TABLE Items (
            item_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            value INT NOT NULL,
            description VARCHAR(255),
            sell_count INT DEFAULT 0,
            sprite_path VARCHAR(500)
        )
        '''
        return query

    @staticmethod
    def insert_user(discord_id):
        return f"INSERT INTO User (discord_id) VALUES ('{discord_id}')"

    @staticmethod
    def insert_purchase(user, blob):
        return f"INSERT INTO Purchases (user_id, items) VALUES ({user}, '{blob}')"

    @staticmethod
    def insert_item(name, value, description=None, path=None, sell_count=0):
        query =  f'''
        INSERT INTO Items (name, value, description, sprite_path, sell_count)
        VALUES ('{name}', {value}, '{description}', '{path}', {sell_count})
        '''
        return query

    @staticmethod
    def select_user(where=None):
        if not where:
            return 'SELECT * FROM User'

        column, value = where.get('column'), where.get('value')
        operator = where.get('operator')
        condition = f'{column} {operator} {value}'

        return f'SELECT * FROM User WHERE {condition}'

    @staticmethod
    def select_purchases(where=None):
        if not where:
            return 'SELECT * FROM Purchases'

        column, value = where.get('column'), where.get('value')
        operator = where.get('operator')
        condition = f'{column} {operator} {value}'

        return f'SELECT * FROM Purchases WHERE {condition}'

    @staticmethod
    def select_item(where=None):
        if not where:
            return 'SELECT * FROM Items'

        column, value = where.get('column'), where.get('value')
        operator = where.get('operator')
        condition = f'{column} {operator} {value}'

        return f'SELECT * FROM Items WHERE {condition}'

    @staticmethod
    def update_user(user_id, coins):
        query = f'''
        UPDATE User
        SET coins = {coins}
        WHERE user_id = {user_id}
        '''
        return query

    @staticmethod
    def update_purchases(user_id, blob):
        query = f'''
        UPDATE Purchases
        SET items = '{blob}'
        WHERE user_id = {user_id}
        '''
        return query


def db_connection(host_name=MYSQL_HOST, user_name=MYSQL_USER, user_password=MYSQL_PASSWORD):
    """
    Connects with database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
        print('Database connection successful')
    except Error as err:
        print(f"Error: '{err}'")

    return connection


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


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def get_or_create_user(discord_id):
    condition = {'column': 'discord_id', 'operator': '=', 'value': f"'{discord_id}'"}
    query = DBQueries.select_user(where=condition)

    con = create_db_connection()
    result = read_query(con, query)

    if result:  # return the existent
        return next(iter(result))

    # object does not exist: create new
    query = DBQueries.insert_user(discord_id)
    execute_query(con, query)

    return get_or_create_user(discord_id)


def init_db():
    """
    Initializes barmaid database:
    Creates schema and tables.
    Register initial items from population file defined on path setted at
    global setting variable ITEM_REGISTRATION_FILE.
        It is suggested to write the mentioned population file as json before
        running this command.
    """
    try:
        with open(ITEM_REGISTRATION_FILE, 'r') as data:
            items = json.load(data)
    except FileNotFoundError:
        raise Exception(f'Population file not found on {ITEM_REGISTRATION_FILE}!')

    if not items:
        raise Exception('No item found on population file!')

    con = db_connection()

    # Creates main schema and tables
    script = (
        DBQueries.create_schema(MYSQL_DATABASE),
        DBQueries.use_schema(MYSQL_DATABASE),
        DBQueries.create_user_table(),
        DBQueries.create_purchases_table(),
        DBQueries.create_items_table()
    )
    for statement in script:
        execute_query(con, statement)
    print('Database and tables created!')

    # populate item with initial items
    for item in items:
        print(f'Registering {item["name"]}')
        query = DBQueries.insert_item(
            name=item['name'],
            value=item['value'],
            description=item['description'],
            path=item['sprite_path'],
            sell_count=item['sell_count']
        )
        execute_query(con, query)

    print('Initial migration end.')
