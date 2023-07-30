import os
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.components.data_process import CustomerAnalysis
from src.logger import logging
from src.utils import DatabaseManager,save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.db=DatabaseManager()

    def get_data_transformation_object(self):
        """
        Get the data transformation object.

        This function defines a data transformation pipeline to preprocess the data. It performs
        ordinal encoding and scaling on the categorical and numerical columns, respectively.

        Returns:
            preprocessor (ColumnTransformer): The preprocessor object that applies the defined
            transformations to the appropriate columns.
        """
        try:
            logging.info('Data Transformation initiated')

            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['education', 'living_with', 'is_parent']
            numerical_cols = ['income', 'kidhome', 'teenhome', 'recency', 'wines', 'fruits', 'meat',
                            'fish', 'sweets', 'gold', 'numdealspurchases', 'numwebpurchases',
                            'numcatalogpurchases', 'numstorepurchases', 'numwebvisitsmonth',
                            'acceptedcmp3', 'acceptedcmp4', 'acceptedcmp5', 'acceptedcmp1',
                            'acceptedcmp2', 'complain', 'response', 'customer_for', 'age', 'spent',
                            'children', 'family_size']

            logging.info('Pipeline Initiated')

            # Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler()),
                    ('pca', PCA(n_components=3))
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('LableEncoding', LabelEncoder()),
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

    def initaite_data_transformation(self,filename):

        # read the database table
        try:
            logging.info('reading database table initaited')

            df=self.db.execute_query(f'select * from {filename}',fetch=True)

            logging.info('reading database table complete')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            ## Trnasformating using preprocessor obj

            preprocessing_obj = self.get_data_transformation_object()

            cols_del = ['AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2', 'Complain', 'Response']
            df_train=test_df.drop(columns=drop_columns,axis=1)

            input_feature_train_arr=preprocessing_obj.fit_transform(df_train)

            logging.info("Applying preprocessing object on training and testing datasets.")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]

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
            logging.info(f'Error occurred during reading database table {filename} in data transformation')
            raise CustomException(e,sys)
            self.db.rollback_transaction()


