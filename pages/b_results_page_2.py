import streamlit as st
from src.logger import logging
import time
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

def results_page():
    st.title("Results Page")

    try:
        if st.session_state.form_submitted:
            income = st.session_state.income
            customer_for = st.session_state.customer_for
            Age = st.session_state.Age
            Spent = st.session_state.Spent
            children = st.session_state.children

            data = CustomData(
                Income=income,
                Customer_for=customer_for,
                Age=Age,
                Spent=Spent,
                Children=children
            )

            start_time = time.time()

            final_new_data = data.get_data_as_dataframe()
            predict_pipeline = PredictPipeline()
            pred = predict_pipeline.predict_clusters(final_new_data)

            results = round(pred[0], 2)

            end_time = time.time()
            execution_time = end_time - start_time

            logging.info(f"Execution time to predict the cluster with predict pipeline pipeline: {execution_time} seconds")

            if results == 3:
                results = 'Bronze'
            elif results == 2:
                results = 'Gold'
            elif results == 1:
                results = 'Silver'
            elif results == 0:
                results = 'Platinum'


            st.session_state.results = results

            st.dataframe(final_new_data)
            st.write(f'### As per the above info the customer falls into Cluster {results}')
        else:
            st.warning("Please submit the form on the previous page.")
    except Exception as e:
        st.warning("Please submit the form on the previous page.")

results_page()
