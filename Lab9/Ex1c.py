# Read the contents of the file and print each line and count how many names are in the file.

with open("names.txt", "r") as file_object:
    content = file_object.read()
    print(content)
    names_list = content.split("\n ")
    print("Total names in the file:", len(names_list))