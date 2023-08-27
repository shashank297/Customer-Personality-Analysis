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

            # Calculate the Soliot score based on cluster sizes
            soliot_score = self.calculate_soliot_score(train_array, yhat_kmeans)

            logging.info(f'Model is trained successfully. Soliot Score: {soliot_score}')
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=kmeans
            )

            logging.info('Model.pkl file has been saved')

            df = self.db.execute_query(f'select * from {tablename}', fetch=True)
            df["Clusters"] = yhat_kmeans

            df.replace({'Clusters': {0: 'Bronze', 3: 'Platinum', 2: 'Silver', 1: 'Gold'}},inplace=True)

            merge_table = 'merge_table'
            logging.info(f'Initiating table uploading to the database as {merge_table}')

            # self.db.create_table(df=df, table_name=merge_table)
            self.db.execute_values(df, merge_table)

            logging.info(f'Table has been uploaded to the database with table name {merge_table}')

        except Exception as e:
            logging.info('Exception occurred at Model Training')
            raise CustomException(e, sys)

    def calculate_soliot_score(self, train_array, clusters):
        # Calculate Soliot score based on the distribution of data points in clusters
        cluster_sizes = [len(train_array[clusters == i]) for i in range(4)]

        # Assuming Soliot score is the ratio of the smallest cluster size to the largest cluster size
        soliot_score = min(cluster_sizes) / max(cluster_sizes)

        return soliot_score
