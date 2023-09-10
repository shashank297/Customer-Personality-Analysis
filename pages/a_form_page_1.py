import streamlit as st
import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development




def form_page():
    st.markdown("# Customer Personality Analysis")
    st.markdown("## Form")

    with st.form('cluster prediction'):
        income = st.number_input('Income')
        customer_for = st.number_input('No of days customer for')
        Age = st.number_input('Age')
        Spent = st.number_input('Spent')
        children = st.number_input('Children')

        submit = st.form_submit_button('Submit')

    if submit:
        st.session_state['income'] = income
        st.session_state['customer_for'] = customer_for
        st.session_state['Age'] = Age
        st.session_state['Spent'] = Spent
        st.session_state['children'] = children
        st.session_state['form_submitted'] = True
        st.session_state.selected_demo = "Results Page"  # Set selected demo for navigation
