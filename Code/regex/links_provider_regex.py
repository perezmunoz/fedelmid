# Provide the links for both players and teams

import re
import urllib
import string


# Get the links to the players' page

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	needle = '[^p]><a href="(/players/./.+)"'
	# We use a '.'' for 'letter' because some players change names. In this case 'letter' might not be the same as c.
	m = re.findall(needle, html)
	return m

# Get the links for all the players
# Return a list with results of the form /players/letter/	name.html
def all_players_links():
	alphabet = string.ascii_lowercase
	res = []
	for c in alphabet:
		if c!='x':
		#There is no player whose name starts with x	
			res+=players_links(c)
	return res

# Get the links for all the teams

def teams_links():
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/teams')
	html=urlHandle.read()
	needle = 'href="(/teams/[A-Z]+/)"'
	res = re.findall(needle, html)
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