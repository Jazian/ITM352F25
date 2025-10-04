# Original tuple
data = ("hello", 10, "goodbye", 3, "goodnight", 5)

new_item = input("Enter something to add to the tuple: ")

# Try to convert to int if possible
try:
    new_item = int(new_item)
except ValueError:
    pass  # Keep it as string if conversion fails

# Attempt to append to the tuple (which will fail)
try:
    data.append(new_item)
except AttributeError as error:
    print("Attempted to append a value to a tuple.")
    print("Error encountered:", error)

    # Correct way: create a new tuple
    updated_data = data + (new_item,)
    print("Instead, here's the updated tuple:", updated_data)
