# Provide the links for both players and teams

import re
import urllib
import string


# Get the links to the players' page

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/name.html
def players_links(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	needle = '[^p]><a href="(/players/./.+)"'
	m = re.findall(needle, html)
	return m

# Get the links for all the players
# Return a list with results of the form /players/name.html
def all_players_links():
	alphabet = string.ascii_lowercase
	res = []
	for c in alphabet:
		if c!='x':
		#There is no player whose name starts with x	
			res+=get_players_links(c)
	return res

# Calculate the number of players to check the results

# Calculate the number of players whose names start with the letter c
def number_players(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	needle = '<h2 data-mobile-header="" style="">(.+) Players</h2>'
	m = re.search(needle, html)
	return int(m.group(1))

# Calculate the number of all the players on basketball-reference
def number_all_players():
	alphabet = string.ascii_lowercase
	res=0
	for c in alphabet:
		if c!='x':
		#There is no player whose name starts with x	
			res+=number_players(c)
	return res