import psycopg2
import pandas as pd
import psycopg2.extras as extras
from src.components.variable import dataBase


class DatabaseManager:
    def __init__(self):
        self.conn = dataBase.conn

    def fetch_columns(self, table_name):
        cur = self.conn.cursor()
        try:
            cur.execute(
                '''
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s;
                ''',
                (table_name,)
            )
            records = cur.fetchall()
            return [column[0] for column in records]
        except Exception as e:
            print(f'There is an error in fetch_columns: {e}')
            return []

    def create_table(self, df, table_name):
        cur = self.conn.cursor()
        columns = df.columns
        dtypes = df.dtypes
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for col, dtype in zip(columns, dtypes):
            sql_type = self.get_sql_type(dtype)
            query += f"{col} {sql_type}, "
        query = query.rstrip(", ")
        query += ")"
        cur.execute(query)
        self.conn.commit()

    def get_sql_type(self, dtype):
        if dtype == 'object':
            return 'TEXT'
        elif dtype == 'int64':
            return 'INTEGER'
        elif dtype == 'float64':
            return 'REAL'
        elif dtype == 'bool':
            return 'BOOLEAN'
        else:
            return 'TEXT'

    def execute_values(self, df, table_name):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", (table_name,))
            table_exists = cur.fetchone()[0]
            if not table_exists:
                self.create_table(df, table_name)
            tuples = [tuple(row) for _, row in df.iterrows()]
            cols = ','.join(df.columns)
            query = "INSERT INTO %s(%s) VALUES %%s" % (table_name, cols)
            psycopg2.extras.execute_values(cur, query, tuples)
            self.conn.commit()
            print("The DataFrame is inserted")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()

    def execute_query(self, query, commit=False, fetch=False, table_name=''):
        cur = self.conn.cursor()
        try:
            cur.execute(query)

            if fetch:
                try:
                    records = cur.fetchall()
                    columns = self.fetch_columns(table_name) if table_name else []
                    df = pd.DataFrame(records, columns=columns)
                    return df
                except Exception as e:
                    print(f'Done fetchall without col: Error: {e}')

            if commit:
                try:
                    self.conn.commit()
                    print('Done commit')
                except Exception as e:
                    print(f'There is an error in commit: {e}')
        except Exception as e:
            print(f"There is an error in query: {e}")

# Example usage:
db_manager = DatabaseManager()
table='marketing_campaign'
df = pd.read_csv(r'C:\Python_project\Customer-Personality-Analysis\Notebook\Data\marketing_campaign.csv')
df.drop('Unnamed: 0',axis=1,inplace=True)
db_manager.create_table(df,table_name=table)
db_manager.execute_values(df, table)  # Insert DataFrame into the database
result_df = db_manager.execute_query('drop table marketing_campaign',commit=True) # Fetch data from the database

