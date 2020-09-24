import sqlite3
import os


class DbConnector:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def _bd_exists(self):
        return os.path.exists(self.db_path)

