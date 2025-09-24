# Create a list of dictionaries where each dictionary reprenents a taxi trip
# Name: Jazian Uejo
# Date: 9/19/25
taxiTrips = [
    {'duration' : 1.1, 'fare' : 6.25},
    {'duration' : 2.3, 'fare' : 12.50},
    {'duration' : 0.5, 'fare' : 3.75},
    {'duration' : 4.0, 'fare' : 20.00}
]
print(taxiTrips)
print(f"The third trip was {taxiTrips[2]['duration']} miles and cost ${taxiTrips[2]['fare']}.")
driver_share = taxiTrips[2]['fare'] * 0.8
print(f"The driver's share of the fare is ${driver_share : .2f}.")
