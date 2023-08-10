import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import pandas as pd

class PredictPipeline:

    def __init__(self):
        pass    
    def predict(self,features):

        try:
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            model_path=os.path.join('artifacts','model.pkl')

            preprocessor=load_object(preprocessor_path)
            model=load_object(model_path)

            data_scaled=preprocessor.transform(features)
            pred=model.predict(data_scaled)

        except Exception as e:

            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)

        return pred


import pandas as pd
import logging


class CustomData:
    def __init__(
        self,
        Education: str,
        Income: float,
        Kidhome: int,
        Teenhome: int,
        Recency: int,
        MntWines: int,
        MntFruits: int,
        MntMeatProducts: int,
        MntFishProducts: int,
        MntSweetProducts: int,
        MntGoldProds: int,
        NumDealsPurchases: int,
        NumWebPurchases: int,
        NumCatalogPurchases: int,
        NumStorePurchases: int,
        NumWebVisitsMonth: int,
        AcceptedCmp3: int,
        AcceptedCmp4: int,
        AcceptedCmp5: int,
        AcceptedCmp1: int,
        AcceptedCmp2: int,
        Complain: int,
        Response: int,
        Customer_for: int,
        Age: int,
        Spent: int,
        Living_with: str,
        Children: int,
        Family_size: int,
        Is_parent: str
    ):
        self.Education = Education
        self.Income = Income
        self.Kidhome = Kidhome
        self.Teenhome = Teenhome
        self.Recency = Recency
        self.MntWines = MntWines
        self.MntFruits = MntFruits
        self.MntMeatProducts = MntMeatProducts
        self.MntFishProducts = MntFishProducts
        self.MntSweetProducts = MntSweetProducts
        self.MntGoldProds = MntGoldProds
        self.NumDealsPurchases = NumDealsPurchases
        self.NumWebPurchases = NumWebPurchases
        self.NumCatalogPurchases = NumCatalogPurchases
        self.NumStorePurchases = NumStorePurchases
        self.NumWebVisitsMonth = NumWebVisitsMonth
        self.AcceptedCmp3 = AcceptedCmp3
        self.AcceptedCmp4 = AcceptedCmp4
        self.AcceptedCmp5 = AcceptedCmp5
        self.AcceptedCmp1 = AcceptedCmp1
        self.AcceptedCmp2 = AcceptedCmp2
        self.Complain = Complain
        self.Response = Response
        self.Customer_for = Customer_for
        self.Age = Age
        self.Spent = Spent
        self.Living_with = Living_with
        self.Children = Children
        self.Family_size = Family_size
        self.Is_parent = Is_parent

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Education': [self.Education],
                'Income': [self.Income],
                'Kidhome': [self.Kidhome],
                'Teenhome': [self.Teenhome],
                'Recency': [self.Recency],
                'MntWines': [self.MntWines],
                'MntFruits': [self.MntFruits],
                'MntMeatProducts': [self.MntMeatProducts],
                'MntFishProducts': [self.MntFishProducts],
                'MntSweetProducts': [self.MntSweetProducts],
                'MntGoldProds': [self.MntGoldProds],
                'NumDealsPurchases': [self.NumDealsPurchases],
                'NumWebPurchases': [self.NumWebPurchases],
                'NumCatalogPurchases': [self.NumCatalogPurchases],
                'NumStorePurchases': [self.NumStorePurchases],
                'NumWebVisitsMonth': [self.NumWebVisitsMonth],
                'AcceptedCmp3': [self.AcceptedCmp3],
                'AcceptedCmp4': [self.AcceptedCmp4],
                'AcceptedCmp5': [self.AcceptedCmp5],
                'AcceptedCmp1': [self.AcceptedCmp1],
                'AcceptedCmp2': [self.AcceptedCmp2],
                'Complain': [self.Complain],
                'Response': [self.Response],
                'Customer_for': [self.Customer_for],
                'Age': [self.Age],
                'Spent': [self.Spent],
                'Living_with': [self.Living_with],
                'Children': [self.Children],
                'Family_size': [self.Family_size],
                'Is_parent': [self.Is_parent]
            }

            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df

        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e,sys)


