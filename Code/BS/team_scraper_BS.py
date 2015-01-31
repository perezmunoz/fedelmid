# to scrap team infos using BS4

from bs4 import BeautifulSoup
import re
import urllib
import string

# Get the location of a team given its url

def team_location(team_url):
	thisURL = "http://basketball-reference.com"+team_url
	soup = BeautifulSoup(urllib.urlopen(thisURL).read())
	tag = soup.find("div",class_="mobile_text")
	print(tag)

	# Work in progress - Simon

team_location("/teams/ATL/")
