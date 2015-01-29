# Provide the links for both players and teams

from bs4 import BeautifulSoup
import re
import urllib
import string


# Get the links to the players' page

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	res=[]
	soup = BeautifulSoup(html)
	for player in soup.tbody.find_all('tr'):
		res.append(str(player.td.a.get('href')))
     	return res

# Get the links for all the players
# Return a list with results of the form /players/letter/name.html
def all_players_links():
	alphabet = string.ascii_lowercase
	res = []
	for c in alphabet:
		if c!='x':      #There is no player whose name starts with x
			res+=players_links(c)
	return res


# Get links for the teams

def teams_links():
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/teams')
	html=urlHandle.read()
	soup = BeautifulSoup(html)
	res=[]
	for team in soup.find_all(class_="full_table"):  # To get all the teams
	# for team in soup.tbody.find_all(class_="full_table"):  # To get only the current teams
		res.append(str(team.td.a.get('href')))
	return res


# Calculate the number of players to check the results

# Calculate the number of players whose names start with the letter c
def number_players(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	soup = BeautifulSoup(html)
	s = soup.h2.string
	m = re.search('[0-9]+',s)
	return m.group(0)

# Calculate the number of all the players on basketball-reference
def number_all_players():
	alphabet = string.ascii_lowercase
	res=0
	for c in alphabet:
		if c!='x':		#There is no player whose name starts with x
			res+=number_players(c)
	return res
