from mcp.DbConnector import DbConnector
import pandas as pd


class CovidDb(DbConnector):
    table_name = 'stats'

    def __init__(self, db_path):
        super().__init__(db_path)

    def getStats(self):
        query = f'''
            SELECT * FROM {self.table_name} 
        '''
        df = pd.read_sql_query(query, self.conn).set_index('data')
        df.index = pd.to_datetime(df.index)
        return df.sort_index(ascending=True)

    def insertStats(self, df: pd.DataFrame):
        df.to_sql(self.table_name, self.conn, if_exists='replace')

    def table_exists(self):
        return self.conn.execute(f'''
            SELECT count(name) 
            FROM sqlite_master 
            WHERE type='table' AND name='{self.table_name}';
        ''').fetchone()[0] == 1

    def close(self):
        self.conn.close()


