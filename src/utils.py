import pandas as pd
import os
import sys
from sqlalchemy import create_engine  # Import create_engine from SQLAlchemy
from src.components.variable import dataBase
from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import silhouette_score
import numpy as np
from sklearn.cluster import KMeans
import pickle

class PostgreSQLDataHandler:
    def __init__(self,db_url=dataBase.db_url):
        self.engine = create_engine(db_url)
    
    def upload_dataframe(self, df, table_name):
        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            logging.info(f"DataFrame successfully uploaded to '{table_name}' in PostgreSQL.")
            return f"DataFrame successfully uploaded to '{table_name}' in PostgreSQL."
        except Exception as e:
            raise CustomException(e, sys)
            logging.error(f"An error occurred: {str(e)}")
            return f"An error occurred: {str(e)}"

    def fetch_data(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            raise CustomException(e, sys)
            logging.error(f"An error occurred: {str(e)}")
            return None  # Return None to indicate an error

    def close_connection(self):
        try:
            self.engine.dispose()  # Close the database connection
            logging.info("Database connection closed.")
        except Exception as e:
            raise CustomException(e, sys)
            logging.error(f"An error occurred while closing the connection: {str(e)}")



def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception Occured in load_object function utils')
        raise CustomException(e,sys)

def calculate_scores(train_array, num_clusters):
    # Perform clustering on the training data using KMeans as an example
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(train_array)

    # Calculate the silhouette score
    silhouette_avg = silhouette_score(train_array, clusters)

    # Calculate the sizes of each cluster
    cluster_sizes = [np.sum(clusters == i) for i in range(num_clusters)]

    # Calculate the Soliot score as the ratio of the smallest to the largest cluster size
    soliot_score = min(cluster_sizes) / max(cluster_sizes)

    return silhouette_avg, soliot_score



