import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# Function to initialize a session with headers
def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    })
    return session


# Function to fetch the IMDb Top-250 page
def fetch_top_movies(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None


# Function to parse movie data from the page
def parse_movies(soup):
    movies_data = []
    for col in soup.find_all('td', class_='titleColumn'):
        title_tag = col.find('a')
        year_tag = col.find('span')

        if title_tag and year_tag:
            title = title_tag.text
            year = year_tag.text.strip('()')
            link = f'https://www.imdb.com{title_tag["href"]}'
            movies_data.append({'Title': title, 'Year': year, 'IMDB Link': link})
    return movies_data


# Function to save movie details to HTML files
def save_movie_pages(session, link_list, num_movies=5):
    for n in range(min(num_movies, len(link_list))):
        try:
            r = session.get(link_list[n])
            r.raise_for_status()
            with open(f'page_{n}.html', 'w', encoding='utf-8') as output_file:
                output_file.write(r.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link_list[n]}: {e}")


# Main execution
if __name__ == "__main__":
    start_page = 'https://www.imdb.com/chart/top'
    session = create_session()

    page_content = fetch_top_movies(session, start_page)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        movies_data = parse_movies(soup)

        # Create DataFrame
        movies_df = pd.DataFrame(movies_data)

        # Save movie pages
        movie_links = movies_df['IMDB Link'].tolist()
        save_movie_pages(session, movie_links)

