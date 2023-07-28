import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering

from datetime import datetime

class CustomerAnalysis:
    def __init__(self, df):
        self.df = df
    
    def process_customer_data(self):
        self.df.dropna(inplace=True)
        # Convert 'Dt_Customer' column to datetime
        self.df['Dt_Customer'] = pd.to_datetime(self.df['Dt_Customer'])

        # Calculate the newest and oldest recorded customer dates
        newest_customer_date = self.df['Dt_Customer'].max()
        oldest_customer_date = self.df['Dt_Customer'].min()

        # Create a new feature 'Customer_For' indicating the number of days since customer registration relative to the newest customer
        self.df['Customer_For'] = (newest_customer_date - self.df['Dt_Customer']).dt.days

        # Calculate the customer's age as of today (using dynamic current year)
        current_year = datetime.now().year
        self.df['Age'] = current_year - self.df['Year_Birth']

        # Calculate total spendings on various items
        self.df['Spent'] = self.df[['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].sum(axis=1)

        # Derive living situation by marital status
        self.df['Living_With'] = self.df['Marital_Status'].replace({"Married": "Partner", "Together": "Partner", "Absurd": "Alone", "Widow": "Alone", "YOLO": "Alone", "Divorced": "Alone", "Single": "Alone"})

        # Create a feature indicating total children living in the household
        self.df['Children'] = self.df['Kidhome'] + self.df['Teenhome']

        # Create a feature for total members in the household
        self.df['Family_Size'] = self.df['Living_With'].replace({"Alone": 1, "Partner": 2})

        # Create a feature indicating parenthood
        self.df['Is_Parent'] = np.where(self.df['Children'] > 0, 1, 0)

        # Segment education levels into three groups
        self.df['Education'] = self.df['Education'].replace({"Basic": "Undergraduate", "2n Cycle": "Undergraduate", "Graduation": "Graduate", "Master": "Postgraduate", "PhD": "Postgraduate"})

        # Convert 'Customer_For' column to numeric
        self.df['Customer_For'] = pd.to_numeric(self.df['Customer_For'], errors="coerce")

        # Rename the column names for better understanding
        self.df.rename(columns={
            "MntWines": "Wines",
            "MntFruits": "Fruits",
            "MntMeatProducts": "Meat",
            "MntFishProducts": "Fish",
            "MntSweetProducts": "Sweets",
            "MntGoldProds": "Gold"
        }, inplace=True)

        # Drop some of the redundant features
        to_drop = ["Marital_Status", "Dt_Customer", "Z_CostContact", "Z_Revenue", "Year_Birth", "ID"]
        self.df.drop(to_drop, axis=1, inplace=True)

        data = self.df.select_dtypes(include=[np.number])

        return self.df, data
    
    def preprocess_and_reduce_dimensionality(self):
        # Get list of categorical variables
        s = (self.df.dtypes == 'object')
        object_cols = list(s[s].index)

        # Label Encoding the object dtypes.
        LE = LabelEncoder()
        for i in object_cols:
            self.df[i] = LE.fit_transform(self.df[i])

        # Creating a copy of data
        ds = self.df.copy()

        # Create a subset of the DataFrame by dropping the features on deals accepted and promotions
        cols_del = ['AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Complain', 'Response']
        ds = ds.drop(cols_del, axis=1)

        # Scaling the data using StandardScaler
        scaler = StandardScaler()
        scaler.fit(ds)
        scaled_ds = pd.DataFrame(scaler.transform(ds), columns=ds.columns)

        # Initiating PCA to reduce dimensions (features) to 3
        pca = PCA(n_components=3)
        pca.fit(scaled_ds)
        PCA_ds = pd.DataFrame(pca.transform(scaled_ds), columns=["PCA1", "PCA2", "PCA3"])
        self.reduced_data=PCA_ds
        return PCA_ds

    def perform_clustering(self, num_clusters=4):
        # Initiating the Agglomerative Clustering model 
        AC = AgglomerativeClustering(n_clusters=num_clusters)

        # Fit model and predict clusters
        yhat_AC = AC.fit_predict(self.reduced_data)
        self.df["Clusters"] = yhat_AC
        return self.df

# Sample usage:
# Assuming 'data_file' is the path to the CSV file containing customer data
# df=pd.read_csv(r'C:\Python_project\Customer-Personality-Analysis\Notebook\Data\marketing_campaign.csv')
# customer_analysis = CustomerAnalysis(df=df)
# customer_analysis.process_customer_data()
# reduced_data = customer_analysis.preprocess_and_reduce_dimensionality()
# customer_analysis.perform_clustering(num_clusters=4)

