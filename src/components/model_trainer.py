import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from src.exception import CustomException
from src.logger import logging
from src.utils import PostgreSQLDataHandler,calculate_scores
from src.components.variable import dataBase
from src.utils import save_object
from kneed import KneeLocator
import sys
from dataclasses import dataclass
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)
import os

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.db = PostgreSQLDataHandler()
        self.calculate_scores=calculate_scores

    def initiate_model_training(self, train_array, tablename):

        try:
            logging.info('Initiating model training')

            wcss=[]
            for k in range(2,11):
                kmean=KMeans(n_clusters=k,init="k-means++")
                kmean.fit(train_array)
                wcss.append(kmean.inertia_)

            k=KneeLocator(range(2,11),wcss,curve='convex',direction='decreasing')


            # Use K-Means clustering with 4 clusters
            kmeans = KMeans(n_clusters=k.elbow,init='k-means++', random_state=42).fit(train_array)
            yhat_kmeans = kmeans.predict(train_array)

            # Calculate the Soliot score based on cluster sizes
            soliot_score,silhouette_score = self.calculate_scores(train_array,4)

            logging.info(f'Model is trained successfully. Soliot Score: {soliot_score} silhouette_score: {silhouette_score}')
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=kmeans
            )

            logging.info('Model.pkl file has been saved')


            df = self.db.fetch_data(tablename)
            df["Clusters"] = yhat_kmeans

            df.replace({'Clusters': {3: 'Bronze', 0: 'Platinum', 1: 'Silver', 2: 'Gold'}},inplace=True)

            merge_table = 'merge_table'
            logging.info(f'Initiating table uploading to the database as {merge_table}')

            self.db.upload_dataframe(df, merge_table)

            logging.info(f'Table has been uploaded to the database with table name {merge_table}')

        except Exception as e:
            logging.info('Exception occurred at Model Training')
            raise CustomException(e, sys)
