# Read n a csv file of employee data and calculate the Average salary, Max Salary, Min Salary

import csv

csv_filename = "my_custom_spreadsheet.csv"
salaries = []

with open(csv_filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Skip the header row
    print(f"Headers: {headers}")

    salary_index = headers.index("Annual_Salary")  # Assuming the header for salary is "Salary"
    for row_data in reader:
        salaries.append(float(row_data[salary_index])) # Using the salary index


if salaries:
    average_salary = sum(salaries) / len(salaries)
    max_salary = max(salaries)
    min_salary = min(salaries)

    print(f"Average Salary: ${average_salary:.2f}")
    print(f"Max Salary: ${max_salary:.2f}")
    print(f"Min Salary: ${min_salary:.2f}")
else:
    print("No salary data found.")