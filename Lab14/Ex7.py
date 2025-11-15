# Create a 3D plot of fares, trip miles, and dropoff area
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

trips_df = pd.read_json("../Trips from area 8.json")
trips_df = trips_df.dropna()  # Drop rows with missing values

fares_series = trips_df.fare
trip_miles_series = trips_df.trip_miles
dropoff_area_series = trips_df.dropoff_community_area

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(fares_series, trip_miles_series, dropoff_area_series)
ax.set_title("3D Plot of Trip Miles, Fare, and Dropoff Area")
ax.set_xlabel("Fare in ($)")
ax.set_ylabel("Trip Miles")
ax.set_zlabel("Dropoff Area")

plt.show()
