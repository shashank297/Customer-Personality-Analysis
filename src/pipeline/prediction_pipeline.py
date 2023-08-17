import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import pandas as pd

class PredictPipeline:

    def __init__(self):
        pass

    def predict_clusters(self, features):
        try:
            # Load the preprocessor and AgglomerativeClustering model
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join('artifacts', 'model.pkl')

            preprocessor = load_object(preprocessor_path)
            agglomerative_clustering_model = load_object(model_path)

            # Preprocess the features
            data_scaled = preprocessor.transform(features)

            # Predict cluster assignments using the agglomerative_clustering_model
            cluster_assignments = agglomerative_clustering_model.predict(data_scaled)

        except Exception as e:
            logging.info("Exception occurred in clustering prediction")
            raise CustomException(e, sys)

        return cluster_assignments


import pandas as pd
import logging


class CustomData:
    def __init__(
        self,
        Income: float,
        Customer_for: int,
        Age: int,
        Spent: int,
        Children: int,
    ):
        self.Income = Income
        self.Customer_for = Customer_for
        self.Age = Age
        self.Spent = Spent
        self.Children = Children

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'income': [self.Income],
                'customer_for': [self.Customer_for],
                'age': [self.Age],
                'spent': [self.Spent],
                'children': [self.Children]
            }

            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df

        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e,sys)


