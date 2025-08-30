def calculator():
    print("Welcome to the Calculator!")
    
    while True:  # Loop to allow multiple calculations
        print("\nChoose an operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")

        try:
            # Get user input for operation
            operation = int(input("Enter the number of the operation (1-5): "))

            # Exit the program if the user chooses 5
            if operation == 5:
                print("Thank you for using the calculator. Goodbye!")
                break

            # Validate operation choice
            if operation not in [1, 2, 3, 4]:
                print("Invalid operation. Please choose a number between 1 and 5.")
                continue

            # Get user input for numbers
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            # Perform the chosen operation
            if operation == 1:
                result = num1 + num2
                print(f"The result of addition is: {result}")
            elif operation == 2:
                result = num1 - num2
                print(f"The result of subtraction is: {result}")
            elif operation == 3:
                result = num1 * num2
                print(f"The result of multiplication is: {result}")
            elif operation == 4:
                # Handle division by zero
                if num2 == 0:
                    print("Error: Division by zero is not allowed.")
                else:
                    result = num1 / num2
                    print(f"The result of division is: {result}")

        except ValueError:
            print("Invalid input. Please enter numeric values.")

# Run the calculator
if __name__ == "__main__":
    calculator()