# Zip together a list of trip durations and a tuple of trip fares.
# From this zip create a dictionary.
# Name: Jazian Uejo
# Date: 9/24/25

trip_durations = [1.1, 0.8, 2.5, 2.6]
trip_fares = (6.25, 5.25, 10.50, 8.05)

trips = dict(zip(trip_durations, trip_fares))
print(trips)

trip_num=int(input("What trip do you want?:"))

print(f"Duration: {list(trips.keys())[trip_num - 1]} miles")
print(f"Cost: ${list(trips.values())[trip_num - 1]:.2f}")
