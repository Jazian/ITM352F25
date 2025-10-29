# Read in a CSV file of homes data and create a dataframe.

import pandas as pd

df_homes = pd.read_csv('homes_data.csv')

# Print out the dimensions of the dataframe and the first 10 rows.
shape = df_homes.shape
print(f"The homes data has {shape[0]} rows and {shape[1]} columns.")

# Select only the homes with 500 or more units
df_big_homes = df_homes[df_homes.units >= 500]

#Drop unnecessary columns and print the first 10 rows
df_big_homes = df_big_homes.drop(columns=['id', 'easement'])
print(df_big_homes.head(10))

# Look at the data types
print(df_big_homes.info())

# Convert columns to appropriate data types
df_big_homes["sale_price"] = pd.to_numeric(df_big_homes["sale_price"], errors='coerce')
df_big_homes["land_sqft"] = pd.to_numeric(df_big_homes["land_sqft"], errors='coerce')
df_big_homes["gross_sqft"] = pd.to_numeric(df_big_homes["gross_sqft"], errors='coerce')

# Drop rows with missing values
df_big_homes = df_big_homes.dropna()

# Drop duplicate rows
df_big_homes = df_big_homes.drop_duplicates()

# Print out the first 10 rows of the cleaned dataframe
print("After dropping nulls and duplicates\n", df_big_homes.head(10))

# Keep only rows where saleprice is greater than 0
df_big_homes = df_big_homes[df_big_homes["sale_price"] > 0]
print("After dropping 0 sales\n", df_big_homes.head(10))

# Calculate the average sale price
average_price = df_big_homes["sale_price"].mean()
print(f"The average sale price of homes with 500 or more units is ${average_price:,.2f}.")