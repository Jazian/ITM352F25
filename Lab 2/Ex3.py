#Ask the user to enter a number between 1 and 100. Square the number
#and print the result...
#Name: Jazian Uejo
#Date: 9/3/25

print("Hi There")
value_entered = input("Please enter an floating point number between 1 and 100: ")
print("The user entered ", value_entered)

# Convert the string to a floating (Allows use of decimal integers) point number
vaule_as_float = float(value_entered)

# Square the number
value_squared = vaule_as_float ** 2

# Round to 2 decimal places and print result
value_rounded = round(value_squared, 2)
print(f"The value squared is {value_rounded}")
