import os
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.components.data_process import CustomerAnalysis
from src.logger import logging
from src.utils import DatabaseManager

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')

            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['Education', 'Marital_Status', 'Dt_Customer']
            numerical_cols = ['ID', 'Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency', 'MntWines', 'MntFruits',
                              'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
                              'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
                              'NumWebVisitsMonth', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1',
                              'AcceptedCmp2', 'Complain', 'Z_CostContact', 'Z_Revenue', 'Response']

            # # Define the custom ranking for each ordinal variable
            # cut_categories = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
            # color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            # clarity_categories = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']

            logging.info('Pipeline Initiated')

            ## Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ordinalencoder', OrdinalEncoder(categories=[cut_categories, color_categories, clarity_categories])),
                    ('scaler', StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipeline', cat_pipeline, categorical_cols)
            ])

            logging.info('Pipeline Completed')
            
            return preprocessor

        except Exception as e:
            logging.info("Error in Data Transformation")
            raise CustomException(e, sys)
