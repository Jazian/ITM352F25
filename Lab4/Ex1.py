# String Manipulation Example

first = input("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last = input("Enter your last name: ")

full_name = last + ", " + first
print("Your full name is:", full_name)

print(f"Your full name is: {first} {middle_initial}. {last}")
print("Your full name is: %s %s %s" % (first, middle_initial + ".", last))
print("Your full name using format is: {} {} {}".format(first, middle_initial + ".", last))
print("Your full name tuple version is " + " ".join([first, middle_initial + ".", last]))