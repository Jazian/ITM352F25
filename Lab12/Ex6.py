import urllib.request
from bs4 import BeautifulSoup

# Load the page
hawaii_mortgage_url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
mortgage_html = urllib.request.urlopen(hawaii_mortgage_url)
html_to_parse = BeautifulSoup(mortgage_html, 'html.parser')

# Locate the mortgage rate table and its rows
rate_table = html_to_parse.find("table")
rate_rows = rate_table.find("tbody").find_all("tr")

# Extract lender and rate info separating them by lender and their rates
lender = None
rate_data = []

for row in rate_rows:
    cells = row.find_all("td")
    if len(cells) == 5:
        lender_info = cells[0].get_text(separator=" ", strip=True)
        lender = lender_info.split("\n")[0].strip()
        term = cells[1].get_text(strip=True)
        rate = cells[2].get_text(strip=True)
        points = cells[3].get_text(strip=True)
        apr = cells[4].get_text(strip=True)
    elif len(cells) == 4:
        term = cells[0].get_text(strip=True)
        rate = cells[1].get_text(strip=True)
        points = cells[2].get_text(strip=True)
        apr = cells[3].get_text(strip=True)
    else:
        continue

# Store and append the data and print it accordingly
    rate_data.append((lender, term, rate, points, apr))
    print(f"{lender}: {term} | Rate: {rate} | Points: {points} | APR: {apr}")
