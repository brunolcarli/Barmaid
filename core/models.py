from core.database import create_db_connection, execute_query, get_or_create_user, read_query, DBQueries
from core.util import condition


class User:
    def __init__(self, discord_id):
        # resove data from db
        user = get_or_create_user(discord_id)
        purchases = read_query(
            create_db_connection(),
            DBQueries.select_purchases(where=condition('user_id', user[0]))
        )
        purchases = next(iter(purchases), None)

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
        if self.purchases:
            execute_query(
                con,
                DBQueries.update_purchases(self.id, self.purchases)
            )

    def add_coin(self, value):
        self.coins += value
        self.save()
