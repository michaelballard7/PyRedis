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
                            count = 0
                            dates = []
                            age = []
                            team_id = []
                            game_location = []
                            opp_id = []
                            game_result = []
                            gs = []
                            mp = []
                            fg = []
                            fga = []
                            fg_pct = []
                            fg3 = []
                            fg3a = []
                            fg3_pct = []
                            ft = []
                            fta = []
                            ft_pct = []
                            orb = []
                            drb = []
                            trb = []
                            ast = []
                            stl = []
                            blk = []
                            tov = []
                            pf = []
                            pts = []
                            game_score = []
                            plus_minus = []
                            for r in season_rows:
                                th = r.find('th', {"data-stat":"ranker"}).text
                                table_break_count+=1
                                if table_break_count > 20:
                                    table_break_count = 0
                                else:
                                    date = r.find('td', {"data-stat":"date_game"}).text
                                    dates.append(date)
                                    for q in r.find_all('td'):
                                        if q.attrs['data-stat'] == 'reason':
                                            gs.append('dnp')
                                            mp.append('dnp')
                                            fg.append('dnp')
                                            fga.append('dnp')
                                            fg_pct.append('dnp')
                                            fg3.append('dnp')
                                            fg3a.append('dnp')
                                            fg3_pct.append('dnp')
                                            ft.append('dnp')
                                            fta.append('dnp')
                                            ft_pct.append('dnp')
                                            orb.append('dnp')
                                            drb.append('dnp')
                                            trb.append('dnp')
                                            ast.append('dnp')
                                            stl.append('dnp')
                                            blk.append('dnp')
                                            tov.append('dnp')
                                            pf.append('dnp')
                                            pts.append('dnp')
                                            game_score.append('dnp')
                                            plus_minus.append('dnp')
                                        if q.attrs['data-stat'] == "age":
                                            age.append(q.text)
                                        if q.attrs['data-stat'] == "team_id":
                                            team_id.append(q.text)
                                        if q.attrs['data-stat'] == "game_location":
                                            if q.text == "":
                                                game_location.append("home")
                                            else:
                                                game_location.append("away")
                                        if q.attrs['data-stat'] == "opp_id":
                                            opp_id.append(q.text)
                                        if q.attrs['data-stat'] == "game_result":
                                            game_result.append(q.text)
                                        if q.attrs['data-stat'] == "mp":
                                            mp.append(q.text)
                                        if q.attrs['data-stat'] == 'gs':
                                            gs.append(q.text)
                                        if q.attrs['data-stat'] == "fg":
                                            if q.text == "":
                                                fg.append(0)
                                            else:
                                                fg.append(q.text)
                                        if q.attrs['data-stat'] == "fga":
                                            if q.text == "":
                                                fga.append(0)
                                            else:
                                                fga.append(q.text)
                                        if q.attrs['data-stat'] == "fg_pct":
                                            if q.text == "":
                                                fg_pct.append(0.0)
                                            else:
                                                fg_pct.append(q.text)
                                        if q.attrs['data-stat'] == "fg3":
                                            if q.text == "":
                                                fg3.append(0)
                                            else:
                                                fg3.append(q.text)
                                        if q.attrs['data-stat'] == "fg3a":
                                            if q.text == "":
                                                fg3a.append(0)
                                            else:
                                                fg3a.append(q.text)
                                        if q.attrs['data-stat'] == "fg3_pct":
                                            if q.text == "":
                                                fg3_pct.append(0.0)
                                            else:
                                                fg3_pct.append(q.text)
                                        if q.attrs['data-stat'] == "ft":
                                            if q.text == "":
                                                ft.append(0)
                                            else:
                                                ft.append(q.text)
                                        if q.attrs['data-stat'] == "fta":
                                            if q.text == "":
                                                fta.append(0)
                                            else:
                                                fta.append(q.text)
                                        if q.attrs['data-stat'] == "ft_pct":
                                            if q.text == "":
                                                ft_pct.append(0.0)
                                            else:
                                                ft_pct.append(q.text)
                                        if q.attrs['data-stat'] == "orb":
                                            if q.text == "":
                                                orb.append(0)
                                            else:
                                                orb.append(q.text)
                                        if q.attrs['data-stat'] == "drb":
                                            if q.text == "":
                                                drb.append(0)
                                            else:
                                                drb.append(q.text)
                                        if q.attrs['data-stat'] == "trb":
                                            if q.text == "":
                                                trb.append(0)
                                            else:
                                                trb.append(q.text)
                                        if q.attrs['data-stat'] == "ast":
                                            if q.text == "":
                                                ast.append(0)
                                            else:
                                                ast.append(q.text)
                                        if q.attrs['data-stat'] == "stl":
                                            if q.text == "":
                                                stl.append(0)
                                            else:
                                                stl.append(q.text)
                                        if q.attrs['data-stat'] == "blk":
                                            if q.text == "":
                                                blk.append(0)
                                            else:
                                                blk.append(q.text)
                                        if q.attrs['data-stat'] == "tov":
                                            if q.text == "":
                                                tov.append(0)
                                            else:
                                                tov.append(q.text)
                                        if q.attrs['data-stat'] == "pf":
                                            if q.text == "":
                                                pf.append(0)
                                            else:
                                                pf.append(q.text)
                                        if q.attrs['data-stat'] == "pts":
                                            if q.text == "":
                                                pts.append(0)
                                            else:
                                                pts.append(q.text)
                                        if q.attrs['data-stat'] == "game_score":
                                            if q.text == "":
                                                game_score.append(0)
                                            else:
                                                game_score.append(q.text)
                                        if q.attrs['data-stat'] == "plus_minus":
                                            if q.text == "":
                                                plus_minus.append(0)
                                            else:
                                                plus_minus.append(q.text)
                            count+=1
                            game_count = 0
                            for game in dates:
                                # print('GOR LOOP: ', age[game_count], team_id[game_count])
                                npo_all_player_games[data_no] = [player_name, dates[game_count], age[game_count], game_location[game_count], team_id[game_count], opp_id[game_count], game_result[game_count], gs[game_count], mp[game_count], fg[game_count], fga[game_count], fg3[game_count], fg3a[game_count],  fg3_pct[game_count], ft[game_count], fta[game_count], ft_pct[game_count], orb[game_count], drb[game_count], trb[game_count], ast[game_count], stl[game_count], blk[game_count], tov[game_count], pf[game_count], pts[game_count], game_score[game_count], plus_minus[game_count]]
                                data_no += 1
                                game_count += 1
                        npo_all_player_games_df = pd.DataFrame.from_dict(npo_all_player_games, orient = 'index', columns = ['Name', 'Dates', 'Age', 'Location', 'Team', 'Opponent', 'Game Result', 'Started', 'Minutes Played', 'FG', 'FGA', 'FG3', 'FG3A', 'FG3Pct', 'FreeThrows', 'Free Throw Attempts', 'Free Throw Percent', 'Offensive Rebounds', 'Defensive Rebounds', 'Total Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'Personal Fouls', 'Points', 'Game Score', 'Plus Minus'])
                        # print(npo_all_player_games_df.head())
                        npo_all_player_games_df.to_csv('npo_all_player_games4.csv')
