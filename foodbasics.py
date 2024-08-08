#Webscrapping data from Food Basics
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def get_foodbasics_search(item):
    url = f'https://www.foodbasics.ca/search?filter={item}'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'}
    proxies = {
    'http': 'http://SwathiSivagnanamurthi:Stream@2024@45.32.86.6:31280',
    'https': 'http://SwathiSivagnanamurthi:Stream@2024@45.32.86.6:31280'
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers,proxies=proxies)
    
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting product names, brands, and prices
        description = soup.findAll('div', class_='head__title')
        brands = soup.findAll('span', class_='head__brand')
        prices = soup.findAll('div', class_='pricing__sale-price')
        
        Description = [des.text.strip() for des in description]
        brand_names = [brand.text.strip() for brand in brands]
        sale_prices = [price.text.strip().replace('ea', '').strip() for price in prices]
        
        # Create a DataFrame to display the results
        data = { 'Brand': brand_names, 'Description': Description,'Price': sale_prices, 'store':"Food Basics"}
        foodbasics_df = pd.DataFrame(data)
        return foodbasics_df
    else:
        st.error(f'Failed to retrieve the page. Status code: {response.status_code}')
        return pd.DataFrame(columns=['Product', 'Brand', 'Price'])
