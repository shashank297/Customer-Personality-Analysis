import streamlit as st
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

def results_page():
    st.title("Results Page")

    if st.session_state.form_submitted:
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

        if results == 0:
            results = 'Bronze'
        elif results == 1:
            results = 'Gold'
        elif results == 2:
            results = 'Silver'
        elif results == 3:
            results = 'Platinum'
        else:
            results = None

        st.session_state.results = results

        st.dataframe(final_new_data)
        st.write(f'### As per the above info the customer falls into Cluster {results}')
    else:
        st.warning("Please submit the form on the previous page.")

if __name__ == '__main__':
    results_page()
