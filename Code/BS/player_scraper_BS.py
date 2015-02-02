# Provide the .csv files of player's profile and basic statistics

from bs4 import BeautifulSoup
import urllib
import string
import time

# Scrap profile's information

# declare URL to scrape from and store html in content variable
urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/c/cabocbr01.html')
html = urlHandle.read()

# process html using BeautifulSoup
soup = BeautifulSoup(content)

# get player name
playerName = soup.find('h1')
for n in playerName:
   name = n

# get info like position, shoots, height, weight, born, country, draft, NBA debut, experience
infoall = soup.find_all('p','padding_bottom_half')
for info1 in infoall:
   info = info1.text
   
def get_profile_player(link_player):

	# List containing the player's profile
	res = []

	# Letters of the players
	# execfile('scraping_links_players.py') prior to lunch this script
	alphabetical = get_letters_players()

	index = BeautifulSoup(urllib.urlopen('http://www.basketball-reference.com/players/'+link_player[0]+'/'+link_player).read())
	# class=padding_bottom_half is unique
	# The used of find_all returns a bs4.element.ResultSet element which cannot be accessed
	# find method returns a Tag object which can be accessed with common methods
	profile = index.find('p', {'class': 'padding_bottom_half'})

	# Retrieve all text data from profile (outside tags)
	# profile_str = profile.get_text()
	# Removing \xa0 and \u25aa characters (using unicode characters)
	# profile_str.replace(u'\xa0\u25aa\xa0',u' ').replace(u'\n',u'')

	# A way to chain these two previous lines
	profile_str = str((profile.get_text()).replace(u'\xa0\u25aa\xa0',u' ').replace(u'\n',u''))

	# profile_str.split('Position:','Shoots:','Height:','Weight:','Born:','High School:','College:','Draft:','NBA Debut:','Other Pages:')
	# re.split('[Position: Shoots: Height:]',profile_str)
	profile_split = re.split('(?:Position:|Shoots:|Height:|Weight:|Born:|High School:|College:|Draft:|NBA Debut:|Other Pages:)',profile_str)

	# Remove 1st element which is empty
	del profile_split[0]

	# Strip each element of the list. 
	res += map(str.strip,profile_split)
	# Player's profile:
	# [0] Position
	# [1] Shoots
	# [2] Heigh
	# [3] Weight
	# [4] Born (date and place)
	# [5] High School
	# [6] College
	# [7] Draft
	# [8] NBA Debut
	# [9] Others Pages
	return res

def get_all_profile_player():

	# Player's profile list
	profiles = [[]]

	for player in res[0]:
		profiles += get_profile_player(player)
		# Output to algorithm's steps
		print player

	return profiles

# Get all profile's characteristics in order to build player's profile
def get_all_characteristics():

	# Date regex
	date_regex = re.compile("[A-Za-z]*\s[0-9]*[,]{1}\s[0-9]*")

	# Characteristics'list
	properties = []

	# res[0] contains all url's players
	res = [[]]
	res = get_all_players()

	for player in res[0]:

		# Sleeps 1 seconde
		time.sleep(1)

		# Player's soup
		index = BeautifulSoup(urllib.urlopen('http://www.basketball-reference.com/players/'+player[0]+'/'+player).read())
		# Retrieving p tag containing relevant information
		profile = index.find('p', {'class': 'padding_bottom_half'})
		# Get all span tags containing characteristics
		span_tag = profile.find_all('span')

		# Testing whether it's already in properties list or not
		for char in span_tag:
			char_str = str(char.get_text())
			if date_regex.match(char_str) or char_str=='':
				print "Date or blank avoided"
				print char_str
			else:
				if char_str in properties:
					print "Characteristic already in properties list"
				else:
					properties.append(char_str)
	
	return properties

# Scrap player's basic statistics
# Return player's Totals, Per Game, Salaries and Contract tables as .csv files
# Remember: player's links are like /players/letter/name.html
def get_statistics_player(link_player):
	urlHandle = urllib.urlopen('http://www.basketball-reference.com'+link_player)
	html = urlHandle.read()
	soup = BeautifulSoup(html)
	# Dictionary to store tables
	dict = {}
	# Getting relevant tables into the dictionary dict
	dict['totals'] = soup.find('table', {'id': 'totals'})
	dict['per_game'] = soup.find('table', {'id': 'per_game'})
	dict['salaries'] = soup.find('table', {'id': 'salaries'})
	dict['contract'] = soup.find('table', {'id': 'contract'})
	for key in dict:
		with open(key+'.csv', 'a') as output:
			# Scrap lines from dict[key] table
			if dict[key] is not None:
				body = dict[key].tbody.find_all('tr')
				for row in body:
					data = row.find_all('td')
					for i in range(len(data)):
						output.write(str(data[i].get_text())+',')
					output.write(link_player+'\n')
					print key+' table has been scraped into '+key+'.csv'
			else:
				print 'Table '+key+' missing for player '+link_player




	# Get all tables
	tables = index.find_all('table')
	# Avoid computing 'Links' table which is useless
	for t in tables[0:len(tables)-1]:
			with open(str(t.get('id'))+'.txt', 'w') as output:
				# Writing header to the file
				# We take the last line in header (some tables have mutiple header lines)
				print str(t.get('id'))

				# Writing the header
				# Tables which don't have thead tag
				if t.thead is not None:
					header = t.thead.find_all('tr')[-1].find_all('th')
				else:
					# No thead tag means that 1st row in the tbody tag is the header
					header = t.find_all('tr')[0].find_all('th')

				for i in range(len(header)):
					# Last element should be erased when importing data
					output.write(str(header[i].get_text())+',')
				# Back to line
				# Add the player_id (equivalent to html link) at the end
				output.write('Player_id'+'\n')
				
				# Writing the data contained in tbody
				# Tables which don't heave tbody tag
				if t.body is not None:
					body = t.tbody.find_all('tr')
				else:
					body = t.find_all('tr')[1:]	

				# Writing data to the file
				for row in body:
					data = row.find_all('td')
					for j in range(len(data)):
						output.write(str(data[j].get_text())+',')
					output.write(link_player+'\n')


# Tables
# totals = index.find('table', {'id': 'totals'})
# per_game = index.find('table', {'id': 'per_game'})
# per_minute = index.find('table', {'id': 'per_minute'})
# per_poss = index.find('table', {'id': 'per_poss'})
# advanced = index.find('table', {'id': 'advanced'})
# shooting = index.find('table', {'id': 'shooting'})
# advanced_pbp = index.find('table', {'id': 'advanced_pbp'})
# playoffs_totals = index.find('table', {'id': 'playoffs_totals'})
# playoffs_per_game = index.find('table', {'id': 'playoffs_per_game'})
# playoffs_per_minute = index.find('table', {'id': 'playoffs_per_minute'})
# playoffs_per_poss = index.find('table', {'id': 'playoffs_per_poss'})
# playoffs_advanced = index.find('table', {'id': 'playoffs_advanced'})
# playoffs_shooting = index.find('table', {'id': 'playoffs_shooting'})
# playoffs_advanced_pbp = index.find('table', {'id': 'playoffs_advanced_pbp'})
# sim_thru = index.find('table', {'id': 'sim_thru'})
# sim_career = index.find('table', {'id': 'sim_career'})
# college = index.find('table', {'id': 'college'})
# salaries = index.find('table', {'id': 'salaries'})
# contract = index.find('table', {'id': 'contract'})


#		# Writing header to the file
#		header_totals = totals.thead.tr.find_all('th')
#		for i in range(len(header_totals)):
#			# Last element should be erased when importing data
#			output.write(str(header_totals[i].get_text())+',')
#		# Back to line
#		# I add the link to the data in order to find to whom belongs it
#		output.write('Player_id'+'\n')
		
#		# Writing header to the file
#		body_totals = totals.tbody.find_all('tr')
#		for row in body_totals:
#			data = row.find_all('td')
#			for j in range(len(data)):
#				output.write(str(data[j].get_text())+',')
#			output.write('smithis01'+'\n')
