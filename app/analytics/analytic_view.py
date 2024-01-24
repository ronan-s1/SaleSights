import pandas as pd
import streamlit as st
from analytics.analytic_controller import get_cat_and_qty
import plotly.express as px


def analytic_main():
    st.title("Monthly Product Sales by Category")
    start_date = "2024-01-24"
    end_date = "2024-04-24"

    data = get_cat_and_qty(start_date, end_date)
    st.dataframe(data)
    
    # Create a bar chart using Plotly Express
    fig = px.bar(data, x='category', y='quantity', title='Monthly Product Sales by Category')

    # Display the chart using Streamlit
    st.plotly_chart(fig)

 

