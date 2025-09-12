# Test to see how the funtions define din HandyMath work
# Name: Jazian Uejo
# Date: 9/12/25

import HandyMath as HM

number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: "))

mid = HM.midpoint(number1, number2)
print(f"The midpoint between {number1} and {number2} is {mid}")

exp = HM.exponent(number1, number2)
print(f"{number1} raised to the power of {number2} is {exp}")

max_number = HM.max(number1, number2)
print(f"The maximum between {number1} and {number2} is {max_number}")

min_number = HM.min(number1, number2)
print(f"The minimum between {number1} and {number2} is {min_number}")

sq_root = HM.square_root(number1)
print(f"The square root of {number1} is {sq_root}")
