# Sales Data Pipeline Project

## Overview


This project aims to build a comprehensive sales data pipeline that includes data extraction, transformation, and loading (ETL) processes. The pipeline incorporates user information, sales data, and weather information, providing insights into sales trends, customer behavior, and the impact of weather conditions on sales.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup and Usage](#setup-and-usage)
- [Data Pipeline Components](#data-pipeline-components)
- [Database Schema](#database-schema)
- [Visualizations](#visualizations)
- [Dockerization](#dockerization)
- [Deliverables](#deliverables)

## Project Structure

- **/:** Contains the source code for the data pipeline.
- **/:** Includes sample sales data and any other necessary data files.
- **/:** Documentation files, including this README.

## Setup and Usage

### Prerequisites

Requirements
Python (version 3.10)
Pandas
Requests
Matplotlib
Seaborn
SQLite3

### Installation

1. Clone the repository: git clone https://github.com/cssumit1/SalesData_EDA.git
2. Navigate to the project directory: cd SalesData_EDA
3. Install dependencies: pip install -r requirements.txt
4. run the program >> python main.py
   
## Install the dependencies
    pip install -r requirements.txt
    python main.py


### Data Sources
1. Sales data: CSV file (sales_data.csv)
2. User data: JSONPlaceholder API
4. Weather data: OpenWeatherMap API

### Project Structure
1. sales_data.csv: CSV file containing sales data
2. sales_data.py: Script for fetching weather information and building the data pipeline
3. data_visualization.py: Script for visualizing insights from the data
4. sales_data.db: SQLite database to store processed data
5. requirements.txt: File listing required Python packages

### Data Extraction and Transformation
The script sales_data.py extracts sales and user data, enriches it with weather information, performs various data manipulations, and stores the results in an SQLite database.

## Database Schema
    - The SQLite database consists of three tables:

## Database Schema

### Users

- `user_id` (INTEGER, PRIMARY KEY)
- `name` (TEXT)
- `username` (TEXT)
- `email` (TEXT)
- `lat` (REAL)
- `lng` (REAL)

### Sales

- `order_id` (INTEGER, PRIMARY KEY)
- `customer_id` (INTEGER, FOREIGN KEY)
- `product_id` (INTEGER)
- `quantity` (INTEGER)
- `price` (REAL)
- `order_date` (TEXT)
- `weather_info` (TEXT)

### Aggregations

- `customer_id` (INTEGER, PRIMARY KEY, FOREIGN KEY)
- `total_sales_quantity` (INTEGER)
- `avg_order_quantity` (REAL)


## Visualizations
## Data Analysis

The following analyses have been performed on the sales data:

### Total Sales per Customer

- Calculated the total sales quantity for each customer.

### Average Order Quantity per Product

- Determined the average order quantity for each product.

### Top-Selling Products and Customers

- Identified the top-selling products and customers based on total sales quantity.

### Monthly Sales Trends

- Analyzed trends in monthly sales quantity.

### Weather Impact on Sales

- Included weather data in the analysis to understand its impact on sales.


