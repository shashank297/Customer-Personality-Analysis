import os
from dataclasses import dataclass
import pandas as pd
import numpy as np
import sys
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from src.exception import CustomException
from src.logger import logging
from src.utils import DatabaseManager, save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.db = DatabaseManager()

    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')

            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['education', 'living_with', 'is_parent']
            numerical_cols = ['income', 'kidhome', 'teenhome', 'recency', 'wines', 'fruits', 'meat',
                              'fish', 'sweets', 'gold', 'numdealspurchases', 'numwebpurchases',
                              'numcatalogpurchases', 'numstorepurchases', 'numwebvisitsmonth',
                              'customer_for', 'age', 'spent','children', 'family_size']

            logging.info('Pipeline Initiated')

            # Single Pipeline for both numerical and categorical features
            data_pipeline = Pipeline(
                steps=[
                    ('imputer_num', SimpleImputer(strategy='median')),  # Imputer for numerical columns
                    ('imputer_cat', SimpleImputer(strategy='most_frequent')),  # Imputer for categorical columns
                    ('scaler', StandardScaler()),  # StandardScaler for both types of columns
                    ('pca', PCA(n_components=3))  # PCA for numerical columns
                ]
            )

            preprocessor = ColumnTransformer([
                ('data_pipeline', data_pipeline, numerical_cols + categorical_cols)  # Combine all columns
            ])

            logging.info('Pipeline Completed')

            return preprocessor

        except Exception as e:
            logging.info("Error in Data Transformation")
            raise CustomException(e,sys)

    def initiate_data_transformation(self, filename):
        # Read the database table
        try:
            logging.info(f'Reading database table {filename} initiated')

            df = self.db.execute_query(f'select * from {filename}', fetch=True)

            logging.info(f'Reading database table {filename} complete')
            logging.info(f'Dataframe Head: \n{df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            # Transforming using preprocessor object
            preprocessing_obj = self.get_data_transformation_object()

            # Drop the specified columns from the DataFrame
            cols_del = ['acceptedcmp3', 'acceptedcmp4', 'acceptedcmp5', 'acceptedcmp1',
                        'acceptedcmp2', 'complain', 'response']
            df_train = df.drop(columns=cols_del, axis=1)

            input_feature_train_arr = preprocessing_obj.fit_transform(df_train)

            logging.info("Applying preprocessing object on training datasets.")

            # train_arr = np.c_[input_feature_train_arr, np.array(input_feature_train_arr)]
            train_arr = input_feature_train_arr
            logging.info(train_arr)
            # self.db.create_table(train_arr,'pca')
            # self.db.execute_values(train_arr,'pca')

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            logging.info(f'Error occurred during reading database table {filename} in data transformation error: {e}')
            raise CustomException(e,sys)
            # Optionally, you can rollback the transaction here if necessary
            self.db.rollback_transaction()


# a=DataTransformation()
# a.initiate_data_transformation('cleaned_data')