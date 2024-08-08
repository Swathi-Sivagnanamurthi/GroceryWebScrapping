#Webscrapping data from Walmart
import requests
import pandas as pd
import streamlit
from bs4 import BeautifulSoup

def get_walmart(item):
    # Example product URL (you may want to construct the URL based on the user input)
    product_url = f'https://www.walmart.ca/en/search?q={item}'
    # Headers to mimic a real browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'}

    # List to store product data
    products = []

    # Request the URL and parse the content
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print(soup)
    brand_name=soup.find_all("div",class_='mb1 mt2 b f6 black mr1 lh-copy')
    item_des=soup.find_all("span",class_='normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy')
    price=soup.find_all("div",class_='mr1 mr2-xl b black lh-copy f5 f4-l')

    
    # Loop through the results and collect the data
    for brand, description, price in zip(brand_name, item_des, price):
        products.append({
            'Brand': brand.get_text(strip=True),
            'Description': description.get_text(strip=True),
            'Price': price.get_text(strip=True).replace('$', ''),
            'store': "Walmart"
        })

    # Convert the list of dictionaries to a DataFrame
    walmart = pd.DataFrame(products)
    return walmart
