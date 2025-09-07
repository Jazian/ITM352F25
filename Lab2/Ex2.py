# Ask the user for their birthyear. Calculate their age b subtracting by current year.
# Name: Jazian Uejo
# Date: 9/3/25

birth_year = input("Please enter your bitrh year as a four digit number: ")
# Need to check they really entered an integer.
birth_year_int = int(birth_year)

# This should be changed to extract the year automaticlly from the current date.
current_year = 2025

# This doesn't take into account the day and month. Need to fix.
age = current_year - birth_year_int
print ("You entered ", birth_year)
print ("Your age is ", age)