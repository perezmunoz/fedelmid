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

=============================================================================================
"Juan's code"
=============================================================================================

from bs4 import BeautifulSoup
import urllib # Library used to open links
import re
import time

# URL start point url = http://www.basketball-reference.com
# For name's players starting with a, the URL is ".../players/a"

# Get player's first letter in name
def get_letters_players():
	# Links are stored in an unique <table>...</table> HTML tag
	links = []

	# Opening index.html file which corresponds to url
	index = BeautifulSoup(urllib.urlopen('http://www.basketball-reference.com/players/').read())

	for row in index('td', {'class': 'align_center bold_text valign_bottom xx_large_text'}):
		links.append(str(row.a.get('href').split('/')[2]))

	# links represent the list of alphabetical players names
	# Ex: links[0] = /players/a/
	return links

# Get player's links and names for a specific letter
def get_players_by_letter(letter):

	# List containing player's links
	links_players = []

	# List containing player's names
	names_players = []

	# Index of players whose name start by 'letter'
	index = BeautifulSoup(urllib.urlopen('http://www.basketball-reference.com/players/'+letter).read())
	
	# Retrieve url links or names
	for row in index('a', href=re.compile('/players/'+letter)):
		# Sleeps 1 second
		# time.sleep(1)
		links_players.append(str(row.get('href').split('/')[3]))
		names_players.append(str(row.get_text()))
	
	return links_players, names_players

# Note: result can be stored in res = [[]] (list of list)
# Then res[0] = links_players and res[1] = names_players
# For each, elements are accessed by res[0][50] = links_players[50]

# Get all links and names of the players
def get_all_players():

    alphabetical = get_letters_players()

    # Lists containing links and name's players
    all_links_players = []
    all_names_players = []

    for letter in alphabetical:
    	all_players = get_players_by_letter(letter)
    	all_links_players += all_players[0]
    	all_names_players += all_players[1]

    return all_links_players, all_names_players

# Launching the code
# List of list containing links and name's players
# res = [[]]
# res = get_all_players()

# res[0] contains links and res[1] contains name's players


