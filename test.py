from src.utils import DatabaseManager

db=DatabaseManager()

df=db.execute_query('Select * from marketing_campaign',fetch=True)
print(df.head())