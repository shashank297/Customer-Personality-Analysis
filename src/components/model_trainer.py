# Basic Imports
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from src.exception import CustomException
from src.logger import logging
from src.utils import DatabaseManager
from src.components.variable import dataBase
from src.utils import save_object
from dataclasses import dataclass
import sys
import os

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.db = DatabaseManager()
        self.conn = dataBase.conn

    def initiate_model_training(self, train_array, tablename):

        try:
            logging.info('Initiating model training')

            # Use K-Means clustering with 4 clusters
            kmeans = KMeans(n_clusters=4,init='k-means++', random_state=42)
            yhat_kmeans = kmeans.fit_predict(train_array)

            logging.info('Model is trained successfully')
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=kmeans
            )

            logging.info('Model.pkl file has been saved')

            df = self.db.execute_query(f'select * from {tablename}', fetch=True)
            df["Clusters"] = yhat_kmeans

            merge_table = 'merge_table'
            logging.info(f'Initiating table uploading to the database as {merge_table}')

            # self.db.create_table(df=df, table_name=merge_table)
            self.db.execute_values(df, merge_table)

            logging.info(f'Table has been uploaded to the database with table name {merge_table}')

        except Exception as e:
            logging.info('Exception occurred at Model Training')
            raise CustomException(e, sys)

# # Usage
# if __name__ == "__main__":
#     # Sample usage of ModelTrainer
#     trainer = ModelTrainer()
#     train_data = np.random.rand(100, 10)  # Example training data
#     table_name = "data_table"  # Example table name
#     trainer.initiate_model_training(train_data, table_name)
