with open("names.txt_bad", "r") as file_object:
    lines = file_object.readlines()
    for line in lines:
        print(line)
