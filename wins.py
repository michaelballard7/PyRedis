from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

url = "https://www.basketball-reference.com/"

response = requests.get(url)
data = response.text
soup = bs(data, 'html.parser')
all_teams = soup.find('div', {"id":"teams"})
teams = all_teams.find_all('a')
for team in teams:
    if 'Franchise' in str(team.get('title')):
        team_url = url + team.get('href')
        team_response = requests.get(team_url)
        team_data = team_response.text
        team_soup = bs(team_data, 'html.parser')
        # team_table = team_soup.find(class_="sortable stats_table")
        team_table = team_soup.tbody
        team_name_index = re.search(r"\ Franchise", team_soup.title.text)
        team_name_index = team_name_index.start()
        team_name = team_soup.title.text[0:team_name_index]
        # print(team_name)
        wins = []
        for row in team_table.find_all('tr'):
            for td in row.find_all("td", {"class":"right"}):
                if td.attrs['data-stat'] == "wins":
                    wins.append(td.text)
        print(team_name, '\nWins', wins, '\n----')
