import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../sales_data.db')
cursor = conn.cursor()

# Query to fetch data from Users table
users_query = 'SELECT * FROM Users LIMIT 5'
cursor.execute(users_query)
users_data = cursor.fetchall()

# Query to fetch data from Sales table
sales_query = 'SELECT * FROM Sales LIMIT 5'
cursor.execute(sales_query)
sales_data = cursor.fetchall()

# Query to fetch data from Aggregations table
aggregations_query = 'SELECT * FROM Aggregations LIMIT 5'
cursor.execute(aggregations_query)
aggregations_data = cursor.fetchall()

# Print the fetched data
print("Users Data:")
for row in users_data:
    print(row)

print("\nSales Data:")
for row in sales_data:
    print(row)

print("\nAggregations Data:")
for row in aggregations_data:
    print(row)

# Close the connection
conn.close()