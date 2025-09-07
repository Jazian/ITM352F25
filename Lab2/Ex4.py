# Ask the user to enter a floating point number between 1 and 100.
# Square the number and return the result rounded to 2 decimal places.
# Name: Jazian Uejo
# Date: 9/5/25

value_entered = input("Please enter a floating point number between 1 and 100: ")

value_entered_float = float(value_entered)
squared_value = value_entered_float ** 2
rounded_value = round(squared_value, 2)

print(f"The squared value of {value_entered_float} is {rounded_value}")
print(f"The value without rounding is {squared_value}")