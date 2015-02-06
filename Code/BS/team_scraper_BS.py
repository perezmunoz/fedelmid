# Provide the .csv file of team's statistics

from bs4 import BeautifulSoup
import re, urllib, string, os, csv, time

# Get the html of a specific team given its url
def get_html(team_url):
	return urllib.urlopen("http://basketball-reference.com"+team_url).read()

# Get the location of a team
def team_location(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	location_str = tag.contents[0].contents[1]
	location_str = location_str[1:len(location_str)-1]
	(city,state) = location_str.split(",")
	(city,state) = (city,state[1:len(state)])
	return city,state

# Get the name of a team
def team_name(html):
	soup = BeautifulSoup(html)
	tag = soup.find("h1")
	# Deleting the phrase "Franchise Index"
	name = tag.string[0:len(tag.string)-16]
	return name

# Get the Season's statistics
def team_seasons(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	# Get the Season's information
	season_infos = re.search("Seasons:.*\n",text).group()
	# Get the number of seasons
	nbrSeasons = re.search("Seasons: [0-9]+",season_infos).group()
	nbrSeasons = re.compile("Seasons: | ").sub("",nbrSeasons)
	# Get the year of first season
	firstSeason = re.search("Seasons:.*to",season_infos).group()
	firstSeason = re.compile("Seasons:.*; |-[0-9][0-9] to").sub("",firstSeason)
	# Get the year of last season
	lastSeason = re.search("to.*\n",season_infos).group()
	lastSeason = re.compile("to |-[0-9][0-9]\n").sub("",lastSeason)
	return nbrSeasons,firstSeason,lastSeason

# Get the Win-Loss statistics
def team_WL(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	record = re.search("Record: .*\n",text).group()
	# Get the WL percentage
	wl_percentage = re.search(", .*%",record).group()
	wl_percentage = re.compile(", | W-L%").sub("",wl_percentage)
	# Get the number of wins
	wNbr = re.search("[0-9]*-",record).group()
	wNbr = re.compile("-").sub("",wNbr)
	# Get the number of losses
	lNbr = re.search("-[0-9]*",record).group()
	lNbr = re.compile("-").sub("",lNbr)
	return wNbr,lNbr,"0"+wl_percentage

# Get the number of playoff appearances
def team_playoff(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	text = re.search("Playoff Appearances: [0-9]+",text).group()
	remote_word = re.compile("Playoff Appearances: |\n")
	return remote_word.sub("",text)

# Get the number of championships
def team_championships(html):
	soup = BeautifulSoup(html)
	tag = soup.find("div",class_="mobile_text")
	text = tag.text
	text = re.search("Championships: [0-9]+",text).group()
	remote_word = re.compile("Championships: |\n")
	return remote_word.sub("",text)

# Check if a team has already been added to the .csv file
def team_is_on_csv(team_id, path):
	with open(path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			if row[0] == team_id:
				return True
		return False

# Write the team's basic information in the proper .csv file
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
	# Test if the team is already in the .csv file
	if team_is_on_csv(team_id,"teams_basic_info.csv"):
		print("team "+team_id+" had already been added")
		return False	
	# Fill the csv
	html = get_html(team_url)
	team_info = ""
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

# Write the team's statistics in the proper .csv file
# The team id is a three letters abbreviation of the team name like it is used in the url of the pages of the teams
# Example, the Boston Celtics abbreviation is "BOS" because the url of its page is http://www.basketball-reference.com/teams/BOS/
# I didn't keep the last two columns because they are useless and they would complexify our SQLite table
def load_statistics_team(team_url):
	# Test if the file already exists, if not, it creates it
	if not os.path.isfile("teams_statistics.csv"):
		output = open("teams_statistics.csv", 'w')
		output.write("Team_id,Season,Lg,Team,W,L,WL_percentage,Finish,SRS,Pace,Rel_Pace,ORtg,Rel_ORtg,DRtg,Rel_DRtg,Playoffs\n")
	else:
		output = open("teams_statistics.csv", 'a')
	# Get the html's soup
	html = get_html(team_url)
	soup = BeautifulSoup(html)
	remote_word = re.compile("/teams/|/")
	team_id =remote_word.sub("",team_url)
	# Test if the team is already in the .csv file
	if team_is_on_csv(team_id,"teams_statistics.csv"):
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
			# Clean the season format
			if re.search("[0-9][0-9][0-9][0-9]-[0-9][0-9]",data[i].get_text()):
				text_to_write = re.search("[0-9][0-9][0-9][0-9]",data[i].get_text()).group()+","
			else:
				text_to_write = data[i].get_text()+','
			output.write(text_to_write.encode('utf-8'))
		output.write("\n")
	print 'team table has been scraped into team_statistics.csv'
	output.close()

def all_statistics_teams():
	teams = all_teams_links()
	# Going into the "Data" directory
	# Define your PATH
	PATH = "C:\\Users\\Simon\\Documents\\Project HowBA\\fedelmid\\Data"
	os.chdir(PATH)
	# Writing team_stats and team_basic_info in this directory
	for team_url in teams:
		print("Currently loading stats from "+team_url)
		load_statistics_team(team_url)
		# Systems sleeps 2 sec in order to avoid being blocked
		time.sleep(2)
		print("Currently loading basic info from "+team_url)
		load_team_basic_info(team_url)
		# Systems sleeps 2 sec in order to avoid being blocked
		time.sleep(2)
	print("loading of statistics ended")