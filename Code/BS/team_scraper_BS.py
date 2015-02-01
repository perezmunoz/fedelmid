# to scrap team infos using BS4

from bs4 import BeautifulSoup
import re
import urllib
import string

# Get the soup of a specific team given its url

def get_soup(team_url):
	return BeautifulSoup(urllib.urlopen("http://basketball-reference.com"+team_url).read())

team_url = "/teams/BOS/"
soup = get_soup(team_url)

# Location of a team

def team_location():
	tag = soup.find("div",class_="mobile_text")
	location_str = tag.contents[0].contents[1]
	location_str = location_str[1:len(location_str)-1]
	return location_str.split(",")

print(team_location())

# Name of the team

def team_name():
	tag = soup.find("h1")
	name = tag.string[0:len(tag.string)-16] # Deleting the phrase "Franchise Index"
	return name

print("Name = " + team_name())

# Season statistics

def team_nbrSeasons():
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	season_infos = re.search("Seasons:.*\n",text).group()

	# Number of seasons
	nbrSeasons = re.search("Seasons: [0-9]+;",season_infos).group()
	nbrSeasons = re.compile("Seasons: |;").sub("",nbrSeasons)

	# Year of first season
	firstSeason = re.search("Seasons:.*to",season_infos).group()
	firstSeason = re.compile("Seasons: [0-9]*; |-[0-9][0-9] to").sub("",firstSeason)

	# Year of last season
	lastSeason = re.search("to.*\n",season_infos).group()
	lastSeason = re.compile("to |-[0-9][0-9]\n").sub("",lastSeason)

	return int(firstSeason),int(lastSeason),int(nbrSeasons)

	# tag = soup.find("div",class_="mobile_text")
	# seasons = tag.contents[0].contents[2].contents[2].contents[1].string
	# nbrSeasons = re.search('[0-9]+',seasons).group()
	# return nbrSeasons
print("First season, Last season, Number of seasons")
print(team_nbrSeasons())

# Win-Loss statistics

def team_WL():
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	record = re.search("Record: .*\n",text).group()

	# WL percentage
	wl_percentage = re.search(", .*%",record).group()
	wl_percentage = re.compile(", | W-L%").sub("",wl_percentage)

	# Nbr wins
	wNbr = re.search("[0-9]*-",record).group()
	wNbr = re.compile("-").sub("",wNbr)

	# Nbr losses
	lNbr = re.search("-[0-9]*",record).group()
	lNbr = re.compile("-").sub("",lNbr)

	return int(wNbr),int(lNbr),float("0"+wl_percentage)

print("Number of wins, Number of losses, Win-Loss percentage")
print(team_WL())

# Number of playoff appearances

def team_playoff():
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	text = re.search("Playoff Appearances: [0-9]*\n",text).group()
	remote_word = re.compile("Playoff Appearances: |\n")
	return remote_word.sub("",text)

print("Playoff Appearances = " + team_playoff())

# Number of championships

def team_championships():
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	text = re.search("Championships: [0-9]*\n",text).group()
	remote_word = re.compile("Championships: |\n")
	return remote_word.sub("",text)

print("Championships: = " + team_championships())