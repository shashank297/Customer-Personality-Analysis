
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

## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/cad56c93-d0a3-4f23-9ba0-22672b58086f" width="32" height="32" alt="Customer Personality Analysis"> Tech Stack Used
1. Python
2. Moduler Programing
3. Used Logging
5. PostgreSQL Database (GCP)
6. GitHub Action (CI/CD)
7. Streamlit (Website)
8. scikit-learn
9. Docker
10. Github
11. AWS ECR (private image)
12. AWS EC2 (VM)


## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/befd6434-b0dc-4843-8f48-05335476b8e7" width="32" height="32" alt="Customer Personality Analysis"> Directory Structure

```
│   Dockerfile
│   home.py
│   README.md
│   requirements.txt
│   setup.py
│
├───.github
│   └───workflows
│           main.yaml
│
├───artifacts
│       model.pkl
│       preprocessor.pkl
│
├───docs
│       Architecture_Final.pdf
│       CPA_HLD.pdf
│       Detail project report.pdf
│       Low Level Design.pdf
│       Wireframe Documentation_CPA.pdf
│
├───logs
├───Notebook
│   │   Agglomerative Clustering.ipynb
│   │   KMeans Clustering.ipynb
│   │
│   └───Data
│           marketing_campaign.csv
│
├───pages
│       a_form_page_1.py
│       b_results_page_2.py
│       c_charts_page_3.py
│       d_Make_own_chart.py
│
└───src
    │   exception.py
    │   logger.py
    │   utils.py
    │   __init__.py
    │
    ├───components
    │       data_ingetion.py
    │       data_process.py
    │       data_transformation.py
    │       model_trainer.py
    │       variable.py
    │       __init__.py
    │
    └───pipeline
            prediction_pipeline.py
            training_pipeline.py
            __init__.py
```

## Watch Our Project in Action



https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/55b8b2f0-89a1-4a66-ba5c-16595d29b815



            



## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/a925db2c-4b89-4376-aa6d-e91d2c2fd4b9" width="32" height="32" alt="Customer Personality Analysis"> Flow Chart

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/4fc24359-1e5c-44f5-9a45-7216359867a8)

### Feature Engineering 
![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/fd755ab7-b840-476d-abd6-92b2dcd0ae04)

### Data Cleaning
![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/8a9b3dda-264f-48db-9e83-e03137ca80fb)

### Data Transformation flow
![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/910e32cc-7e91-4950-b3a2-37ea4ebec0ea)

### Traning Pipeline Flow
![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/a9f1f869-bb08-42f8-94f7-85ca29ee5be3)

### Prediction Pipeline Flow
![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/3c06499d-88eb-4839-bdca-b43e06694fe1)

### CI/ CD Flow
![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/991630c9-79ca-41ca-ba06-b0a285373190)




## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/4944f33a-6b3e-472b-a750-f1b61a07e0f0"  width="32" height="32"> What We Got From This Project
- What are the statistical characteristics of the customers?
- What are the spending habits of the customers?
- Are there some products that need more marketing?
- How the marketing can be made effective?

## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/ed57b5bf-527a-4af3-b83b-34bc898abc8f"  width="32" height="32"> Step Inside The Project
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

 ## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/cb8f2bbe-6b24-4e2e-8013-36c9b2f63719"  width="32" height="32"> Conclusion
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

## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/7a1a27d2-ae60-457a-b1eb-11be3b77d6e4"  width="32" height="32"> Answering Question

**What are the statistical characteristics of the customers?**

The company's customers are mostly married. There are more Middle Aged Adults, aged between 40 and 60, and most of them like to have one child. Most of the customers hold bachelor degrees and their earnings are mostly between 25,000 and 85,000.

**What are the spending habits of the customers?**

Customers have spent more on wine and meat products. Those without children have spent more than those having children. Singles are spending more than the ones with the partners. Middle-aged adults have spent more than the other age groups. Store shopping is the preferred channel for purchasing among customers. Web and Catalog purchasing also have potential.


**Are there some products that need more marketing?**

Sweets and Fruits need some effective marketing. The company needs to run promotions for these products in order to increase the revenue from these products. Baskets of the least-selling products combined with the most-selling products can be effective.

**How marketing can be made effective?**

As a marketing recommendation give coupons to the old and high-spending customers. Market cheap and on-offer products to low-income and low-spending customers. Web purchasing has some potential. To unlock this give special discounts to the customers who sign up on the company's website.

## <img src="https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/434aee4c-74d3-4abd-ab71-3fccf1c22d6e" width="32" height="32" > Streamlit App




![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/7b4ea346-18f6-4dac-a711-917fba583b10)

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/84a02abf-eaf6-4676-a971-02a22abc0fb6)

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/43e82c56-8886-4182-834c-91bbc8e7d3c7)

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/b7e2e9b2-a4e9-4787-ae18-1b2cb2279906)

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/c31a5fc4-fc4b-4e42-8c7b-1f24e8b5ad54)

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/2e1b2d58-4d76-4802-a3f4-a1c1c21d2960)

![image](https://github.com/shashank297/Customer-Personality-Analysis/assets/67503481/cc22011d-a779-43c7-a40a-31bd3567a8e2)








