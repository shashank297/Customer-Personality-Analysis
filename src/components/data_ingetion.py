import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.variable import dataBase
from src.utils import PostgreSQLDataHandler


@dataclass
class DataIngestionconfig:
    folder_path = os.path.join('Notebook', 'Data')
    file_names = os.listdir(folder_path)[0].split('.')[0]


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()
        self.PostgreSQLDataHandler = PostgreSQLDataHandler()  # Initialize the PostgreSQLDataHandler

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion Method Start')

        try:
            df = pd.read_csv(os.path.join('Notebook/data', 'marketing_campaign.csv'))
            logging.info("Dataset Read as a Pandas dataframe")

            df.drop('unnamed: 0',axis=1,inplace=True)
            try:
                self.PostgreSQLDataHandler.upload_dataframe(df, self.ingestion_config.file_names)
                logging.info('DataFrame values have been successfully uploaded to the database table')

            except Exception as e:
                logging.info('Exception occurred at database table creation/data_transfer stage')
                raise CustomException(e, sys)

            logging.info('Ingestion of Data is completed')

        except Exception as e:
            logging.info('Exception occurred at Data Ingestion stage')
            raise CustomException(e, sys)
        return self.ingestion_config.file_names

