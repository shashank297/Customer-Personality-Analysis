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

class DataCleaning:
    def __init__(self):
        self.db = DatabaseManager()
        self.conn = dataBase.conn

    def process_data_and_reduce_dimensionality(self, filename):

        try:
            logging.info('Database table reading start in data_process.py')
            df=self.db.execute_query(f'select * from {filename}',fetch=True)
            logging.info('In data_process.py database table converted into df')

        except Exception as e:
            logging.info('Exception occurred at data_process.py in table reading from db stage')
            raise CustomException(e,sys)

        # Process customer data
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

        data = df.copy()

        data.Is_Parent = pd.to_numeric(data.Is_Parent, errors='coerce')


        filename2 = 'Without_encoding'

        try:
            self.db.execute_values(data, filename2)
            logging.info('DataFrame data values have been successfully uploaded to the database table')

        except Exception as e:
            logging.info('Exception occurred at data_process.py file during creating table/execute_value')
            raise CustomException(e, sys)



        #Get list of categorical variables
        s = (data.dtypes == 'object')
        object_cols = list(s[s].index)

        LE = LabelEncoder()
        for i in object_cols:
            data[i] = LE.fit_transform(data[i])
            
        print("All features are now numerical")


        
        filename1 = 'cleaned_data'

        try:
            # self.db.create_table(data, filename1)
            # logging.info(f'Successfully created table in the database table name: {filename1}')



            self.db.execute_values(data, filename1)
            logging.info('DataFrame data values have been successfully uploaded to the database table')

        except Exception as e:
            logging.info('Exception occurred at data_process.py file during creating table/execute_value')
            raise CustomException(e, sys)

        return filename1

# data_transformer = DataTransformationConfig()

# # Step 2: Load your data into a pandas DataFrame
# # Assuming you have your data in a CSV file named 'customer_data.csv'
# db=DatabaseManager()
# customer_data = db.execute_query('select * from marketing_campaign',fetch=True)

# # Step 3: Call the process_data_and_reduce_dimensionality method and pass the DataFrame
# filename1= data_transformer.process_data_and_reduce_dimensionality(customer_data)

# df1=db.execute_query(f'select * from {filename1}',fetch=True)
# logging.info(f'file names is : {filename1}')
# logging.info(f'df1: \n {df1.head()}')