import sqlite3

print("import kardam")

class DataBaseConnection(sqlite3.Connection):
    def __init__(self):
        super().__init__(r"E:\learning python\my codes\srcc\Library.db")

    __instance = None

    def __new__(cls):
        try:
            if not DataBaseConnection.__instance:
                # DataBaseConnection.__instance = sqlite3.connect("ChatroomDatabased.db")
                DataBaseConnection.__instance = super().__new__(cls)
            return DataBaseConnection.__instance
        except Exception as e:
            raise e

class DataBaseCursor:

    def __init__(self):
        pass

    __instance = None

    def __new__(cls,conn):
        try:
            if not DataBaseCursor.__instance:
                DataBaseCursor.__instance = conn.cursor()
            return DataBaseCursor.__instance
        except Exception as e:
            raise e    