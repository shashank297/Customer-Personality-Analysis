import streamlit as st
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

def results_page():
    st.title("Results Page")

    if hasattr(st.session_state, 'results'):
        results = st.session_state.results
    elif hasattr(st.session_state, 'form_submitted') and st.session_state.form_submitted:
        income = st.session_state.income
        customer_for = st.session_state.customer_for
        age = st.session_state.age
        spent = st.session_state.spent
        children = st.session_state.children

        data = CustomData(
            Income=income,
            Customer_for=customer_for,
            Age=age,
            Spent=spent,
            Children=children
        )

        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict_clusters(final_new_data)

        results = round(pred[0], 2)
        st.session_state['results'] = results

    if 'results' in st.session_state:
        final_new_data = data.get_data_as_dataframe()
        st.dataframe(final_new_data)
        st.write(f'### As per the above info the customer fall into Cluster {results}')
    else:
        st.warning("Please submit the form on the previous page.")
