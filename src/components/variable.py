from dataclasses import dataclass
import psycopg2

@dataclass
class dataBase:
    username=''
    password=''
    hostname=''
    port=''
    database_name=''
    db_url = f""




