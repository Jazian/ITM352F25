# File now has my name within it

# Rewrite using append mode to add my name to the file
with open("names.txt", "a") as file_object:
    file_object.write("Jazian Uejo\n")

with open("names.txt", "r") as file_object:
    lines = file_object.readlines()
    for line in lines:
        print(line)