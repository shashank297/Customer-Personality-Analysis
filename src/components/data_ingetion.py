import sys
sys.path.append(r'c:\Python_project\Customer-Personality-Analysis')
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngetionconfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifact','test.csv')
    raw_data_path:str=os.path.join('artifact','raw.csv')

class DataIngetion:

    def __init__(self):
        self.ingestion_config=DataIngetionconfig()


