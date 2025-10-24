# Create a dataframe from an individual list.
# Do some simple statistics on the data.

import pandas as pd

# List of individuals' ages
ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]


#Lists of individuals' names and genders
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

# Create a dictionary from the lists
dict = zip(ages, gender)

# Convert the dictionary into a dataframe with names as the keys
df = pd.DataFrame(dict, index=names, columns=["Age", "Gender"])

print(df)
summary = df.describe()
print(summary)

#Calculate avgerage age by gender
avergae_age_by_gender = df.groupby("Gender")["Age"].mean()
print(avergae_age_by_gender)