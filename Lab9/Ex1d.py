# Rewrite Ex1c.py using the .readline() method.

with open("names.txt", "r") as file_object:
    while (line := file_object.readline()):
        print(line)
    # print("Total names in the file:", len(names_list))
