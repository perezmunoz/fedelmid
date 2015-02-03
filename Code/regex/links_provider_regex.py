# Provide the links for both players and teams

import re
import urllib
import string

##########################################################
# Get the links to the players' page
##########################################################

# Get player's first letter in name
# Return a list of the form ['a', 'b', ..., 'z']
def letters_players():
	letters = []
	# Opening player's page
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/')
	html = urlHandle.read()
	needle = '<a href="/players/([a-z]+)/">[A-Z]+</a></td>'
	# Get the letters
	letters = re.findall(needle, html)
	return letters


# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	needle = '[^p]><a href="(/players/./.+)"'    # We use a '.'' for 'letter' because some players change names. In this case 'letter' might not be the same as c.
	m = re.findall(needle, html)
	return m

# Get the links for all the players
# Return a list with results of the form /players/letter/name.html
def all_players_links():
	alphabet = letters_players()
	res = []
	for c in alphabet:
		res+=players_links(c)
		time.sleep(2)
	return res

##########################################################
# Get the links to the teams' page
##########################################################

# Get the links for all the teams
# Return a list with results of the form /team/name/
def all_teams_links():
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/teams')
	html=urlHandle.read()
	needle = 'href="(/teams/[A-Z]+/)"'
	res = re.findall(needle, html)
	return res

##########################################################
# Calculate the number of players to check the results
##########################################################

# Retrieve the number of players whose names start with the letter c 
# Return an integer
def number_players(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	needle = '<h2 data-mobile-header="" style="">(.+) Players</h2>'
	m = re.search(needle, html)
	return int(m.group(1))

# Calculate the number of all the players on basketball-reference
# Return an integer
def number_all_players():
	alphabet = letters_players()
	res=0
	for c in alphabet:
		res+=number_players(c)
		time.sleep(2)
	return res
