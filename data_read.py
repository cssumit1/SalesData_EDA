import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('../sales_data.db')

# Read data from the created tables
users_data = pd.read_sql_query('SELECT * FROM Users', conn)
sales_data = pd.read_sql_query('SELECT * FROM Sales', conn)
aggregations_data = pd.read_sql_query('SELECT * FROM Aggregations', conn)

# Close the database connection
conn.close()

# Display the data
print("Users Data:")
print(users_data.head())

print("\nSales Data:")
print(sales_data.head())

print("\nAggregations Data:")
print(aggregations_data.head())
