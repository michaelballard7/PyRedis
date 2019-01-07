""" Remember to install and activate the redis server first """

import redis
import requests as r
import bs4 as soup

# establish the database connection
r = redis.Redis(host='localhost', port=6379, db=0)

r.set('foo',"bar")

print(r.get('foo'))