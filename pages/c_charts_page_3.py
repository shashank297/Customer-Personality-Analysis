import streamlit as st
from src.components.variable import dataBase
from src.utils import DatabaseManager


def charts_page():
    DB=DatabaseManager()
    conn=dataBase.conn

    if hasattr(st.session_state, 'results'):
        results = st.session_state.results
        results=str(results)
        query=f"select * from merge_table where clusters = '{results}' "

        # df=DB.execute_query(f'select income,customer_for,age,spent,children from merge_table',fetch=True)
        df=DB.execute_query(query,fetch=True)
        st.title(f"Charts Page for cluster {results}")
        st.write("Display charts and dashboard content here.")
        st.dataframe(df.head())
    else:
         st.warning("Please submit the form on the Home page.")

