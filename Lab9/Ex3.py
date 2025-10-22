# Read the 1,000 lines of taxi data from the taxi_1000.csv file
# Calculate he total of all fares, average fares, and the maximum trip distance

import csv

with open("taxi_1000.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    total_fares = 0.0
    max_distance = 0.0
    average_fare = 0.0
    num_rows = 0

    for line in csv.reader:
        if (num_rows > 0): # Skip header row

            tripfare = float(line[10])
            distance = float(line[5])
            total_fares += tripfare
            if distance > max_distance:
                max_distance = distance
        num_rows += 1

    if num_rows > 0:
        average_fare = round(total_fares / num_rows, 2)

    print(f"We read {num_rows} rows")
    print(f"Total Fares: ${total_fares:,.2f}")
    print(f"Average Fare: ${average_fare:,.2f}")
    print(f"Maximum Distance: {max_distance:,.2f}")
