""" Remember to install and activate the redis server first """

# https://stackoverflow.com/questions/8810036/complex-data-structures-redis
# https://redis-py.readthedocs.io/en/latest/_modules/redis/client.html#Redis.hmset

import redis
import requests as resp
from bs4 import BeautifulSoup as bs
import json
import pprint

# header values to bypass site filters
headerValues = {
     "User-Agent" : "Michael Ballard App / 1.0.0"
    }

# url for scraping
url = "https://www.basketball-reference.com/teams/DEN/"

# establish the database connection
r = redis.Redis(host='localhost', port=6379, db=0)

# request and response object
response = resp.get(url, headers=headerValues)

# raw response text stripped of spaces
data = response.text.strip()

# create soup object to access bs4 methods
soup = bs(data, 'html.parser')

# use bs4 find method to locate table element on page
table = soup.find(class_="sortable stats_table")

# find the table body element
table_body = soup.tbody

wins = []

# iterate throught t body to findAll rows
for row in table_body.findAll("tr"):
    for td in row.findAll("td", {"class":"right"}):
           if td.attrs['data-stat'] == "wins":
               wins.append(td.text)

print(wins)

# Shawn firt Scrappin
# for row in table_body.findAll("tr"):
#     for td in row.findAll("td"):
#         if "wins" in str(td):
#             print(str(td)[-7:-5])

# dicty = {"pg":"D Russell", "sg": "m ballard", "sf":"lawerence", "pf":"jath", "c":"malorie"}
# r.set('foo',"bar")
# print(r.get('foo'))
# r.mset(dicty)
# print("Brooklyn Players: {}".format((r.mget("pg", "c"))))
# print("The key pg",r.get('pg'))
# r.hmset("team13", "pg" "D Russell" "sg" "M ballard" )
# print(r.hgetall("team13"))
# r.hmset("brooklyn", dicty)
# print(r.hgetall("brooklyn"))
# print(r.keys())
