# Create a scatter plot of fares and trip miles
import matplotlib.pyplot as plt
import pandas as pd

trips_df = pd.read_json("../Trips from area 8.json")

trips_df = trips_df.dropna()  # Drop rows with missing values

# Filter out trips with 0 miles and trips less than 2 miles
trips_df = trips_df[trips_df.trip_miles > 0]
trips_df = trips_df[trips_df.trip_miles >= 2]

fares_series = trips_df.fare
trip_miles_series = trips_df.trip_miles

# Create te scatter plot
fig = plt.figure()
plt.scatter(fares_series, trip_miles_series)
plt.title("Trip Miles by Fare")
plt.xlabel("Fare in ($)")
plt.ylabel("Trip Miles")

plt.savefig("FaresXmiles.png")
plt.show()