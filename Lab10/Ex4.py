# Read a JSON file of taxi trip data and create a dataframe.
# Calculate the median fare.

import pandas as pd

taxi_df = pd.read_json('Taxi_Trips.json')

# Print a summary of the dataframe.
print(taxi_df.describe())
print(taxi_df.head())

# Print the median fare.
print("Median fare: ", taxi_df['fare'].median())