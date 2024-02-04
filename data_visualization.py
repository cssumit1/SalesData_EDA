import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../sales_data.db')

# Query to fetch data from Aggregations table
aggregations_query = 'SELECT * FROM Aggregations'
aggregations_data = pd.read_sql_query(aggregations_query, conn)

# Plotting total sales quantity per customer using seaborn
sns.barplot(x='customer_id', y='total_sales_quantity', data=aggregations_data)
plt.title('Total Sales Quantity per Customer')
plt.xlabel('Customer ID')
plt.ylabel('Total Sales Quantity')
plt.show()

# Fetching monthly sales trends directly from SQLite database
monthly_sales_query = 'SELECT month, SUM(quantity) as total_sales_quantity FROM Sales GROUP BY month'
monthly_sales = pd.read_sql_query(monthly_sales_query, conn)

# Plotting monthly sales trends using seaborn
sns.lineplot(x='month', y='total_sales_quantity', data=monthly_sales)
plt.title('Monthly Sales Trends')
plt.xlabel('Month')
plt.ylabel('Total Sales Quantity')
plt.show()

# Fetching top selling products directly from SQLite database
top_selling_products_query = 'SELECT product_id, SUM(quantity) as total_sales_quantity FROM Sales GROUP BY product_id ORDER BY total_sales_quantity DESC LIMIT 5'
top_selling_products = pd.read_sql_query(top_selling_products_query, conn)

# Plotting top selling products using seaborn
sns.barplot(x='product_id', y='total_sales_quantity', data=top_selling_products)
plt.title('Top Selling Products')
plt.xlabel('Product ID')
plt.ylabel('Total Sales Quantity')
plt.show()

# Fetching top selling customers directly from SQLite database
top_selling_customers_query = 'SELECT customer_id, SUM(quantity) as total_sales_quantity FROM Sales GROUP BY customer_id ORDER BY total_sales_quantity DESC LIMIT 5'
top_selling_customers = pd.read_sql_query(top_selling_customers_query, conn)

# Plotting customer distribution using matplotlib
plt.pie(top_selling_customers['total_sales_quantity'], labels=top_selling_customers['customer_id'], autopct='%1.1f%%')
plt.title('Customer Distribution')
plt.show()

# Plotting weather impact on sales using seaborn
weather_impact_query = 'SELECT weather_info, quantity FROM Sales'
weather_impact_data = pd.read_sql_query(weather_impact_query, conn)
sns.boxplot(x='weather_info', y='quantity', data=weather_impact_data)
plt.title('Weather Impact on Sales')
plt.xlabel('Weather Conditions')
plt.ylabel('Sales Quantity')
plt.xticks(rotation=45, ha='right')
plt.show()

# Plotting average sales quantity per weather condition using seaborn
average_sales_per_weather_condition_query = 'SELECT weather_info, AVG(quantity) as avg_sales_quantity FROM Sales GROUP BY weather_info'
average_sales_per_weather_condition = pd.read_sql_query(average_sales_per_weather_condition_query, conn)
sns.barplot(x='weather_info', y='avg_sales_quantity', data=average_sales_per_weather_condition)
plt.title('Average Sales Quantity per Weather Condition')
plt.xlabel('Weather Conditions')
plt.ylabel('Average Sales Quantity')
plt.xticks(rotation=45, ha='right')
plt.show()

# Close the connection
conn.close()
