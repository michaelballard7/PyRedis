from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

url = "https://www.basketball-reference.com/"

year = "2019.html"
response = requests.get(url)
data = response.text
soup = bs(data, 'html.parser')
all_teams = soup.find('div', {"id":"teams"})
teams = soup.find_all('a')

npo_teams = {}
data_no = 0
for team in teams:
    if 'Franchise' in str(team.get('title')):
        team_url = url + team.get('href') + year
        team_response = requests.get(team_url)
        team_data = team_response.text
        team_soup = bs(team_data, 'html.parser')

        content = team_soup.find('div', {"id":"content"})
        per = content.find('div', {"id":"all_per_game"})
        if per:
            head = per.find('thead')
            divs = per.find_all('div')
            body = content.find_all('tbody')
            rows = body[0].find_all('tr')
            for row in rows:
                player_url = url + row.find('a').get('href')
                player_response = requests.get(player_url)
                player_data = player_response.text
                player_soup = bs(player_data, 'html.parser')
                per = player_soup.find('div', {"id":"all_per_game"})
                if per:
                    table = per.find_all('tr', {"class":"full_table"})
                    fg_per_g = []
                    fga_per_g = []
                    for stat_row in table:
                        row = stat_row.find_all('td')
                        for r in row:
                            if r.attrs['data-stat'] == "fg_per_g":
                                fg_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fga_per_g":
                                fga_per_g.append(r.text)
                    print('Field Goals Per Game:', fg_per_g, '\nField Goal Attempts Per Game:', fga_per_g)
                    print(player_url, '\n-----------------------------------------------------------')
