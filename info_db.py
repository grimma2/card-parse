import datetime

from my_settings import DB_DATA
import psycopg2


class DB:

    def __init__(self):
        self.cursor = psycopg2.connect(
            f'dbname={DB_DATA["dbname"]} user={DB_DATA["user"]} password={DB_DATA["password"]}')\
            .cursor()

    def get_last_30_or_none(self, field='*'):
        date = datetime.datetime.now() - datetime.timedelta(days=30)
        self.cursor.execute(f"SELECT {field} FROM trans WHERE deta > %s", (date,))
        return self.cursor

    def get_last_month_or_none(self, field='*'):
        date = datetime.datetime.now().replace(day=1)
        self.cursor.execute(f"SELECT {field} FROM trans WHERE deta >= %s", (date,))
        return self.cursor

    def add_ogr(self, ogr) -> None:
        self.cursor.execute("INSERT INTO ogrs VALUES (%s)", (ogr,))

    def del_ogr(self) -> None:
        self.cursor.execute("DELETE FROM ogrs")

    def get_ogr(self):
        self.cursor.execute("SELECT ogr_cost FROM ogrs")
        return self.cursor
