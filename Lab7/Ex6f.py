# Original tuple
data = ("hello", 10, "goodbye", 3, "goodnight", 5)

new_item = input("Enter something to add to the tuple: ")

try:
    new_item = int(new_item)
except ValueError:
    pass 

# Recast tuple to list, append, then convert back to tuple
data_list = list(data)
data_list.append(new_item)
data = tuple(data_list)

print("Updated tuple:", data)
