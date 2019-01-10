from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

url = "https://www.basketball-reference.com/"

year_for_url = "2019.html"
response = requests.get(url)
data = response.text
soup = bs(data, 'html.parser')
all_teams = soup.find('div', {"id":"teams"})
teams = soup.find_all('a')

npo_players = {}
data_no = 0
for team in teams:
    if 'Franchise' in str(team.get('title')):
        team_url = url + team.get('href') + year_for_url
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
                # print('SOUP', player_soup)
                name = player_soup.find('h1', {"itemprop":"name"}).text
                # print(name)
                per = player_soup.find('div', {"id":"all_per_game"})
                if per:
                    table = per.find_all('tr', {"class":"full_table"})
                    count = 0
                    start_year = 2019
                    year = []
                    age = []
                    team_id = []
                    pos = []
                    g = []
                    gs = []
                    mp_per_g = []
                    fg_per_g = []
                    fga_per_g = []
                    fg_pct = []
                    fg3_per_g = []
                    fg3a_per_g = []
                    fg3_pct = []
                    fg2_per_g = []
                    fg2a_per_g = []
                    fg2_pct = []
                    efg_pct = []
                    ft_per_g = []
                    fta_per_g = []
                    ft_pct = []
                    orb_per_g = []
                    drb_per_g = []
                    ast_per_g = []
                    stl_per_g = []
                    blk_per_g = []
                    tov_per_g = []
                    pf_per_g = []
                    pts_per_g = []

                    for stat_row in table:
                        year.insert(0, start_year)
                        start_year -= 1
                        row = stat_row.find_all('td')
                        for r in row:
                            if r.attrs['data-stat'] == "age":
                                age.append(r.text)
                            if r.attrs['data-stat'] == "team_id":
                                team_id.append(r.text)
                            if r.attrs['data-stat'] == "pos":
                                pos.append(r.text)
                            if r.attrs['data-stat'] == "g":
                                g.append(r.text)
                            if r.attrs['data-stat'] == "gs":
                                gs.append(r.text)
                            if r.attrs['data-stat'] == "mp_per_g":
                                mp_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fg_per_g":
                                fg_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fga_per_g":
                                fga_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fg_pct":
                                fg_pct.append(r.text)
                            if r.attrs['data-stat'] == "fg3_per_g":
                                fg3_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fg3a_per_g":
                                fg3a_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fg3_pct":
                                fg3_pct.append(r.text)
                            if r.attrs['data-stat'] == "fg2_per_g":
                                fg2_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fg2a_per_g":
                                fg2a_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fg2_pct":
                                fg2_pct.append(r.text)
                            if r.attrs['data-stat'] == "efg_pct":
                                efg_pct.append(r.text)
                            if r.attrs['data-stat'] == "ft_per_g":
                                ft_per_g.append(r.text)
                            if r.attrs['data-stat'] == "fta_per_g":
                                fta_per_g.append(r.text)
                            if r.attrs['data-stat'] == "ft_pct":
                                ft_pct.append(r.text)
                            if r.attrs['data-stat'] == "orb_per_g":
                                orb_per_g.append(r.text)
                            if r.attrs['data-stat'] == "drb_per_g":
                                drb_per_g.append(r.text)
                            if r.attrs['data-stat'] == "ast_per_g":
                                ast_per_g.append(r.text)
                            if r.attrs['data-stat'] == "stl_per_g":
                                stl_per_g.append(r.text)
                            if r.attrs['data-stat'] == "blk_per_g":
                                blk_per_g.append(r.text)
                            if r.attrs['data-stat'] == "tov_per_g":
                                tov_per_g.append(r.text)
                            if r.attrs['data-stat'] == "pf_per_g":
                                pf_per_g.append(r.text)
                            if r.attrs['data-stat'] == "pts_per_g":
                                pts_per_g.append(r.text)
                    print(name, player_url)
                    print('\nYear', year, '\nAge:', age, '\nTeam:', team_id, '\nPosition:', pos, '\nGames:', g, '\nGames Started:', gs, '\nMinutes Per Game', mp_per_g, '\nField Goals Per Game:', fg_per_g, '\nField Goal Attempts Per Game:', fga_per_g, '\nField Goal Percent:', fg_pct, '\n3-Point Field Goals Per Game:', fg3_per_g, '\n3-Point Field Goal Attempts Per Game:', fg3a_per_g, '\n3-Point Field Goal Percent:', fg3_pct, '\n2-Point Field Goals Per Game:', fg2_per_g, '\n2-Point Field Goal Attempts Per Game:', fg2a_per_g, '\n2-Point Field Goal Percent:', fg2_pct, '\nEffective Field Goal Percent:', efg_pct, '\nFree Throws Per Game:', ft_per_g, '\nFree Throw Attempts Per Game:', fta_per_g, '\nFree Throw Percent:', ft_pct, '\nOffensive Rebounds Per Game:', orb_per_g, '\nDefensive Rebounds Per Game:', drb_per_g, '\nAssists Per Game:', ast_per_g, '\nSteals Per Game:', stl_per_g, '\nBlocks Per Game:', blk_per_g, '\nTurnovers Per Game:', tov_per_g, '\nPersonal Fouls Per Game:', pf_per_g, '\nPoints Per Game:', pts_per_g)
                    print('\n-----------------------------------------------------------')
                    for years in age:
                        npo_players[data_no] = [name, year[count], age[count], team_id[count], pos[count], g[count], gs[count], mp_per_g[count], fg_per_g[count], fga_per_g[count], fg_pct[count], fg3_per_g[count], fg3a_per_g[count], fg3_pct[count], fg2_per_g[count], fg2a_per_g[count], fg2_pct[count], efg_pct[count], ft_per_g[count], fta_per_g[count], ft_pct[count], orb_per_g[count], drb_per_g[count], ast_per_g[count], stl_per_g[count], blk_per_g[count], tov_per_g[count], pf_per_g[count], pts_per_g[count]]
                        data_no += 1
                        count += 1

npo_players_df = pd.DataFrame.from_dict(npo_players, orient = 'index', columns = ['Name', 'Year', 'Age', 'Team', 'Position', 'Games', 'Games Started', 'Minutes Per Game', 'Field Goals Per Game', 'Field Goal Attempts Per Game', 'Field Goal Percent', '3-Point Field Goals Per Game', '3-Point Field Goal Attempts Per Game', '3-Point Field Goal Percent', '2-Point Field Goals Per Game', '2-Point Field Goal Attempts Per Game', '2-Point Field Goal Percent', 'Effective Field Goal Percent', 'Free Throws Per Game', 'Free Throw Attempts Per Game', 'Free Throw Percent', 'Offensive Rebounds Per Game', 'Defensive Rebounds Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game', 'Turnovers Per Game', 'Personal Fouls Per Game', 'Points Per Game'])
print(npo_players_df.head())
npo_players_df.to_csv('npo_players.csv')









# '\nAge:', age, '\nTeam:', team_id, '\nGames:', g, '\nGames Started:', gs, '\nMinutes Per Game', mp_per_g
# , '\nField Goal Percent:', fg_pct, '\n3-Point Field Goals Per Game:', fg3_per_g, '\n3-Point Field Goal Attempts Per Game:', fg3a_per_g, '\n3-Point Field Goal Percent:', fg3_pct, '\n2-Point Field Goals Per Game:', fg2_per_g, '\n2-Point Field Goal Attempts Per Game:', fg2a_per_g, '\n2-Point Field Goal Percent:', fg2_pct, '\nEffective Field Goal Percent:', efg_pct, '\nFree Throws Per Game:', ft_per_g, '\nFree Throw Attempts Per Game:', fta_per_g, '\nFree Throw Percent:', ft_pct, '\nOffensive Rebounds Per Game:', orb_per_g, '\nDefensive Rebounds Per Game:', drb_per_g, '\nAssists Per Game:', ast_per_g, '\nSteals Per Game:', stl_per_g, '\nBlocks Per Game:', blk_per_g, '\nTurnovers Per Game:', tov_per_g, '\nPersonal Fouls Per Game:', pf_per_g, '\nPoints Per Game:', pts_per_g


# name, age[count], team_id[count], g[count], gs[count], mp_per_g[count], fg_per_g[count], fga_per_g[count], fg_pct[count], fg3_per_g[count], fg3a_per_g[count], fg3_pct[count], fg2_per_g[count], fg2a_per_g[count], fg2_pct[count], efg_pct[count], ft_per_g[count], fta_per_g[count], ft_pct[count], orb_per_g[count], drb_per_g[count], ast_per_g[count], stl_per_g[count], blk_per_g[count], tov_per_g[count], pf_per_g[count], pts_per_g[count]
