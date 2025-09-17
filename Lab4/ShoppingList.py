# Start with an empty shopping list
shopping_list = []
shopping_list.append("apples")
shopping_list.append("milk")
shopping_list.append("bread")
shopping_list.insert(0, "eggs")
print("Current shopping list:", shopping_list)

shopping_list.pop()
print("After removing the last item:", shopping_list)
