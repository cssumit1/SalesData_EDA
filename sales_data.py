import pandas as pd
import requests
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weather_info(api_key, lat, lon):
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
        response.raise_for_status()
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        weather_conditions = weather_data['weather'][0]['description']
        return {'temperature': temperature, 'weather_conditions': weather_conditions}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather information: {e}")
        return {'temperature': None, 'weather_conditions': None}

# Load sales data from CSV file
try:
    sales_data = pd.read_csv('sales_data_1.csv')
except FileNotFoundError:
    logger.error("Error: CSV file not found.")
    exit(1)
except pd.errors.EmptyDataError:
    logger.error("Error: CSV file is empty.")
    exit(1)
except pd.errors.ParserError:
    logger.error("Error: Unable to parse CSV file.")
    exit(1)

# Fetch user data from JSONPlaceholder API
users_data = requests.get('https://jsonplaceholder.typicode.com/users').json()

# Extract relevant fields from user data
users_info = [{'customer_id': user['id'],
               'lat': user['address']['geo']['lat'],
               'lng': user['address']['geo']['lng']} for user in users_data]

# Create a DataFrame from the users_info list
users_df = pd.DataFrame(users_info)

# Merge user data with sales data based on customer_id
merged_data = pd.merge(sales_data, users_df, on='customer_id', how='left')

# Get OpenWeatherMap API key and store address (fictional)
api_key = 'OpenWeatherMap_API_Key'     # Need to Update OpenWeatherMap API Key Here

# Initialize a new column for weather information
merged_data['weather_info'] = None

# Make API requests to OpenWeatherMap for each sale
total_rows = len(merged_data)
for index, row in merged_data.iterrows():
    # Extract latitude and longitude from user data
    lat, lng = row['lat'], row['lng']

    # Make API request to get weather information
    logger.info(f"Fetching weather information for row {index + 1}/{total_rows}...")
    weather_response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}').json()

    # Check if 'main' key is present in the response
    if 'main' in weather_response:
        # Extract relevant weather information
        temperature = weather_response['main']['temp']
        weather_conditions = weather_response['weather'][0]['description']

        # Update the 'weather_info' column with the obtained information
        merged_data.at[index, 'weather_info'] = f'Temperature: {temperature} K, Conditions: {weather_conditions}'
    else:
        # Handle the case where 'main' key is not present
        merged_data.at[index, 'weather_info'] = 'Weather data not available'

# Data Manipulation and Aggregations

# Calculate total sales amount per customer
total_sales_per_customer = merged_data.groupby('customer_id')['quantity'].sum().reset_index()
total_sales_per_customer.rename(columns={'quantity': 'total_sales_quantity'}, inplace=True)

# Determine the average order quantity per product
average_order_quantity_per_product = merged_data.groupby('product_id')['quantity'].mean().reset_index()
average_order_quantity_per_product.rename(columns={'quantity': 'avg_order_quantity'}, inplace=True)

# Identify the top-selling products or customers
top_selling_products = merged_data.groupby('product_id')['quantity'].sum().nlargest(5).reset_index()
top_selling_customers = merged_data.groupby('customer_id')['quantity'].sum().nlargest(5).reset_index()

# Analyze sales trends over time (monthly sales)
merged_data['order_date'] = pd.to_datetime(merged_data['order_date'])
merged_data['month'] = merged_data['order_date'].dt.month

monthly_sales = merged_data.groupby('month')['quantity'].sum().reset_index()
monthly_sales.rename(columns={'quantity': 'monthly_sales_quantity'}, inplace=True)

# Include weather data in the analysis (e.g., average sales amount per weather condition)
average_sales_per_weather_condition = merged_data.groupby('weather_info')['quantity'].mean().reset_index()
average_sales_per_weather_condition.rename(columns={'quantity': 'avg_sales_quantity'}, inplace=True)

# Data Storage (using SQLite)

# Connect to the SQLite database
conn = sqlite3.connect('../sales_data.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        customer_id INTEGER PRIMARY KEY,
        lat REAL,
        lng REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL,
        order_date TEXT,
        weather_info TEXT,
        FOREIGN KEY (customer_id) REFERENCES Users (customer_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Aggregations (
        customer_id INTEGER PRIMARY KEY,
        total_sales_quantity INTEGER,
        avg_order_quantity REAL,
        FOREIGN KEY (customer_id) REFERENCES Users (customer_id)
    )
''')

# Insert data into tables
users_df.to_sql('Users', conn, if_exists='replace', index=False)
merged_data.to_sql('Sales', conn, if_exists='replace', index=False)
total_sales_per_customer.to_sql('Aggregations', conn, if_exists='replace', index=False)

# Commit changes and close connection
conn.commit()
conn.close()
