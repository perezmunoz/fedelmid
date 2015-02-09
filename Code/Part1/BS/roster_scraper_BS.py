#Get all the roster tables from all the teams

from bs4 import BeautifulSoup
import re, urllib, string, os, csv, time

# Open a team's url and scrap all the pages where we can can find the season roster of the team
def roster_links_one_team(team_url):
	html = urllib.urlopen("http://basketball-reference.com"+team_url).read()
	soup = BeautifulSoup(html)
	tag = soup.find("a",href=team_url).parent.find("ul")
	res = []
	for child in tag.contents:
		try:
			res.append(str(child.a["href"]))
		except:
			pass
	return res

# Check if a team has already been added to the .csv file for a specific season
def is_already_in_csv(team_id, season_id, path):
	with open(path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			if row[0] == team_id and row[1] == season_id:
				return True
		return False

# Open a roster's page and scrap the roster, save it in roster_statistics.csv
# We use only one csv file for all the teams and for all seasons. So we add these two info in the table
# /!\/!\/!\ The id of a season is the civil year in which the season began. Eg the id of 2014-15 is 2014
def write_one_roster(roster_url):
	file_name = "roster_statistics.csv"

	# Define header
	header = ["Team_id","Season","No","Player","Pos","Experience"]

	# Test if the file already exists, if not, it creates it
	if not os.path.isfile(file_name):
		output = open(file_name,'w')
		output.write("Team_id,Season,No,Player,Pos,Experience\n")
	else: 
		output = open(file_name, 'a')

	# Get the id of the team
	team_id = re.compile("/teams/|/[0-9][0-9][0-9][0-9].html").sub("",roster_url)

	# Get the id of the season
	season_id = str(int(re.compile("/teams/[a-zA-Z]*/|.html").sub("",roster_url))-1)

	# Check if the info are already in the csv
	if is_already_in_csv(team_id,season_id,file_name):
		print('table of team ' + team_id + ' was already in csv for season ' + season_id)
		return ""

	# Open the page where the roster table is
	html = urllib.urlopen("http://basketball-reference.com"+roster_url).read()
	soup = BeautifulSoup(html)



	# Getting roster table
	table = soup.find('table', {'id': 'roster'})
	# Scrap lines from the table
	body = table.tbody.find_all('tr')
	for row in body:
		output.write(team_id+","+season_id+",")
		count = 1
		data = row.find_all('td')
		nine_columns = (len(data) == 9)
		for i in range(len(data)):
			text_to_write = ""
			# Writing number
			if i == 0:
				text_to_write = data[i].get_text()+','
			# Getting player id
			elif i == 1:
				link = data[i].a['href']
				text_to_write = re.compile('/players/./|.html').sub('',link)+','
			# Getting player position
			elif i == 2:
				text_to_write = data[i].get_text()+','
			elif i == 6 and (not nine_columns):
				text_to_write = data[i].get_text()+','
				output.write(text_to_write.encode('utf-8'))
				break # We only keep the three first columns and the experience column
			elif i == 7 and nine_columns:
				text_to_write = data[i].get_text()+','
				output.write(text_to_write.encode('utf-8'))
				break # We only keep the three first columns and the experience column

			output.write(text_to_write.encode('utf-8'))
			count += 1

		output.write("\n")
	output.close()
	print 'roster table of team ' + team_id + ' and season ' + season_id + ' has been scraped into roster_statistics.csv'

def write_all_roster_from_one_team(team_link):
	# Download all rosters
	tab = roster_links_one_team(team_link)
	for link in tab:
		write_one_roster(link)

# def all_teams_links_BS():
# 	# Open the page where the roster table is
# 	html = urllib.urlopen('http://www.basketball-reference.com/teams').read()
# 	soup = BeautifulSoup(html)
# 	res = []
#     # To get all the teams
# 	for team in soup.find_all(class_="full_table"):
# 		# Get only the current teams present in soup.tbody.find_all(class_="full_table")
# 		res.append(str(team.td.a.get('href')))
# 	return res

def clean_csv():
	with open('roster_statistics.csv', 'b') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			if re.search("-",row[3]):
				row[3] = re.compile("-[0-9]*").sub("",re.search("-",row[3]))

def write_all_rosters():
	# Trick to ba able to stop the code and re-run it without scrapping teams that have already been scrapped
	boolean = False
	# Download all team links
	team_links = all_teams_links_BS()

	file_name = "teams.txt"
	if not os.path.isfile(file_name):
		output = open(file_name,'w')
		output.close()

	# Scrap all teams rosters
	for link in team_links:
		# Look if the team has already been scrapped
		with open(file_name, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in reader:
				# If so, it jumps it
				if row[0] == link:
					boolean = True
					break
		if boolean:
			print("jump")
			boolean = False
			continue

		output = open(file_name,"a")
		# If not, it scraps it and then marked it as scrapped
		write_all_roster_from_one_team(link)
		output.write(link+'\n')
		output.close()
	clean_csv()
	print("scrapping of rosters ended")

write_all_rosters()