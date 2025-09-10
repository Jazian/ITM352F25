# Create a function callled midpoint that takes two numbers as input and returns the value halfway between them.
# Name: Jazian Uejo
# Date: 9/10/25

def midpoint(num1, num2):
    mid = (num1 + num2) / 2
    return mid

number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: "))
result = midpoint(number1, number2)
print(f"The midpoint between {number1} and {number2} is {result}")