import pandas as pd
import requests
import sqlite3
from datetime import datetime

# Load sales data from CSV file
sales_data = pd.read_csv('../sales_data_1.csv')

# Fetch user data from JSONPlaceholder API
users_data = requests.get('https://jsonplaceholder.typicode.com/users').json()

# Extract relevant fields from user data
users_info = [{'user_id': user['id'],
               'name': user['name'],
               'username': user['username'],
               'email': user['email'],
               'lat': user['address']['geo']['lat'],
               'lng': user['address']['geo']['lng']} for user in users_data]

# Create a DataFrame from the users_info list
users_df = pd.DataFrame(users_info)

# Merge user data with sales data based on customer_id
merged_data = pd.merge(sales_data, users_df, left_on='customer_id', right_on='user_id', how='left')

# Get OpenWeatherMap API key and store address (fictional)
api_key = '8eff59dc714f051c65cc3ec635f94570'
store_address = 'Fictional Store, City, Country'

# Initialize a new column for weather information
merged_data['weather_info'] = None

# Make API requests to OpenWeatherMap for each sale
for index, row in merged_data.iterrows():
    # Extract latitude and longitude from user data
    lat, lng = row['lat'], row['lng']

    # Make API request to get weather information
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
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        username TEXT,
        email TEXT,
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
        FOREIGN KEY (customer_id) REFERENCES Users (user_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Aggregations (
        aggregation_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        total_sales_quantity INTEGER,
        avg_order_quantity REAL,
        FOREIGN KEY (customer_id) REFERENCES Users (user_id)
    )
''')

# Insert data into tables
users_df.to_sql('Users', conn, if_exists='replace', index=False)
merged_data.to_sql('Sales', conn, if_exists='replace', index=False)
total_sales_per_customer.to_sql('Aggregations', conn, if_exists='replace', index=False)

# Commit changes and close connection
conn.commit()
conn.close()
