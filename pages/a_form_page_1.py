import streamlit as st

def form_page():
    st.title("Form Page")

    with st.form('cluster prediction'):
        income = st.number_input('Income')
        customer_for = st.number_input('No of days customer for')
        age = st.number_input('Age')
        spent = st.number_input('Spent')
        children = st.number_input('Children')

        submit = st.form_submit_button('Submit')

    if submit:
        st.session_state['income'] = income
        st.session_state['customer_for'] = customer_for
        st.session_state['age'] = age
        st.session_state['spent'] = spent
        st.session_state['children'] = children
        st.session_state['form_submitted'] = True
        st.session_state.selected_demo = "Results Page"  # Set selected demo for navigation
