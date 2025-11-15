# Create a scatter plot of fares and trip miles
import matplotlib.pyplot as plt
import pandas as pd

trips_df = pd.read_json("../Trips from area 8.json")

trips_df = trips_df.dropna()  # Drop rows with missing values
fares_series = trips_df.fare
trip_miles_series = trips_df.trip_miles

# Create te scatter plot
fig = plt.figure()
plt.scatter(fares_series, trip_miles_series)
plt.title("Trip Miles by Fare")
plt.xlabel("Fare in ($)")
plt.ylabel("Trip Miles")

plt.show()

# Create a plot with linestyle "none", "v" marker, cyan color, and 0.2 transparency
fig = plt.figure()
plt.plot(fares_series, trip_miles_series, linestyle="none", marker="v", color="cyan", alpha=0.2)
plt.title("Trip Miles by Fare - Line Plot")
plt.xlabel("Fare in ($)")
plt.ylabel("Trip Miles")

plt.show()