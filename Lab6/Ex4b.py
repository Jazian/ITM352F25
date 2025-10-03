my_birth_year = 2004
if (my_birth_year % 4 == 0 and my_birth_year % 100 != 0) or (my_birth_year % 400 == 0):
    print("Leap year")
else:
    print("Not a leap year")