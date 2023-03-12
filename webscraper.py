# https://realpython.com/beautiful-soup-web-scraper-python/
# Modul requests (pip install requests)
import requests
# Import knihovny BeautifulSoup4 (pip install beautifulsoup4), která usnadňuje web scraping
from bs4 import BeautifulSoup
import json

# Konstanta obsahující adresu webu, z něhož chceme získávat data
# Žebříček 100 momentálně nejlépe hodnocených hráčů Valorantu
URL = 'https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=eu'

# Odeslání požadavku metodou get na určenou URL adresu - HTTP server vrací zpět obsah stránky
page = requests.get(URL, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
page = requests.get(URL)
# Vytvoření objektu parseru stránky
soup = BeautifulSoup(page.content, 'html.parser')
player_link = soup.findAll("a", attrs={"class": None})
player_name = soup.select('span.trn-ign__username')
player_img = soup.select('div.avatar>img.picture')
player_rank = soup.select('table.trn-table>tbody>tr>td.rank')
player_urls = [f'https://tracker.gg{tag["href"]}' for tag in player_link]
# Kontrolní výpis získaných údajů
with open("leaderboard.json",  "w", encoding='utf-8') as file:
    file.write('[\n')
    for i in range(len(player_name)):
        print(i)
        row = f'"rank": "{i+1}", "name": "{player_name[i].text.strip()}", "link": "{player_urls[i+3]}", "img": "{player_img[i].get("src")}"'
        row = '{' + row + '}'
        row = row + ', \n' if i != 99 else row + "\n"
        file.write(row)
    file.write(']')
