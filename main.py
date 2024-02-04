import subprocess

def run_sales_data_read():
    subprocess.run(['python', 'sales_data_read.py'])

def run_data_read():
    subprocess.run(['python', 'sales_data_read.py'])

def run_data_visualization():
    subprocess.run(['python', 'data_visualization.py'])

if __name__ == "__main__":
    # You can call the functions to run each script
    run_sales_data_read()
    run_data_read()
    run_data_visualization()
