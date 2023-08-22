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
        df.family_size.replace({1:'Single',2:'Partner'},inplace=True)

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
        fig.update_layout(showlegend=False)
        fig.update_layout(height=800, width=800)

        # Create the Streamlit layout
        st.markdown("### Data Distributions")
        st.plotly_chart(fig, use_container_width=True)
        
        
        # Create subplots with two columns and one row, specifying the subplot types
        fig1 = sp.make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'sunburst'}]], subplot_titles=("Children Ratio", "Spending vs Income"))

        # First Chart - Pie Chart
        children_counts = df['children'].value_counts()
        fig1.add_trace(go.Pie(
            labels=children_counts.index,
            values=children_counts.values,
            marker=dict(colors=px.colors.sequential.RdBu),
            textinfo='percent+label',
            textfont_size=20,
            marker_line=dict(color='white', width=2)
        ), row=1, col=1)


        sunburst_fig = px.sunburst(df, path=['family_size', 'education', 'children'], values='spent', color='education')
        sunburst_trace = sunburst_fig['data'][0]
        fig1.add_trace(sunburst_trace, row=1, col=2)

          # Customize the layout
        fig1.update_layout(
            showlegend=True,
            height=500,
            width=1000,
        )

        fig1.update_layout(showlegend=False)

        # Create the Streamlit layout
        st.markdown("### Children Ratio and Spending vs Income")
        st.plotly_chart(fig1, use_container_width=True)

        

        cluster_purchases=df[['numdealspurchases','numwebpurchases','numcatalogpurchases','numstorepurchases','numwebvisitsmonth']].sum()
        cam=df[['acceptedcmp1', 'acceptedcmp2', 'acceptedcmp3', 'acceptedcmp4','acceptedcmp5', 'response']].sum()
        # Create subplots with 2 rows and 1 column
        fig2 = sp.make_subplots(rows=1, cols=2,subplot_titles=("Segment-wise distribution on total purchases.", "campaign distribution"))

        # Assuming cluster_purchases is your DataFrame with cluster-wise purchases
        fig2.add_trace(
            go.Bar(
                x=cluster_purchases.index,
                y=cluster_purchases.values,
                marker_color=['#dc4c4c', '#157394', '#589cb4', '#bcb4ac', '#3c444c'],
                text=cluster_purchases.values,
                texttemplate='%{text:.2s}',
                textposition='outside',
                name='Cluster Purchases'
            ),
            row=1, col=1
        )

        # Customize the first subplot
        fig2.update_xaxes(categoryorder='total ascending', tickangle=45, title_text='Category', title_font=dict(size=18), row=1, col=1)
        fig2.update_yaxes(title_text='Purchases', title_font=dict(size=18), row=1, col=1)

        # Assuming cam is your DataFrame with campaign-wise purchases
        fig2.add_trace(
            go.Bar(
                x=cam.index,
                y=cam.values,
                marker_color=['#dc4c4c', '#157394', '#589cb4', '#bcb4ac', '#3c444c','#3c444c'],
                text=cam.values,
                texttemplate='%{text:.2s}',
                textposition='outside',
                showlegend=False
            ),
            row=1, col=2
        )

        # Customize the second subplot
        fig2.update_xaxes(categoryorder='total ascending', tickangle=45, title_text='Campaigns', title_font=dict(size=18), row=1, col=2)
        fig2.update_yaxes(title_text='No. of people', title_font=dict(size=18), row=1, col=2)

        fig2.update_layout(showlegend=False)

        # Set layout properties for the entire figure
        fig2.update_layout(height=600, width=800)

        st.markdown("### Segment-wise distribution on total purchases and campaign distribution.")
        st.plotly_chart(fig2, use_container_width=True)



        # Create a subplot
        fig3 = sp.make_subplots(rows=1, cols=2, specs=[[{'type': 'scatter'}, {'type': 'sunburst'}]], subplot_titles=("Scatter Plot", "Sunburst Plot"))

        # df.income=df.income[df.income<200000]
        # df.family_size.replace({1:'Single',2:'Partner'},inplace=True)

                # Second Chart - Scatter Plot
        scatter_trace = px.scatter(df, x='income', y='spent', color='family_size', color_discrete_sequence=px.colors.qualitative.Set1).data[0]
        fig3.add_trace(scatter_trace, row=1, col=1)


        # Update subplot layout for the second chart
        fig3.update_xaxes(title_text="Income", row=1, col=2)
        fig3.update_yaxes(title_text="Total Spendings", row=1, col=2)

        # Sunburst plot
        sunburst_fig = px.sunburst(df, path=['family_size', 'education', 'children'], values='spent', color='education')
        sunburst_trace = sunburst_fig['data'][0]
        fig3.add_trace(sunburst_trace, row=1, col=2)

        # Customize the layout
        fig3.update_layout(
            showlegend=True,
            height=500,
            width=1000,
        )

        st.markdown("### Segment-wise distribution on total purchases and campaign distribution.")
        st.plotly_chart(fig3, use_container_width=True)

        st.dataframe(df)








    else:
        st.warning("Please submit the form on the Home page.")

# Call the charts_page function
charts_page()
