# Create a heatmap from pickup_community_area and dropoff_community_area 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

csv_path = "../taxi trips Fri 7_7_2017.csv"

# Load the CSV file into a DataFrame
try:
    trips_df = pd.read_csv(csv_path)
except Exception as e:
    print(f"ERROR reading CSV: {e}")
    trips_df = None

if trips_df is None:
    raise SystemExit("Stopping due to CSV load failure.")

# Create a pivot table for the heatmap
heatmap_data = trips_df.pivot_table (
index='pickup_community_area', 
columns='dropoff_community_area',
aggfunc="size",
fill_value=0
)

# Auto adjust the size of the figure
rows, cols = heatmap_data.shape
plt.figure()

# Plot the heatmap
sns.heatmap(heatmap_data)
plt.title("Heatmap of Pickup vs Dropoff Community Areas")
plt.xlabel("Dropoff Community Area")
plt.ylabel("Pickup Community Area")

plt.show()