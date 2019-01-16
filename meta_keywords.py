from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

url = 'http://www.espn.com/nfl/story/_/id/25770455/gregg-williams-defensive-coordinator-new-york-jets'

response = requests.get(url)
data = response.text
soup = bs(data, 'html.parser')
meta = soup.find('meta', {"name":"keywords"}).attrs['content']
keyword_arr = meta.split(',')
stripped = []

for i in keyword_arr:
    if i != " ":
        stripped.append(i.strip())

print(stripped)
