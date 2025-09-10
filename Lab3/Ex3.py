def square_root(x, percision=2):
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    return round(x ** 0.5, percision)

number = float(input("Enter a number: "))
result = square_root(number)
print(f"The square root of {number} is {result}")