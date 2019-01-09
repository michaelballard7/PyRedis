from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

url = "https://www.basketball-reference.com/"

response = requests.get(url)
data = response.text
soup = bs(data, 'html.parser')
all_teams = soup.find('div', {"id":"teams"})
teams = soup.find_all('a')

npo_teams = {}
data_no = 0
for team in teams:
    if 'Franchise' in str(team.get('title')):
        team_url = url + team.get('href')
        team_response = requests.get(team_url)
        team_data = team_response.text
        team_soup = bs(team_data, 'html.parser')
        team_table = team_soup.tbody
        team_name_index = re.search(r"\ Franchise", team_soup.title.text)
        team_name_index = team_name_index.start()
        team_name = team_soup.title.text[0:team_name_index]
        season = 2019
        count = 0
        wins = []
        losses = []
        win_loss_pct = []
        rank_team = []
        srs = []
        pace = []
        pace_rel = []
        off_rtg = []
        off_rtg_rel = []
        def_rtg = []
        def_rtg_rel = []
        rank_team_playoffs = []
        coaches = []
        top_ws = []
        for row in team_table.find_all('tr'):
            for td in row.find_all("td"):
                if td.attrs['data-stat'] == "wins":
                    wins.append(td.text)
                if td.attrs['data-stat'] == "losses":
                    losses.append(td.text)
                if td.attrs['data-stat'] == "win_loss_pct":
                    win_loss_pct.append(td.text)
                if td.attrs['data-stat'] == "rank_team":
                    rank_team.append(td.text)
                if td.attrs['data-stat'] == "srs":
                    srs.append(td.text)
                if td.attrs['data-stat'] == "pace":
                    if td.text == "":
                        pace.append('None')
                    else:
                        pace.append(td.text)
                if td.attrs['data-stat'] == "pace_rel":
                    if td.text == "":
                        pace_rel.append('None')
                    else:
                        pace_rel.append(td.text)
                if td.attrs['data-stat'] == "off_rtg":
                    if td.text == "":
                        off_rtg.append('None')
                    else:
                        off_rtg.append(td.text)
                if td.attrs['data-stat'] == "off_rtg_rel":
                    if td.text == "":
                        off_rtg_rel.append('None')
                    else:
                        off_rtg_rel.append(td.text)
                if td.attrs['data-stat'] == "def_rtg":
                    if td.text == "":
                        def_rtg.append('None')
                    else:
                        def_rtg.append(td.text)
                if td.attrs['data-stat'] == "def_rtg_rel":
                    if td.text == "":
                        def_rtg_rel.append('None')
                    else:
                        def_rtg_rel.append(td.text)
                if td.attrs['data-stat'] == "rank_team_playoffs":
                    if td.text == "":
                        rank_team_playoffs.append('None')
                    else:
                        rank_team_playoffs.append(td.text)
                if td.attrs['data-stat'] == "coaches":
                    coaches.append(td.text)
                if td.attrs['data-stat'] == "top_ws":
                    top_ws.append(td.text)

        print(team_name)
        for years in wins:
            season_string = str((season - 1)) + '-' + str(season)[2:4]
            npo_teams[data_no] = [team_name, season_string, wins[count], losses[count], win_loss_pct[count], rank_team[count], srs[count], pace[count], pace_rel[count], off_rtg[count], off_rtg_rel[count], def_rtg[count], def_rtg_rel[count], rank_team_playoffs[count], coaches[count], top_ws[count]]
            # print('SEASON:', season_string,'Wins:', wins[count], 'Loses:', losses[count], 'Win Loss Percent:', win_loss_pct[count], 'Division Rank:', rank_team[count], 'SRS:', srs[count], 'Pace:', pace[count], 'Pace Rel:', pace_rel[count], 'Off RTG:', off_rtg[count], 'OFF RTG REL:', off_rtg_rel[count], 'DEF RTG:', def_rtg[count], 'DEF RTG REL:', def_rtg_rel[count], 'PLAYOFFS:', rank_team_playoffs[count], 'Coaches:', coaches[count], 'Top WS:', top_ws[count])
            data_no += 1
            season -= 1
            count += 1

npo_teams_df = pd.DataFrame.from_dict(npo_teams, orient = 'index', columns = ['Team Name', 'Season', 'Wins', 'Losses', 'Win Percent', 'Division Rank', 'SRS', 'Pace', 'Relative Pace', 'Offensive Rating', 'Relative Offensive Rating', 'Defensive Rating', 'Relative Defensive Rating', 'Playoff Result', 'Coaches', 'Top Win Shares'])
print(npo_teams_df.head())
npo_teams_df.to_csv('npo_teams.csv')
