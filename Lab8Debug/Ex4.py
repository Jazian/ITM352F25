def get_element(list, index):
    return list[index] if index < len(list) else "Error: Index out of range"


my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))  
print(get_element(my_list, 5)) 
