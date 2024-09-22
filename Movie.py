import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Initializing session
s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
})

# Getting text from the IMDb Top-250 page
start_page = 'https://www.imdb.com/chart/top'

try:
    start_page_text = s.get(start_page).text
except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
    exit()

# Creating a top movies list and parsing the page
link_list = []
movies_data = []

soup = BeautifulSoup(start_page_text, 'html.parser')

for col in soup.find_all('td', {'class': 'titleColumn'}):
    title_tag = col.find('a')
    year_tag = col.find('span')
    
    if title_tag and year_tag:
        title = title_tag.text
        year = year_tag.text.strip('()')
        link = title_tag['href']
        full_link = f'https://www.imdb.com{link}'
        
        # Collecting movie data
        movies_data.append({
            'Title': title,
            'Year': year,
            'IMDB Link': full_link
        })
        link_list.append(full_link)

# Creating a DataFrame for movie list
movies_df = pd.DataFrame(movies_data)

# Parsing detailed data from movie pages (optional)
for n in range(min(5, len(link_list))):  # Change 5 to however many movies you want to scrape
    try:
        r = s.get(link_list[n])
        r.raise_for_status()  # Raise an error for bad responses
        with open(f'page_{n}.html', 'w', encoding='utf-8') as output_file:
            output_file.write(r.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {link_list[n]}: {e}")

# Save to CSV
csv_file_path = 'top_movies.csv'
if os.path.exists(csv_file_path):
    print(f"{csv_file_path} already exists. It will be overwritten.")

movies_df.to_csv(csv_file_path, index=False)
print("Data saved to top_movies.csv")