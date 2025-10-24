# Modify the code from Ex3.py to calculate the total of all fares, the average of those fares, and the maximum trip distance (based on the Trip Miles field) for records that have fares greater than 10 dollars.


import csv

with open("taxi_1000.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    total_fares = 0.0
    max_distance = 0.0
    average_fare = 0.0
    num_rows = 0

    for line in csv_reader:
        if (num_rows > 0): # Skip header row

            tripfare = float(line[10])
            distance = float(line[5])
            total_fares += tripfare
            if distance > max_distance:
                max_distance = distance
        num_rows += 1

    if tripfare > 10:
        total_fares += tripfare
        max_distance = max(max_distance, distance)
        num_rows += 1

    if num_rows > 0:
        average_fare = round(total_fares / num_rows, 2)

    print(f"Rows with fares greater than $10: {num_rows}")
    print(f"Total Fares: ${total_fares:,.2f}")
    print(f"Average Fare: ${average_fare:,.2f}")
    print(f"Maximum Distance: {max_distance:,.2f}")
