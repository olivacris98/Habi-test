import pymysql
from dotenv import dotenv_values
os_environment = dotenv_values('.env')


class Database:

    def __init__(
        self,
        host=os_environment.get("HOST"),
        user=os_environment.get("USER"),
        password=os_environment.get("PASS"),
        database=os_environment.get("SCHEMA"),
        port=int(os_environment.get("PORT"))
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connect()

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def all(self, query):
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                self.connection.close()
                return result
        except pymysql.Error as e:
            print(f"Error fetching data: {e}")

    def verify_conn(self):
        return True if self.connection.ping() else False
