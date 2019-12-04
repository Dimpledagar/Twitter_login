from psycopg2 import pool

'''
import psycopg2
def connect():
    return psycopg2.connect(database="test",
                            user="postgres",
                            password="password",
                            host="localhost")

'''


class Database:
    connection_pool = None  # __ converts a variable into private variable

    @classmethod
    def initilize(cls, **args):
        cls.connection_pool = pool.SimpleConnectionPool(1,
                                                        1,
                                                        **args)

    @classmethod
    def close_all_connections(cls):
        Database.connection_pool.closeall()


class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.connection_pool.getconn()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.connection_pool.putconn(self.connection)
