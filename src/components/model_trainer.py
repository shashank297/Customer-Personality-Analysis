# Basic Import
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
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
    trained_model_file_path:str = os.path.join('artifacts','model.pkl')

class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.db=DatabaseManager()
        self.conn=dataBase.conn

    def initiate_model_training(self,train_array,tablename):

        try:
            logging.info('Initate model traning')

            AC = AgglomerativeClustering(n_clusters=4)
            yhat_AC = AC.fit_predict(train_array)

            logging.info('Model is trained successfully')
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=AC
            )

            logging.info('Modeal.pkl file as been save')

            df=self.db.execute_query(f'select * from {tablename}',fetch=True)
            df["Clusters"]=yhat_AC

            merge_table='merge_table'
            logging.info(f'Initiateing table Uploding to the database as a {merge_table}')
            
            self.db.create_table(df=df,table_name=merge_table)
            self.db.execute_values(df,merge_table)

            logging.info(f'table has been uploded to the database with table name {merge_table}')
            

        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise CustomException(e,sys)