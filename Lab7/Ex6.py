data = ("hello", 10, "goodbye", 3, "goodnight", 5)

new_item = input("Enter something to add to the tuple: ")

data.append(new_item)  

for item in data:
    if type(item) == str:
        string_count += 1
print(f"There are {string_count} strings in the data tuple")