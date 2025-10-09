# Original tuple
data = ("hello", 10, "goodbye", 3, "goodnight", 5)

new_item = input("Enter something to add to the tuple: ")

try:
    new_item = int(new_item)
except ValueError:
    pass

try:
    data.append(new_item)
except AttributeError:
    data = data + (new_item,)

print("Updated tuple:", data)
