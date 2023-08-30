from dataclasses import dataclass
import psycopg2

@dataclass
class dataBase:
    username='postgres'
    password='.t7xdeH~SvJsPjn&'
    hostname='34.131.10.52'
    port='5432'
    database_name='DB1'
    db_url = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"




