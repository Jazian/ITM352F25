# Read in a CSV file of homes data and create a dataframe.

import pandas as pd

df_homes = pd.read_csv('homes_data.csv')

# Print out the dimenstions of the datafram and the first 10 rows.
shape = df_homes.shape
print(f"The homes data has {shape[0]} rows and {shape[1]} columns.")

# Select only the homes with 500 or more units
df_big_homes = df_homes[df_homes.units >= 500]

#Drop unnecessary columns and print the first 10 rows
df_big_homes = df_big_homes.drop(columns=['id', 'easement'])
print(df_big_homes.head(10))

# Look at the data types
print(df_big_homes.info())