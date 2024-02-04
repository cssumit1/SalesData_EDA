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

1. Clone the repository: git clone https://github.com/yourusername/sales-data-pipeline.git
2. Navigate to the project directory: cd sales-data-pipeline
3. Install dependencies: pip install -r requirements.txt
   
## Install the depedecies
    pip install -r requirements.txt

python src/main.py


### Data Sources
1. Sales data: CSV file (sales_data_1.csv)
2. User data: JSONPlaceholder API
4. Weather data: OpenWeatherMap API

### Project Structure
sales_data_1.csv: CSV file containing sales data
sales_data.py: Script for fetching weather information and building the data pipeline
data_visualization.py: Script for visualizing insights from the data
sales_data.db: SQLite database to store processed data
requirements.txt: File listing required Python packages

### Data Extraction and Transformation
The script sales_data.py extracts sales and user data, enriches it with weather information, performs various data manipulations, and stores the results in an SQLite database.

### Data Analysis
Calculate total sales per customer
Determine the average order quantity per product
Identify the top-selling products and customers
Analyze monthly sales trends
Include weather data in the analysis# SalesData_EDA
