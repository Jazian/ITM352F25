# Extract vehicle license data from the city of Chicago's data portal
import pandas as pd
from sodapy import Socrata

# Create a Socrata client to access the Chicago data portal
client = Socrata("data.cityofchicago.org", None)

# Specify the JSON file for the vehicle license data
json_file = "rr23-ymwb"
results = client.get(json_file, limit=500)

# Convert the results to a pandas DataFrame
df = pd.DataFrame.from_records(results)
print(df.head())

vehicle_and_fuel_sources = df[["public_vehicle_number", "vehicle_fuel_source"]]
print(f"Vehicle and fuel sources:\n{vehicle_and_fuel_sources}")

vehicles_by_fuel_type = vehicle_and_fuel_sources.groupby("vehicle_fuel_source").count()
print(f"\nNumber of vehicles by fuel type:\n{vehicles_by_fuel_type}")