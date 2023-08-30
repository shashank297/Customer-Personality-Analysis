import pandas as pd
import numpy as np
from src.exception import CustomException
import os
from src.logger import logging
import sys
from datetime import datetime
from src.utils import PostgreSQLDataHandler
from src.components.variable import dataBase
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA

class DataCleaning:
    def __init__(self):
        self.db = PostgreSQLDataHandler()

    def process_data_and_reduce_dimensionality(self, filename):

        try:
            logging.info('Database table reading start in data_process.py')
            df=self.db.fetch_data(filename)
            logging.info('In data_process.py database table converted into df')

        except Exception as e:
            logging.info('Exception occurred at data_process.py in table reading from db stage')
            raise CustomException(e,sys)

        # Process df data
        df = df.dropna()

        # Assuming the date strings are in the format '%d-%m-%Y'
        df['dt_customer'] = pd.to_datetime(df['dt_customer'], format='%d-%m-%Y')

        # Calculate the 'customer_for' column
        df['customer_for'] = 12.0 * (2015 - df['dt_customer'].dt.year) + (1 - df['dt_customer'].dt.month)

        current_year = datetime.now().year
        df['Age'] = current_year - df['year_birth']
        df['Spent'] = df[['mntwines', 'mntfruits', 'mntmeatproducts', 'mntfishproducts', 'mntsweetproducts', 'mntgoldprods']].sum(axis=1)
        df['living_with'] = df['marital_status'].replace({"Married": "Partner", "Together": "Partner", "Absurd": "Single", "Widow": "Single", "YOLO": "Single", "Divorced": "Single", "Single": "Single"})
        df['children'] = df['kidhome'] + df['teenhome']
        df['Family_Size'] = df['living_with'].replace({"Single": 1, "Partner": 2,"Alone":1})
        df['Is_Parent'] = np.where(df['children'] > 0, 1, 0)
        df['education'] = df['education'].replace({"Basic": "Undergraduate", "2n Cycle": "Undergraduate", "Graduation": "Graduate", "Master": "Postgraduate", "PhD": "Postgraduate"})
        df['customer_for'] = pd.to_numeric(df['customer_for'], errors="coerce")
        df.loc[(df['Age'] >= 13) & (df['Age'] <= 19), 'AgeGroup'] = 'Teen'
        df.loc[(df['Age'] >= 20) & (df['Age']<= 39), 'AgeGroup'] = 'Adult'
        df.loc[(df['Age'] >= 40) & (df['Age'] <= 59), 'AgeGroup'] = 'Middle Age Adult'
        df.loc[(df['Age'] >= 60), 'AgeGroup'] = 'Senior Adult'
        df.rename(columns={
            "mntwines": "Wines",
            "mntfruits": "Fruits",
            "mntmeatproducts": "Meat",
            "mntfishproducts": "Fish",
            "mntsweetproducts": "Sweets",
            "mntgoldprods": "Gold"
        }, inplace=True)

        df = df[df.Age < 100]
        df = df[df.income < 120000]


        filename2 = 'without_encoding'

        try:
            self.db.upload_dataframe(df, filename2)
            logging.info('DataFrame data values have been successfully uploaded to the database table')

        except Exception as e:
            logging.info('Exception occurred at data_process.py file during creating table/execute_value')
            raise CustomException(e, sys)


        data = df.copy()
        to_drop = ["marital_status", "dt_customer", "z_costcontact", "z_revenue", "year_birth", "id","AgeGroup","living_with"]
        data.drop(to_drop, axis=1, inplace=True)

        data.Is_Parent = pd.to_numeric(data.Is_Parent, errors='coerce')



        #Get list of categorical variables
        s = (data.dtypes == 'object')
        object_cols = list(s[s].index)

        LE = LabelEncoder()
        for i in object_cols:
            data[i] = LE.fit_transform(data[i])
            
        print("All features are now numerical")

        filename1 = 'cleaned_data'

        try:
            self.db.upload_dataframe(data, filename1)
            logging.info('DataFrame data values have been successfully uploaded to the database table')

        except Exception as e:
            logging.info('Exception occurred at data_process.py file during creating table/execute_value')
            raise CustomException(e, sys)

        return filename1,filename2