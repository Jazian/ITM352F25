celebrities_tuple = ("Taylor Swift", "Lionel Messi", "Max Verstappen", "Keanu Reaves", "Angelina Jolie")
ages_tuple = (34, 36, 26, 59, 48)
#celebrities_list = []
#ages_list = []

#for celeb in celebrities_tuple:
#    celebrities_list.append(celeb)
celebrities_list = [celeb for celeb in celebrities_tuple]
ages_list = [age for age in ages_tuple]

#for age in ages_tuple:
#    ages_list.append(age)

celebrities_dictionary = {
    "celebrities": celebrities_list,
    "ages": ages_list
}
print(celebrities_dictionary)