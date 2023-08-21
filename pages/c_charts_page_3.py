import streamlit as st
from src.components.variable import dataBase
from src.utils import DatabaseManager
from st_aggrid import AgGrid
import plotly.subplots as sp
import plotly.express as px
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

def charts_page():

    def calculate_percentage_change(current_value, mean_value):
        percentage_change = ((current_value - mean_value) / mean_value) * 100
        return f"{round(percentage_change, 2)}%"
    # Initialize database connection
    DB = DatabaseManager()

    # Retrieve connection from dataBase module
    conn = dataBase.conn

    # Check if the results variable is present in the session state
    if hasattr(st.session_state, 'results'):
        results = st.session_state.results
        results = str(results)
        query = f"SELECT * FROM merge_table WHERE clusters = '{results}'"

    # Check if the form has been submitted
    if hasattr(st.session_state, 'form_submitted') and st.session_state.form_submitted:
        income = st.session_state.income
        customer_for = st.session_state.customer_for
        age = st.session_state.age
        spent = st.session_state.spent
        children = st.session_state.children

        # Execute the query to fetch data based on results
        df = DB.execute_query(query, fetch=True)

        st.title(f"Charts Page for Cluster {results}")
        st.write("Display KPIs for the Cluster with Average values within the same Cluster.")

        # Create columns for displaying KPIs
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

        # Display KPIs using st.metric()
        kpi1.metric(
        label="Income 💰",
        value=f"${round(income, 2)}",
        delta=calculate_percentage_change(income, df.income.mean()),
        )

        kpi2.metric(
            label="Days as Customer ⏳",
            value=round(customer_for),
            delta=calculate_percentage_change(customer_for, df.customer_for.mean()),
        )

        kpi3.metric(
            label="Age 🎂",
            value=round(age),
            delta=calculate_percentage_change(age, df.age.mean()),
        )

        kpi4.metric(
            label="Spent 💳",
            value=f"${round(spent, 2)}",
            delta=calculate_percentage_change(spent, df.spent.mean()),
        )

        kpi5.metric(
            label="Children 👶",
            value=round(children),
            delta=calculate_percentage_change(children, df.children.mean()),
        )

        # top-level filters
        # Create a subplot with 2 rows and 2 columns
        fig = sp.make_subplots(rows=2, cols=2, 
            subplot_titles=("Age Distribution 🎂", "Days as Customer ⏳", "spent Distribution 💳", "Income Distribution 💰"))

        # Age distribution chart
        fig.add_trace(go.Histogram(x=df['age'], marker_color='#1f77b4', xbins=dict(size=5)), row=1, col=1)

        # Days as Customer distribution chart
        fig.add_trace(go.Histogram(x=df['customer_for'], marker_color='#2ca02c', xbins=dict(size=5)), row=1, col=2)

        # Children distribution chart
        fig.add_trace(go.Histogram(x=df['spent'], marker_color='#d62728', xbins=dict(size=5)), row=2, col=1)

        # Income distribution chart
        fig.add_trace(go.Histogram(x=df['income'], marker_color='#ff7f0e', xbins=dict(size=10000)), row=2, col=2)

        # Customize the layout of the subplot
        fig.update_layout(
            title_text="Data Distributions",
            title_x=0.5,
            template="plotly_dark",  # Dark mode template
            xaxis=dict(showgrid=False),  # Hide x-axis gridlines
            yaxis=dict(showgrid=False),  # Hide y-axis gridlines
            bargap=0.2,  # Add gap between columns in the subplot
        )

        # Update individual subplot titles
        fig.update_xaxes(title_text="Value", row=1, col=1)
        fig.update_xaxes(title_text="Value", row=1, col=2)
        fig.update_xaxes(title_text="Value", row=2, col=1)
        fig.update_xaxes(title_text="Income", row=2, col=2)

        fig.update_yaxes(title_text="Frequency", row=1, col=1)
        fig.update_yaxes(title_text="Frequency", row=1, col=2)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=2)

        # Create the Streamlit layout
        st.markdown("### Data Distributions")
        st.plotly_chart(fig, use_container_width=True)






    else:
        st.warning("Please submit the form on the Home page.")

# Call the charts_page function
charts_page()
