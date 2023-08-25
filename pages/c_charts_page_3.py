import streamlit as st
from src.components.variable import dataBase
import pandas as pd
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
        children_counts=df.children.value_counts()
        education_counts=df.education.value_counts()
        living_with_counts=df.living_with.value_counts()
        agegroup_counts=df.agegroup.value_counts()

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
        fig = sp.make_subplots(rows=1, cols=4, 
            subplot_titles=("Age Distribution 🎂", "Days as Customer ⏳", "spent Distribution 💳", "Income Distribution 💰"))

        # Age distribution chart
        fig.add_trace(go.Histogram(x=df['age'], marker_color='#b43058', xbins=dict(size=5)), row=1, col=1)

        # Days as Customer distribution chart
        fig.add_trace(go.Histogram(x=df['customer_for'], marker_color='#d35454', xbins=dict(size=5)), row=1, col=2)

        # Children distribution chart
        fig.add_trace(go.Histogram(x=df['spent'], marker_color='#b2182b', xbins=dict(size=5)), row=1, col=3)

        # Income distribution chart
        fig.add_trace(go.Histogram(x=df['income'], marker_color='#e28f71', xbins=dict(size=10000)), row=1, col=4)

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
        fig.update_layout(height=400, width=1000)

        # Create the Streamlit layout
        st.markdown("### Data Distributions")
        st.plotly_chart(fig, use_container_width=True)


        products = df[['wines', 'fruits', 'meat', 'fish', 'sweets', 'gold']]
        product_means = products.mean(axis=0).sort_values(ascending=False)
        product_means_df = pd.DataFrame(list(product_means.items()), columns=['Product', 'Average Spending'])

        # Create a Plotly bar chart for product spending
        trace2 = go.Bar(
            x=product_means_df['Average Spending'],
            y=product_means_df['Product'],
            orientation='h',
            marker=dict(color=['#e28f71', '#b43058', '#57274e', '#472345', '#d35454', '#b2182b']),  # Custom colors
        )

        layout2 = go.Layout(
            title='Average Spending on Products',
            xaxis=dict(title='Average Spending'),
            yaxis=dict(title='Product'),
            margin=dict(l=100, r=50, b=80, t=50),  # Adjust margins as needed
        )

        fig2 = go.Figure(data=[trace2], layout=layout2)

        # Calculate average spending by age group
        agegroupspending = df.groupby('agegroup')['spent'].mean().reset_index()

        # Replace 'Alone' with 'Single' in the 'living_with' column
        df['living_with'] = df['living_with'].str.replace('Alone', 'Single')

        # Group by 'living_with' and calculate the mean of 'spent'
        maritalspending = df.groupby('living_with')['spent'].mean().reset_index()
        maritalspending = maritalspending.sort_values(by='spent', ascending=False)

        # Create a Plotly bar chart for marital spending
        trace1 = go.Bar(
            x=maritalspending['spent'],
            y=maritalspending['living_with'],
            orientation='h',
            marker=dict(color='rgb(255, 99, 71)'),  # Use the 'rocket' palette color
        )

        layout1 = go.Layout(
            title='Average Spending by Marital Status',
            xaxis=dict(title='Average Spending'),
            yaxis=dict(title='Marital Status'),
            margin=dict(l=150),  # Adjust the left margin for longer labels
        )

        fig1 = go.Figure(data=[trace1], layout=layout1)

        # Create the age spending bar chart
        agegroupspending = agegroupspending.sort_values(by='spent', ascending=False)

        age_spending = go.Figure()

        age_spending.add_trace(go.Bar(
            x=agegroupspending['spent'],
            y=agegroupspending['agegroup'],
            orientation='h',
            marker=dict(color=['#e28f71', '#b43058', '#57274e']),
        ))

        age_spending.update_layout(
            title='Average Spending by Age Group',
            xaxis=dict(title='Average Spending'),
            yaxis=dict(title='Age Group'),
            font=dict(size=12),
            showlegend=False,
            margin=dict(l=50, r=50, b=50, t=50),
        )

        # Create a subplot with 1 row and 3 columns
        fig6 = sp.make_subplots(rows=1, cols=3, subplot_titles=('Average Spending by Age Group', 'Average Spending by Marital Status', 'Average Spending on Products'))

        # Add the age spending chart to the first column of the subplot
        fig6.add_trace(go.Bar(
            x=agegroupspending['spent'],
            y=agegroupspending['agegroup'],
            orientation='h',
            marker=dict(color=['#e28f71', '#b43058', '#57274e']),
        ), row=1, col=1)

        # Add the marital spending chart to the second column of the subplot
        fig6.add_trace(go.Bar(
            x=maritalspending['spent'],
            y=maritalspending['living_with'],
            orientation='h',
            marker=dict(color=['#b43058', '#57274e', '#472345', '#d35454', '#b2182b']),
        ), row=1, col=2)

        # Add the product spending chart to the third column of the subplot
        fig6.add_trace(go.Bar(
            x=product_means_df['Average Spending'],
            y=product_means_df['Product'],
            orientation='h',
            marker=dict(color=['#e28f71', '#b43058', '#57274e', '#472345', '#d35454', '#b2182b']),
        ), row=1, col=3)

        fig6.update_layout(
            yaxis=dict(tickfont=dict(size=12)),
            xaxis=dict(tickfont=dict(size=12)),
            height=300,
            width=1200,
            showlegend=False,
        )

        # Show the combined subplot
        st.markdown("### Average Spending")
        st.plotly_chart(fig6, use_container_width=True)

        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("#### Percentage Wise Age Distribution")
            age_group = px.pie(labels = agegroup_counts.index, values = agegroup_counts.values, names = agegroup_counts.index)
            age_group.update_traces(textposition = 'inside', 
                  textinfo = 'percent + label', 
                  hole = 0.4, 
                  marker = dict(colors = ['#57274e', '#b2182b'  , '#b43058','#d35454'], 
                                line = dict(color = 'white', width = 2)))

            age_group.update_layout(annotations = [dict(text = 'Age Groups', 
                                                x = 0.5, y = 0.5, font_size = 20, showarrow = False,                                       
                                                font_color = 'white')],
                            showlegend = False)
            
            st.write(age_group)
        
        with fig_col2:
            st.markdown("#### Segregation Based On Relationship, Education, Children")
            
            # Create the customized sunburst chart
            sunburst_fig = px.sunburst(df, path=['family_size', 'education', 'children'], values='spent', color='education',
                                        color_discrete_sequence=['#57274e', '#b2182b', '#b43058', '#d35454'],
                                        custom_data=['spent', 'family_size', 'education', 'children'])
            
            # Customize the text color to white
            sunburst_fig.update_traces(textinfo='label+percent parent', insidetextfont=dict(color='white'))
            
            # Customize the hover template
            sunburst_fig.update_traces(hovertemplate='<b>%{label}</b><br>Spent: %{customdata[0]}<extra></extra>')
            
            # Customize the separation border color to white
            sunburst_fig.update_traces(marker_line=dict(color='white', width=1))
            
            sunburst_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',
                                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', sunburstcolorway=['white'])
            
            # Display the customized sunburst chart
            st.plotly_chart(sunburst_fig)


        

        cluster_purchases=df[['numdealspurchases','numwebpurchases','numcatalogpurchases','numstorepurchases','numwebvisitsmonth']].sum()
        cam=df[['acceptedcmp1', 'acceptedcmp2', 'acceptedcmp3', 'acceptedcmp4','acceptedcmp5', 'response']].sum()
        # Create subplots with 2 rows and 1 column
        fig2 = sp.make_subplots(rows=1, cols=3,subplot_titles=("Segment-wise distribution on total purchases.", "campaign distribution","scater plot"))

        # Assuming cluster_purchases is your DataFrame with cluster-wise purchases
        fig2.add_trace(
            go.Bar(
                x=cluster_purchases.index,
                y=cluster_purchases.values,
                marker_color=['#e28f71', '#d35454', '#b2182b', '#b43058', '#57274e', '#832b5a'],
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
                marker_color=['#e28f71', '#d35454', '#b2182b', '#b43058', '#57274e', '#832b5a'],
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
        custom_colors = {'Partner': '#57274e', 'Single': '#b43058'}


        # Create the scatter plot with custom colors
        scatter_fig = px.scatter(df, x='spent', y='income', color='family_size',
                        hover_name='income', color_discrete_map=custom_colors)

        # Add all scatter plot data to the third subplot
        for trace in scatter_fig.data:
            fig2.add_trace(trace, row=1, col=3)



        # Set layout properties for the entire figure
        fig2.update_layout(height=600, width=800)

        st.markdown("### Segment-wise distribution on total purchases and campaign distribution.")
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("Please submit the form on the Home page.")

# Call the charts_page function
charts_page()
