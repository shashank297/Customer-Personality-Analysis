import os
import sys
from src.components.data_ingetion import DataIngestion
from src.components.data_process import DataCleaning
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
import pandas as pd



if __name__=='__main__':
    obj=DataIngestion()
    table_name=obj.initiate_data_ingestion()
    DataProcess=DataCleaning()
    cleantable_name,Without_encoding=DataProcess.process_data_and_reduce_dimensionality(table_name)
    data_transformation=DataTransformation()
    train_df,_=data_transformation.initiate_data_transformation(cleantable_name)
    model_trainer=ModelTrainer()
    model_trainer.initiate_model_training(train_df,Without_encoding)