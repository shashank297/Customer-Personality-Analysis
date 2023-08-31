# from dataclasses import dataclass
# import psycopg2

# @dataclass
# class dataBase:
#     conn = psycopg2.connect(
#         dbname='DB1',
#         user='postgres',
#         password='.t7xdeH~SvJsPjn&',
#         host='34.131.10.52',
#         port=5432
#     )



# class DatabaseManager:
#     def __init__(self):
#         self.conn = dataBase.conn

#     def create_table(self, df, table_name):
#         with self.conn.cursor() as cur:
#             columns = df.columns
#             dtypes = df.dtypes
#             query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
#             for col, dtype in zip(columns, dtypes):
#                 sql_type = self.get_sql_type(dtype)
#                 query += f"{col} {sql_type}, "
#             query = query.rstrip(", ")
#             query += ")"
#             cur.execute(query)
#             self.conn.commit()

#     def get_sql_type(self, dtype):
#         if dtype == 'object':
#             return 'TEXT'
#         elif dtype == 'int64':
#             return 'INTEGER'
#         elif dtype == 'float64':
#             return 'REAL'
#         elif dtype == 'bool':
#             return 'BOOLEAN'
#         elif dtype == '<M8[ns]':
#             return 'TIMESTAMP'
#         else:
#             return 'TEXT'

#     def execute_values(self, df, table_name):
#         with self.conn.cursor() as cur:
#             try:
#                 cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", (table_name,))
#                 table_exists = cur.fetchone()[0]
#                 if not table_exists:
#                     self.create_table(df, table_name)
#                     tuples = [tuple(row) for _, row in df.iterrows()]
#                     cols = ','.join(df.columns)
#                     query = "INSERT INTO %s(%s) VALUES %%s" % (table_name, cols)
#                     psycopg2.extras.execute_values(cur, query, tuples)
#                     self.conn.commit()
#                     logging.info("The DataFrame is inserted")
#                 # else:
#                     # logging.info("Table is already exists in the database")
#             except (Exception, psycopg2.DatabaseError) as error:
#                 logging.info("Error: %s" % error)
#                 self.conn.rollback()

#     def execute_query(self, query, commit=False, fetch=False):
#         with self.conn.cursor() as cur:
#             try:
#                 cur.execute(query)

#                 if fetch:
#                     try:
#                         records = cur.fetchall()
#                         columns = [desc[0] for desc in cur.description]
#                         df = pd.DataFrame(records, columns=columns)
#                         return df
#                     except Exception as e:
#                         logging.info(f'Done fetchall without col: Error: {e}')

#                 if commit:
#                     try:
#                         self.conn.commit()
#                         logging.info('Done commit')
#                     except Exception as e:
#                         logging.info(f'There is an error in commit: {e}')
#             except Exception as e:
#                 logging.info(f"There is an error in query: {e}")
#             finally:
#                 self.conn.rollback()
#     def rollback_transaction(self):
#         try:
#             self.conn.rollback()
#             logging.info("Transaction rolled back successfully.")
#         except psycopg2.Error as e:
#             logging.info("Error while rolling back the transaction:", e)