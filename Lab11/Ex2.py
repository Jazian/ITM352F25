# Read in a csv file an create a dataframe. Print some info.
# Pivot the dataframe to show the total by order type.
# Calculate the total sales per quarter.
import pandas as pd
import numpy as np

# Comments below display a temporarily fix a certificate error using ssl, do not use in production.
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

pd.set_option('display.max_columns', None)

url = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

# The engine "pyarrow" has a built in skipbadlines feature, if utilizing python you must reference it.
try:
    df = pd.read_csv(url, engine="pyarrow")
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['sales'] = df['quantity'] * df['unit_price']

    # Create a pivot table aggregating sales by region and order type
    pivot_table = pd.pivot_table(df, 
                                 values='sales', 
                                 index='sales_region', 
                                 columns='order_type', 
                                 aggfunc=np.sum,
                                 margins=True, # Add a 'Total' column and row
                                 margins_name='Total_Sales')
    print(pivot_table)

except Exception as e:
    print(f"Error reading CSV: {e}")

