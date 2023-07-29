import pandas as pd
import numpy as np
from src.exception import CustomException
import os
from src.logger import logging
import sys
from datetime import datetime
from src.utils import DatabaseManager
from src.components.variable import dataBase
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA

class DataTransformationConfig:
    def __init__(self):
        self.DatabaseManager = DatabaseManager()
        self.conn = dataBase.conn

    def process_data_and_reduce_dimensionality(self, df):  
        # Process customer data
        df.dropna(inplace=True)
        df['dt_customer'] = pd.to_datetime(df['dt_customer']) #dt_customer
        newest_customer_date = df['dt_customer'].max()
        oldest_customer_date = df['dt_customer'].min()
        df['Customer_For'] = (newest_customer_date - df['dt_customer']).dt.days

        current_year = datetime.now().year
        df['Age'] = current_year - df['year_birth']
        df['Spent'] = df[['mntwines', 'mntfruits', 'mntmeatproducts', 'mntfishproducts', 'mntsweetproducts', 'mntgoldprods']].sum(axis=1)
        df['living_with'] = df['marital_status'].replace({"Married": "Partner", "Together": "Partner", "Absurd": "Alone", "Widow": "Alone", "YOLO": "Alone", "Divorced": "Alone", "Single": "Alone"})
        df['children'] = df['kidhome'] + df['teenhome']
        df['Family_Size'] = df['living_with'].replace({"Alone": 1, "Partner": 2})
        df['Is_Parent'] = np.where(df['children'] > 0, 1, 0)
        df['education'] = df['education'].replace({"Basic": "Undergraduate", "2n Cycle": "Undergraduate", "Graduation": "Graduate", "Master": "Postgraduate", "PhD": "Postgraduate"})
        df['Customer_For'] = pd.to_numeric(df['Customer_For'], errors="coerce")
        df.rename(columns={
            "mntwines": "Wines",
            "mntfruits": "Fruits",
            "mntmeatproducts": "Meat",
            "mntfishproducts": "Fish",
            "mntsweetproducts": "Sweets",
            "mntgoldprods": "Gold"
        }, inplace=True)

        to_drop = ["marital_status", "dt_customer", "z_costcontact", "z_revenue", "year_birth", "id"]
        df.drop(to_drop, axis=1, inplace=True)

        data = df.select_dtypes(include=[np.number])

        # Reduce dimensionality using PCA
        s = (df.dtypes == 'object')
        object_cols = list(s[s].index)
        LE = LabelEncoder()
        for col in object_cols:
            df[col] = LE.fit_transform(df[col])

        ds = df.copy()
        cols_del = ['acceptedcmp3', 'acceptedcmp4', 'acceptedcmp5', 'acceptedcmp1', 'acceptedcmp2', 'complain', 'response']
        ds = ds.drop(cols_del, axis=1)

        scaler = StandardScaler()
        scaler.fit(ds)
        scaled_ds = pd.DataFrame(scaler.transform(ds), columns=ds.columns)

        pca = PCA(n_components=3)
        pca.fit(scaled_ds)
        PCA_ds = pd.DataFrame(pca.transform(scaled_ds), columns=["PCA1", "PCA2", "PCA3"])

        filename1 = 'CleanData'
        filename2 = 'PCAdata'

        try:
            self.DatabaseManager.create_table(data, filename1)
            logging.info(f'Successfully created table in the database table name: {filename1}')

            self.DatabaseManager.create_table(PCA_ds, filename2)
            logging.info(f'Successfully created table in the database table name: {filename2}')

            self.DatabaseManager.execute_values(data, filename1)
            logging.info('DataFrame data values have been successfully uploaded to the database table')

            self.DatabaseManager.execute_values(PCA_ds, filename2)
            logging.info('DataFrame data values have been successfully uploaded to the database table')
        except Exception as e:
            logging.info('Exception occurred at data_process.py file during creating table/execute_value')
            raise CustomException(e, sys)

        return filename1, filename2

# Step 1: Create an instance of the DataTransformationConfig class
data_transformer = DataTransformationConfig()

# Step 2: Load your data into a pandas DataFrame
# Assuming you have your data in a CSV file named 'customer_data.csv'
db=DatabaseManager()
customer_data = db.execute_query('select * from marketing_campaign',fetch=True)

# Step 3: Call the process_data_and_reduce_dimensionality method and pass the DataFrame
filename1, filename2 = data_transformer.process_data_and_reduce_dimensionality(customer_data)

df1=db.execute_query(f'select * from {filename1}',fetch=True)
df2=db.execute_query(f'select * from {filename2}',fetch=True)

logging.info(f'file names is : {filename1},{filename2}')
logging.info(f'df1: {df1.head()}')
logging.info(f'df2: {df2.head()}')


# Step 4: The method will process the data and upload it to the database
# You can now use 'processed_data' and 'reduced_data' for further analysis or other tasks.
# The data has been transformed and reduced using PCA.
