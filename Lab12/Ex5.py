# Get a JSON file from the city of Chicago's data portal and analyze driver types.
# Make use of the SQL like queary capabilities of the portal.
import pandas as pd
import requests

# Create a REST queary that returns the count of driver licenses by type
search_results = requests.get("https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type")
results_json = search_results.json()

# Convert the results to a pandas DataFrame
results_df = pd.DataFrame.from_records(results_json)
results_df.columns = ['driver_type', 'count']
results_df = results_df.set_index('driver_type')

# Print the results of dataframe
print(f"Driver License Counts by Type:\n{results_df}")