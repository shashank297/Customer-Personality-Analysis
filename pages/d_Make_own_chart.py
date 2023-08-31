import pygwalker as pyg
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
from src.utils import PostgreSQLDataHandler

def custom_chart(data_frame):
    st.title("Make Own Your On Chart")

    # Generate the HTML using Pygwalker
    pyg_html = pyg.walk(data_frame, return_html=True)
    
    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)

def c_main():

    pg = PostgreSQLDataHandler()
    df = pg.fetch_data('merge_table')

    custom_chart(df)


c_main()
