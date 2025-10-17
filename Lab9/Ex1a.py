# Write a code that opens the file with the appropriate file mode and displays data type returned from open()
# Date: 10/17/2025
# Name: Jazian Uejo

file_object = open("names.txt", "r")

print(type(file_object))

file_object.close()
