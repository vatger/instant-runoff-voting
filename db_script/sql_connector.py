from dotenv import load_dotenv
import mysql.connector
import os


class SqlConnector:
    def __init__(self):
        self.host = ''
        self.username_hp = ''
        self.password_hp = ''
        self.database_hp = ''
        self.username_board = ''
        self.password_board = ''
        self.database_board = ''

        self.current_db = ''
        self.conn = None

        self.__get_credentials()

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def execute_select(self, command: str, db_target) -> str:
        if self.current_db != db_target:
            self.__connect(db_target)

        cursor = self.conn.cursor()
        cursor.execute(command)
        res = cursor.fetchall()
        return res

    def execute(self, command: str, db_target):
        if self.current_db != db_target:
            self.__connect(db_target)

        print(command)

        cursor = self.conn.cursor()
        cursor.execute(command)
        self.conn.commit()

    def __connect(self, conn_dest: str):
        if self.conn is not None:
            self.conn.close()

        if conn_dest == 'hp':
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.username_hp,
                password=self.password_hp,
                database=self.database_hp
            )
            self.current_db = self.database_hp
        elif conn_dest == 'board':
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.username_board,
                password=self.password_board,
                database=self.database_board
            )
            self.current_db = self.database_board
        else:
            print(f"{conn_dest} is not a valid Database!")
            exit(-1)

        print(f"Connected to Database {self.current_db}@{self.host}")

    def __get_credentials(self):
        load_dotenv()

        self.host = os.getenv('DB_HOST')
        self.username_hp = os.getenv('DB_USERNAME_HP')
        self.password_hp = os.getenv('DB_PASSWORD_HP')
        self.database_hp = os.getenv('DB_DATABASE_HP')
        self.username_board = os.getenv('DB_USERNAME_BOARD')
        self.password_board = os.getenv('DB_PASSWORD_BOARD')
        self.database_board = os.getenv('DB_DATABASE_BOARD')

        print(f"Loaded SQL credentials...\n"
              f"Host: {self.host}\n"
              f"=========================================================")
