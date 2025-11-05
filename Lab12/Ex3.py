# Parse the UH Shidler ITM Department page and extract names of faculty members.
import urllib.request
# import ssl
from bs4 import BeautifulSoup

# ssl._create_default_https_context = ssl._create_unverified_context
itm_url = "https://shidler.hawaii.edu/itm/people"

itm_html = urllib.request.urlopen(itm_url)
html_to_parse = BeautifulSoup(itm_html, 'html.parser')

pretty_html = html_to_parse.prettify()
lines = pretty_html.splitlines()
num_to_print = 10

# Print the first few lines of the prettified HTML
for line in lines[:num_to_print]:
    print(line)

# Find and print just the names of faculty members
list_of_itm_faculty = html_to_parse.find_all('h2', class_='title')

# Create a list with just the names
itm_faculty = []
for element in list_of_itm_faculty:
    itm_faculty.append(element.text)
    print(element.text)

print("Number in the initial list:", len(list_of_itm_faculty))
unique_itm_faculty = list(set(itm_faculty))
print("Number of unique faculty names:", len(unique_itm_faculty))

