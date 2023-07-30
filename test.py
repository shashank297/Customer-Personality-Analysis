import os
from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA  # Import PCA
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

    def process_customer_data(self, df):
        # Your custom data transformation code here
        # ... (paste the entire code of process_customer_data function here)
        return df

    def get_data_transformation_object(self):
        try:
            logging.info('Data Transformation initiated')

            # Load or fetch your original DataFrame here
            original_df = ...  # Load your original DataFrame here

            # Apply the custom transformation function to the original DataFrame
            self.df = self.process_customer_data(original_df)

            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['Education', 'Marital_Status', 'Dt_Customer']
            numerical_cols = ['ID', 'Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency', 'MntWines', 'MntFruits',
                              'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
                              'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
                              'NumWebVisitsMonth', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1',
                              'AcceptedCmp2', 'Complain', 'Z_CostContact', 'Z_Revenue', 'Response']

            logging.info('Pipeline Initiated')

            ## Numerical Pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler()),
                    ('pca', PCA(n_components=3))  # Add PCA as a step with the desired number of components
                ]
            )

            # Categorical Pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ordinalencoder', LabelEncoder()),
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























































# df=pd.read_csv(r'C:\Python_project\Customer-Personality-Analysis\Notebook\Data\marketing_campaign.csv')

# df.drop('Unnamed: 0',axis=1,inplace=True)
# df.Dt_Customer=pd.to_datetime(df.Dt_Customer)
# dates=[]
# for i in df["Dt_Customer"]:
#     i = i.date()
#     dates.append(i)  
# #Dates of the newest and oldest recorded customer
# print("The newest customer's enrolment date in therecords:",max(dates))
# print("The oldest customer's enrolment date in the records:",min(dates))

# #Created a feature "Customer_For"
# days = []
# d1 = max(dates) #taking it to be the newest customer
# for i in dates:
#     delta = d1 - i
#     days.append(delta)
# df["Customer_For"] = days
# df["Customer_For"] = pd.to_numeric(df["Customer_For"], errors="coerce")

# for i in df.columns[df.dtypes == 'object']:
#     print(f'Total categories in the feature {i}:\n  \n',df[i].value_counts())

# # Age of customer today
# df['Age']=2023-df.Year_Birth

# #Total spendings on various items
# df["Spent"] = df["MntWines"]+ df["MntFruits"]+ df["MntMeatProducts"]+ df["MntFishProducts"]+ df["MntSweetProducts"]+ df["MntGoldProds"]

# #Deriving living situation by marital status"Alone"
# df["Living_With"]=df["Marital_Status"].replace({"Married":"Partner", "Together":"Partner", "Absurd":"Alone", "Widow":"Alone", "YOLO":"Alone", "Divorced":"Alone", "Single":"Alone",})

# #Feature indicating total children living in the household
# df["Children"]=df["Kidhome"]+df["Teenhome"]

# #Feature for total members in the householde
# df["Family_Size"] = df["Living_With"].replace({"Alone": 1, "Partner":2})+ df["Children"]

# #Feature pertaining parenthood
# df["Is_Parent"] = np.where(df.Children> 0, 1, 0)

# #Segmenting education levels in three groups
# df["Education"]=df["Education"].replace({"Basic":"Undergraduate","2n Cycle":"Undergraduate", "Graduation":"Graduate", "Master":"Postgraduate", "PhD":"Postgraduate"})

# #Renameing the column name to better understand

# data=df.rename(columns={"MntWines": "Wines","MntFruits":"Fruits","MntMeatProducts":"Meat","MntFishProducts":"Fish","MntSweetProducts":"Sweets","MntGoldProds":"Gold"},inplace=True)
# #Dropping some of the redundant features
# to_drop = ["Marital_Status", "Dt_Customer", "Z_CostContact", "Z_Revenue", "Year_Birth", "ID"]
# df.drop(to_drop, axis=1,inplace=True)

# #Dropping the outliers by setting a cap on Age and income. 
# df = df[(df["Age"]<90)]
# df = df[(df["Income"]<600000)]
# print("The total number of data-points after removing the outliers are:", len(df))

# # Filter out non-numeric columns
# data = df.select_dtypes(include=[np.number])

# # Correlation matrix
# corrmat = data.corr()

# # Create a custom color map
# cmap = sns.diverging_palette(240, 10, as_cmap=True)

# # Set the figure size
# plt.figure(figsize=(20, 20))

# # Plot the correlation matrix
# sns.heatmap(corrmat, annot=True, cmap=cmap, center=0)

# # Add a title to the plot
# plt.title('Correlation Matrix')

# # Display the plot
# plt.show()

# #Get list of categorical variables
# s = (df.dtypes == 'object')
# object_cols = list(s[s].index)

# print("Categorical variables in the dataset:", object_cols)

# #Label Encoding the object dtypes.
# LE=LabelEncoder()
# for i in object_cols:
#     df[i]=df[[i]].apply(LE.fit_transform)
    
# print("All features are now numerical")

# #Creating a copy of data
# ds = df.copy()
# # creating a subset of dataframe by dropping the features on deals accepted and promotions
# cols_del = ['AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2', 'Complain', 'Response']
# ds = ds.drop(cols_del, axis=1)
# #Scaling
# scaler = StandardScaler()
# scaler.fit(ds)
# scaled_ds = pd.DataFrame(scaler.transform(ds),columns= ds.columns )
# print("All features are now scaled")

# #Initiating PCA to reduce dimentions aka features to 3
# pca = PCA(n_components=3)
# pca.fit(scaled_ds)
# PCA_ds = pd.DataFrame(pca.transform(scaled_ds), columns=(["col1","col2", "col3"]))

# # Quick examination of elbow method to find numbers of clusters to make.
# print('Elbow Method to determine the number of clusters to be formed:')
# Elbow_M = KElbowVisualizer(KMeans(), k=10)
# Elbow_M.fit(PCA_ds)
# Elbow_M.show()

# #Initiating the Agglomerative Clustering model 
# AC = AgglomerativeClustering(n_clusters=4)
# # fit model and predict clusters
# yhat_AC = AC.fit_predict(PCA_ds)
# PCA_ds["Clusters"] = yhat_AC
# #Adding the Clusters feature to the orignal dataframe.
# data["Clusters"]= yhat_AC

# data.describe()