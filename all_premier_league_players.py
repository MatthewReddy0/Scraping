from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd


def get_players_match_log_hyperlinks(url: str, number_of_players: int) -> pd.DataFrame:
    driver = webdriver.Chrome(executable_path=r"C:\Users\reddy\Downloads\chromedriver_win32\chromedriver.exe")

    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, features="lxml")

    with open('All_PL_Players.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    player_match_log_urls_names_clubs = []

    count = 0

    for link in soup.find_all('a', href=True):
        if count == number_of_players:
            break
        if '/en/players/' in str(link['href']) and 'Match-Logs' in str(link['href']):
            name = soup.select(f'#stats_standard > tbody > tr:nth-child({str(count + 1)}) > td:nth-child(2) > a')[0]
            name = name.text
            club = soup.select(f'#stats_standard > tbody > tr:nth-child({str(count + 1)}) > td:nth-child(5) > a')[0]
            club = club.text

            player_match_log_urls_names_clubs.append([str(link['href']), name, club])
            count += 1

    return pd.DataFrame(player_match_log_urls_names_clubs, columns=['URL', 'Player', 'Club'])


# host = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'
# player_urls = get_players_match_log_hyperlinks(host, 1)
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(player_urls)
