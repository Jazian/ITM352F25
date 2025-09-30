# Create a list that contains random values and print a control statemtn (If, elif, else) that prints different messegaes if list contains 5 or less values, 5-10 values, or more than 10 values.
# Name: Jazian Uejo
# Date: 9/24/25

valuesOfList = [[1]*2, [2]*7, [3]*11]

listnumber = int(input("Enter 0 list number (0-2): "))
listLength = len(valuesOfList[listnumber])

if listLength < 5:
    print("The list contains 5 or less values.")
elif 5 <= listLength <= 10:
    print("The list contains between 5 and 10 values.")
else:
    print("The list contains more than 10 values.")
