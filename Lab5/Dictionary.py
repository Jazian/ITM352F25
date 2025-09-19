# Create a new dictionary

country_capitals = {
    "Germany": "Berlin",
    "Canada": "Ottawa",
    "England": "London",
}
# Print the dictionary
print(country_capitals)

# Access a value by key
print(country_capitals["Germany"])
print(country_capitals["England"])

country_capitals["Italy"] = "Rome"
print(country_capitals)

#del country_capitals["Germany"]
#print(country_capitals)

#country_capitals.clear()
#print(country_capitals)

country_capitals["Italy"] = "Milan"
print(country_capitals)
print(len(country_capitals))

print('Canada' in country_capitals)
