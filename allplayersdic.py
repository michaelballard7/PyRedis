from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

url = "https://www.basketball-reference.com/" #home
url_no_slash = "https://www.basketball-reference.com" #home

year_for_url = "2019.html"
response = requests.get(url)
data = response.text
soup = bs(data, 'html.parser')
all_teams = soup.find('div', {"id":"teams"})
teams = soup.find_all('a')

npo_all_player_games = {}
data_no = 0
for team in teams:
    if 'Franchise' in str(team.get('title')):
        team_url = url + team.get('href') + year_for_url #team url
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
                player_url = url + row.find('a').get('href') #player url
                # player_url = "https://www.basketball-reference.com/players/c/cartevi01.html"
                player_response = requests.get(player_url)
                player_data = player_response.text
                player_soup = bs(player_data, 'html.parser')
                name = player_soup.find('div', {"id":"info"})
                player_name = name.find('h1', {"itemprop":"name"}).text
                print(player_name)
                per = player_soup.find('div', {"id":"all_per_game"})
                if per:
                    table = per.find_all('tr', {"class":"full_table"})
                    for stat_row in table:
                        row = stat_row.find_all('th')
                        for r in row:

                            ## where we get the indivual seasons start new function around here
                            ## for r in row:
                            ##   get_season_stats(r)
                            ## something simple like this

                            table_break_count = 0
                            gamelog_anchor_tag = r.find('a')
                            print("gamelog_anchor_tag", gamelog_anchor_tag)
                            gamelog_url = gamelog_anchor_tag.get('href')
                            player_season_url = url_no_slash + gamelog_url #season url
                            season_response = requests.get(player_season_url)
                            season_data = season_response.text
                            season_soup = bs(season_data, 'html.parser')
                            season_body = season_soup.tbody
                            season_rows = season_body.find_all('tr')
                            stats = dict()
                            for r in season_rows:
                                th = r.find('th', {"data-stat":"ranker"}).text
                                if "Rk" not in th:
                                    for q in r.find_all('td'):
                                        if q.attrs['data-stat'] == 'reason':
                                            stats['date_game'].pop()
                                        elif q.attrs['data-stat'] not in stats:
                                            if q.text == "":
                                                stats[q.attrs['data-stat']] = [0]
                                            else:
                                                stats[q.attrs['data-stat']] = [q.text]
                                        else:
                                            if q.text == "":
                                                stats[q.attrs['data-stat']].append(0)
                                            else:
                                                stats[q.attrs['data-stat']].append(q.text)

                            game_count = 0
                            for game in stats['date_game']:
                                if 'plus_minus' not in stats:
                                    stats['plus_minus'] = []
                                    for i in stats['date_game']:
                                        stats['plus_minus'].append('not tracked')
                                # print('FOR LOOP: ', stats['age'][game_count], stats['opp_id'][game_count])
                                npo_all_player_games[data_no] = [player_name, stats['date_game'][game_count], stats['age'][game_count], stats['game_location'][game_count], stats['team_id'][game_count], stats['opp_id'][game_count], stats['game_result'][game_count], stats['gs'][game_count], stats['mp'][game_count], stats['fg'][game_count], stats['fga'][game_count], stats['fg3'][game_count], stats['fg3a'][game_count],  stats['fg3_pct'][game_count], stats['ft'][game_count], stats['fta'][game_count], stats['ft_pct'][game_count], stats['orb'][game_count], stats['drb'][game_count], stats['trb'][game_count], stats['ast'][game_count], stats['stl'][game_count], stats['blk'][game_count], stats['tov'][game_count], stats['pf'][game_count], stats['pts'][game_count], stats['game_score'][game_count], stats['plus_minus'][game_count]]
                                data_no += 1
                                game_count += 1
                        npo_all_player_games_df = pd.DataFrame.from_dict(npo_all_player_games, orient = 'index', columns = ['Name', 'Dates', 'Age', 'Location', 'Team', 'Opponent', 'Game Result', 'Started', 'Minutes Played', 'FG', 'FGA', 'FG3', 'FG3A', 'FG3Pct', 'FreeThrows', 'Free Throw Attempts', 'Free Throw Percent', 'Offensive Rebounds', 'Defensive Rebounds', 'Total Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'Personal Fouls', 'Points', 'Game Score', 'Plus Minus'])
                        # print(npo_all_player_games_df.head())
                        npo_all_player_games_df.to_csv('npo_all_player_games_dict.csv')
