
<img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/46ccfeb9-28b2-4740-9d2f-36a85b714031" width="1600" height="300" alt="Customer Personality Analysis">



# <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/5b970ab3-07aa-4e99-ae36-61b09be7001e" width="32" height="32" alt="Customer Personality Analysis"> Customer Personality Analysis

Customer Personality Analysis is a detailed analysis of a company’s ideal customers. It helps a business to better understand its customers and makes it easier for them to modify products according to the specific needs, behaviors, and concerns of different types of customers.



## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/64d46879-adb9-4fe4-bd55-09917409c2c3" width="32" height="32" alt="Customer Personality Analysis"> Problem Statement


Customer Personality Analysis is a detailed analysis of a company’s ideal customers. It helps a business to better understand its customers and makes it easier for them to modify products according to the specific needs, behaviors and concerns of different types of customers. 
Customer personality analysis helps a business to modify its product based on its target customers from different types of customer segments. For example, instead of spending money to market a new product to every customer in the company’s database, a company can analyze which customer segment is most likely to buy the product and then market the product only on that particular segment. 
The main objective here is - 
1. What people say about your product: what gives customers’ attitude towards the  product. 
2. What people do: which reveals what people are doing rather than what they are  saying about your product.


## ![target](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/0d440085-c282-408b-85cd-7f499628c170) Project Objectives

1. **Customer Sentiment Analysis**: Understand customers' attitudes towards the product.
2. **Behavior Analysis**: Analyze what customers are doing rather than what they are saying about the product.


## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/a925db2c-4b89-4376-aa6d-e91d2c2fd4b9" width="32" height="32" alt="Customer Personality Analysis"> Flow Chart

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/4fc24359-1e5c-44f5-9a45-7216359867a8)

## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/befd6434-b0dc-4843-8f48-05335476b8e7" width="32" height="32" alt="Customer Personality Analysis"> Directory Structure

| Directory/File                  | Description                               |
|---------------------------------|-------------------------------------------|
| `.github/workflows/main.yaml`   | GitHub Actions workflow configuration.    |
| `artifacts/model.pkl`           | Saved machine learning model.            |
| `artifacts/preprocessor.pkl`    | Saved data preprocessor.                 |
| `docs/CPA_HLD.pdf`              | Documentation: High-Level Design PDF.    |
| `docs/Low Level Design.docx`    | Documentation: Low-Level Design DOCX.    |
| `logs/`                         | Directory for log files.                 |
| `Notebook/Data/`                | Data storage for Jupyter Notebooks.      |
| `Notebook/logs/Agglomerative Clustering.ipynb` | Jupyter Notebook for Agglomerative Clustering. |
| `Notebook/logs/KMeans Clustering.ipynb` | Jupyter Notebook for KMeans Clustering. |
| `pages/a_form_page_1.py`        | Python file for a form page.             |
| `pages/b_results_page_2.py`     | Python file for a results page.          |
| `pages/c_charts_page_3.py`      | Python file for a charts page.           |
| `pages/d_Make_own_chart.py`     | Python file for making custom charts.    |
| `src/components/data_ingestion.py` | Python file for data ingestion.         |
| `src/components/data_process.py` | Python file for data processing.        |
| `src/components/data_transformation.py` | Python file for data transformation. |
| `src/components/model_trainer.py` | Python file for model training.         |
| `src/components/variable.py`    | Python file for component variables.     |
| `.gitignore`                    | Git ignore file for specifying ignored files and directories. |
| `Dockerfile`                    | Configuration file for Docker.           |
| `home.py`                       | Main Python script for the project.      |
| `README.md`                     | Project's README file.                   |
| `requirements.txt`              | List of Python dependencies for the project. |
| `setup.py`                      | Setup script for packaging the project.  |




## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/4944f33a-6b3e-472b-a750-f1b61a07e0f0"  width="32" height="32"> What We Got From This Project
- What are the statistical characteristics of the customers?
- What are the spending habits of the customers?
- Are there some products that need more marketing?
- How the marketing can be made effective?

## Step Inside The Project
- Exploratory Data Analysis (EDA)
- Data Ingestion
- Data Transformation
- Data Pre-processing
- Model Building
- Training Pipeline
- Prediction pipeline
- Streamlit app
- CI/CD Pipeline Integration with Docker, Amazon ECR, GitHub Actions, and AWS 
EC2
  - Docker Build Integration
  - Amazon Elastic Container Registry (ECR)

 ## Conclusion
- Most of the customers are university graduates.
- Most of the customers are living with partners.
- Those living alone have spent more than those living with partners.
- Most of the customers have only one child.
- Those having no children have spent more.
- Middle Age Adults, aged between 40 and 60, are a famous age group category.
- Middle Age Adults are spending on average, more than the other age groups.
- Most of the customers are earning between 25000 and 85000.
- Wine and Meat products are very famous among the customers.
- On the basis of income and total spending, customers are divided into 4 clusters i.e. Platinum, Gold, Silver, and Bronze.
- Most of the customers fall into the Silver and Gold categories.
- Those who are earning more are also spending more.
- Most of the customers like to buy from stores and then online from the web.
- Platinum customers showed more acceptance towards promotion campaigns while bronze customers had the least interest.

## Answering Question
What are the statistical characteristics of the customers?
The company's customers are mostly married. There are more Middle Aged Adults, aged between 40 and 60, and most of them like to have one child. Most of the customers hold bachelor degrees and their earnings are mostly between 25,000 and 85,000.

What are the spending habits of the customers?
Customers have spent more on wine and meat products. Those without children have spent more than those having children. Singles are spending more than the ones with the partners. Middle-aged adults have spent more than the other age groups. Store shopping is the preferred channel for purchasing among customers. Web and Catalog purchasing also have potential.

Are there some products that need more marketing?
Sweets and Fruits need some effective marketing. The company needs to run promotions for these products in order to increase the revenue from these products. Baskets of the least-selling products combined with the most-selling products can be effective.

How marketing can be made effective?
As a marketing recommendation give coupons to the old and high-spending customers. Market cheap and on-offer products to low-income and low-spending customers. Web purchasing has some potential. To unlock this give special discounts to the customers who sign up on the company's website.
