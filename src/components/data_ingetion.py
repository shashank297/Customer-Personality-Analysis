import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.variable import dataBase
from src.utils import DatabaseManager


@dataclass
class DataIngestionconfig:
    conn = dataBase
    folder_path = os.path.join('Notebook', 'Data')
    file_names = os.listdir(folder_path)[0].split('.')[0]


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionconfig()
        self.DatabaseManager = DatabaseManager()  # Initialize the DatabaseManager

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion Method Start')

        try:
            df = pd.read_csv(os.path.join('Notebook/data', 'marketing_campaign.csv'))
            logging.info("Dataset Read as a Pandas dataframe")

            df.drop('Unnamed: 0',axis=1,inplace=True)
            try:
                self.DatabaseManager.create_table(df, self.ingestion_config.file_names)
                logging.info('Successfully created table in the database')

                self.DatabaseManager.execute_values(df, self.ingestion_config.file_names)
                logging.info('DataFrame values have been successfully uploaded to the database table')

            except Exception as e:
                logging.info('Exception occurred at database table creation/data_transfer stage')
                raise CustomException(e, sys)

            logging.info('Ingestion of Data is completed')

        except Exception as e:
            logging.info('Exception occurred at Data Ingestion stage')
            raise CustomException(e, sys)


# Create an instance of the DataIngestion class and call the method
data_ingestion = DataIngestion()
data_ingestion.initiate_data_ingestion()
