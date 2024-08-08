#Importing all the neccessary libraries
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from walmart import get_walmart
from foodbasics import get_foodbasics_search
import plotly.express as px

#Load the custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#Sidebar
st.sidebar.image("blob.jpeg")
st.sidebar.button("Home")
st.markdown('<div class="custom-text">Grocery Item</div>', unsafe_allow_html=True)

#Form for Entering the item and searching
with st.form("Search"):
    item=st.text_input("Enter the Item",placeholder="Type here")
    search=st.form_submit_button("Search")
if search:
    # Call the function from file1.py to get Food Basics eggs
    walmart = get_walmart(item)
    #st.write(walmart)
    # Call the function from file2.py to search Food Basics for the entered keyword
    food_basics = get_foodbasics_search(item)
    #st.write(food_basics)

    # Combine the two dataframes
    combined_df = pd.concat([walmart, food_basics], ignore_index=True)
    st.write(combined_df)
    #Set the seesion state
    st.session_state['search_done'] = True
    st.session_state['compare_clicked'] = False
    st.session_state['combined_df']=combined_df
#Using the session state to display the Compare button
if 'search_done' in st.session_state and st.session_state['search_done']:
    # Display the DataFrame using Streamlit
    df = st.session_state.get('combined_df')
    #if df is not None:
        #st.dataframe(df)
    # Display the compare button after the search
    if st.sidebar.button("Compare"):
        st.session_state['compare_clicked'] = True

if 'compare_clicked' in st.session_state and st.session_state['compare_clicked']:
    # Display the chart and hide the DataFrame
    #df = st.session_state.get('combined_df')
    if df is not None:
        #Drawing the bar chart comparing the Brand,Price of different stores
        fig = px.bar(df, x='Brand', y='Price',color='store', barmode='group',
             title='Prices by Brand and Store')
        st.plotly_chart(fig)
        st.bar_chart(df)
