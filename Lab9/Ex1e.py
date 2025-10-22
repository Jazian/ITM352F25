# Rewrite Ex1d.py using the .readlines() method.

with open("names.txt", "r") as file_object:
    lines = file_object.readlines()
    for line in lines:
        print(line)