from dataclasses import dataclass
import psycopg2

@dataclass
class dataBase:
    conn = psycopg2.connect(
        dbname='DB1',
        user='postgres',
        password='.t7xdeH~SvJsPjn&',
        host='34.131.10.52',
        port=5432
    )

