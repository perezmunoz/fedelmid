# to scrap team infos using BS4

from bs4 import BeautifulSoup
import re
import urllib
import string
import os
import csv
import time

# Get the html of a specific team given its url

def get_html(team_url):
	return urllib.urlopen("http://basketball-reference.com"+team_url).read()


# Location of a team

def team_location(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	location_str = tag.contents[0].contents[1]
	location_str = location_str[1:len(location_str)-1]
	(city,state) = location_str.split(",")
	(city,state) = (city,state[1:len(state)-1])
	return city,state

# Name of the team

def team_name(html):
	soup = BeautifulSoup(html)
	tag = soup.find("h1")
	name = tag.string[0:len(tag.string)-16] # Deleting the phrase "Franchise Index"
	return name

# Season statistics

def team_seasons(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	season_infos = re.search("Seasons:.*\n",text).group()

	# Number of seasons
	nbrSeasons = re.search("Seasons: [0-9]+",season_infos).group()
	nbrSeasons = re.compile("Seasons: | ").sub("",nbrSeasons)

	# Year of first season
	firstSeason = re.search("Seasons:.*to",season_infos).group()
	firstSeason = re.compile("Seasons:.*; |-[0-9][0-9] to").sub("",firstSeason)

	# Year of last season
	lastSeason = re.search("to.*\n",season_infos).group()
	lastSeason = re.compile("to |-[0-9][0-9]\n").sub("",lastSeason)

	return nbrSeasons,firstSeason,lastSeason


# Win-Loss statistics

def team_WL(html):
	soup = BeautifulSoup(html)
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

	return wNbr,lNbr,"0"+wl_percentage


# Number of playoff appearances

def team_playoff(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	text = re.search("Playoff Appearances: [0-9]+",text).group()
	remote_word = re.compile("Playoff Appearances: |\n")
	return remote_word.sub("",text)

# Number of championships

def team_championships(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	text = re.search("Championships: [0-9]+",text).group()
	remote_word = re.compile("Championships: |\n")
	return remote_word.sub("",text)

# Function to know if a team has already been added to the csv file
def teamIsAlreadyInCsv(team_id, path):
	with open(path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			if row[0] == team_id:
				return True
		return False

# Write the team's basic info in the proper csv file
def load_team_basic_info(team_url):

	# Test if the file already exists, if not, it creates it
	if not os.path.isfile("teams_basic_info.csv"):
		output = open("teams_basic_info.csv", 'w')
		# Write the header
		output.write("Team_id,City,State,Seaons,First_Season,Last_Season,Wins,Losses,Win_Lose_Percentage,Playoff_Appearances,Championships\n")
	else:
		output = open("teams_basic_info.csv", 'a')

	# Calculate the team's id
	remote_word = re.compile("/teams/|/")
	team_id =remote_word.sub("",team_url)

	# Test if the team is already in the csv file
	if teamIsAlreadyInCsv(team_id,"teams_basic_info.csv"):
		print("team "+team_id+" had already been added")
		return False	

	# Fill the csv
	html = get_html(team_url)
	team_info=""
	team_info += team_id+","
	for loc in team_location(html):
		team_info += loc+","

	for sea in team_seasons(html):
		team_info += sea+","

	for wl in team_WL(html):
		team_info += wl+","

	team_info += team_playoff(html)+","+team_championships(html)
	output.write(team_info+"\n")
	output.close()

# Write the team's statistics in the proper csv file
# The team id is a three letters abbreviation of the team name like it is used in the url of the pages of the teams
# Example, the Boston Celtics abbreviation is "BOS" because the url of its page is http://www.basketball-reference.com/teams/BOS/
# I didn't keep the last two  columns because they are useless and they would complexify our sql table
def load_statistics_team(team_url):
	# Test if the file already exists, if not, it creates it
	if not os.path.isfile("teams_statistics.csv"):
		output = open("teams_statistics.csv", 'w')
		output.write("Team_id,Season,Lg,Team,W,L,WL_percentage,Finish,SRS,Pace,Rel_Pace,ORtg,Rel_ORtg,DRtg,Rel_DRtg,Playoffs\n")
	else:
		output = open("teams_statistics.csv", 'a')

	html = get_html(team_url)
	soup = BeautifulSoup(html)
	remote_word = re.compile("/teams/|/")
	team_id =remote_word.sub("",team_url)

	# Test if the team is already in the csv file
	if teamIsAlreadyInCsv(team_id,"team_statistics.csv"):
		print("team "+team_id+" had already been added")
		return False	
	
	# Getting relevant tables into the dictionary dict
	table = soup.find('table', {'id': team_id})

	# Scrap lines from table
	body = table.tbody.find_all('tr')
	for row in body:
		data = row.find_all('td')
		output.write(team_id+',')
		for i in range(len(data)):
			# If we arrived to the column "coach" we break the loop, we don't keep the last two columns
			try:
				if re.compile("coaches").search(data[i].a["href"]):
					break
			except:
				pass
			text_to_write = data[i].get_text()+','
			output.write(text_to_write.encode('utf-8'))
		output.write("\n")
	print 'team table has been scraped into team_statistics.csv'
	output.close()

# Main

# # Get links for the teams
# # Return a list with results of the form /teams/name/
# def all_teams_links():
# 	urlHandle = urllib.urlopen('http://www.basketball-reference.com/teams')
# 	html = urlHandle.read()
# 	soup = BeautifulSoup(html)
# 	res = []
# 	# To get all the teams
# 	for team in soup.find_all(class_="full_table"):
# 		# Get only the current teams present in soup.tbody.find_all(class_="full_table")
# 		res.append(str(team.td.a.get('href')))
# 	return res

# teams = all_teams_links()

# # Going into the "Data" directory
# os.chdir("C:\\Users\\Simon\\Documents\\Project HowBA\\NBA\\Data")

# # Writing team_stats in this directory
# for team_url in teams:
# 	print("currently loading stats from "+team_url)
# 	load_statistics_team(team_url)
# 	time.sleep(2)

# print("loading of statistics ended")

# # Writing team_basic_info in this directory
# for team_url in teams:
# 	print("currently loading basic info from "+team_url)
# 	load_team_basic_info(team_url)
# 	time.sleep(2)

# print("loading of basic info ended")