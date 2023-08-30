import os
import sys
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from src.exception import CustomException
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from src.logger import logging
from src.utils import PostgreSQLDataHandler, save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.db = PostgreSQLDataHandler()
        self.preprocessing_obj = self.get_data_transformation_object()

    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')

            cols = ['Age', 'Spent', 'customer_for', 'children', 'income']

            logging.info('Pipeline Initiated')

            data_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler()),
                    ('pca', PCA(n_components=3))
                ]
            )

            preprocessor = ColumnTransformer([
                ('data_pipeline', data_pipeline, cols)
            ])

            logging.info('Pipeline Completed')

            return preprocessor

        except Exception as e:
            logging.error("Error in Data Transformation")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, filename):
        try:
            logging.info(f'Reading database table {filename} initiated')

            df = self.db.fetch_data(filename)
            df=df[['Age', 'Spent', 'customer_for', 'children', 'income']]

            logging.info(f'Reading database table {filename} complete')
            logging.info(f'Dataframe Head: \n{df.head().to_string()}')

            logging.info('Applying preprocessing object on training dataset')
            # train_arr = self.preprocessing_obj.fit_transform(df)
            
            train_arr=df.copy()

            logging.info('Saving preprocessor pickle file')
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=self.preprocessing_obj
            )

            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            logging.error(f'Error occurred during data transformation: {e}')
            raise CustomException(e, sys)

