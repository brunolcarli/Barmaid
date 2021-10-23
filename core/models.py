import json
from ast import literal_eval as read_json
import discord
from core.database import create_db_connection, execute_query, get_or_create_user, read_query, DBQueries
from core.util import condition


class User:
    """
    Representation of an user object on the system.
    Display and manipulate user attribute values as well as handling the
    object interactions such as transactions and data storing and retrieving
    from database.
    """
    def __init__(self, discord_id):
        # resove data from db
        user = get_or_create_user(discord_id)
        purchases = read_query(
            create_db_connection(),
            DBQueries.select_purchases(where=condition('user_id', user[0]))
        )
        purchases = next(iter(purchases), None)

        # Defines object attributes
        self.id = user[0]
        self.discord_id = discord_id
        self.coins = user[2]
        self.purchases = purchases[1] if purchases else purchases

    def save(self):
        """
        Save current attributes to permanet file on database.
        """
        con = create_db_connection()
        execute_query(
            con,
            DBQueries.update_user(self.id, self.coins)
        )

    def add_coin(self, value):
        self.coins += value
        self.save()

    def add_purchase(self, item):
        self.add_coin(-item.value)
        purchases = read_json(self.purchases) if self.purchases else {}

        if item.name in purchases:
            purchases[item.name] += 1
        else:
            purchases[item.name] = 1

        if not self.purchases:
            execute_query(
                create_db_connection(),
                DBQueries.insert_purchase(self.id, purchases)
            )
        else:
            execute_query(
                create_db_connection(),
                DBQueries.update_purchase(self.id, purchases)
            )
        self.purchases = f'{json.dumps(purchases)}'
        print(f'Updated purchases for user {self.discord_id}')  # TODO: use logger

    def get_purchases(self) -> dict:
        """
        Return purchases as dict.
        Purchases are originally stored as json string on database, this
        method returns the data converted as python dict.
        """
        return read_json(self.purchases)


class Item:
    def __init__(self, data):
        self.code = data[0]
        self.name = data[1]
        self.value = data[2]
        self.description = data[3]
        self.sell_count = data[4]
        self.sprite = f'static/img/{data[5]}'

    def __repr__(self) -> str:
        return self.name

    def sell(self):
        self.sell_count += 1
        execute_query(
            create_db_connection(),
            DBQueries.update_item(self.code, self.sell_count)
        )


class SpecificItem(Item):
    def __init__(self, code):
        item = read_query(
            create_db_connection(),
            DBQueries.select_item(where=condition('item_id', code))
        )
        if not item:
            raise NameError(f'Item {code} does not exist!')

        super().__init__(next(iter(item)))


class ItemList:
    def __init__(self):
        items = read_query(
            create_db_connection(),
            DBQueries.select_item()
        )
        self.items = [Item(item) for item in items]
