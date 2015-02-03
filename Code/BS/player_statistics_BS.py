# Provide the .csv files of player's basic statistics

from bs4 import BeautifulSoup
import urllib
import string
import time

# Scrap profile's information

# declare URL to scrape from and store html in content variable
#urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/c/cabocbr01.html')
#html = urlHandle.read()

# process html using BeautifulSoup
#soup = BeautifulSoup(content)

# get player name
#playerName = soup.find('h1')
#for n in playerName:
#   name = n

# get info like position, shoots, height, weight, born, country, draft, NBA debut, experience
#infoall = soup.find_all('p','padding_bottom_half')
#for info1 in infoall:
#   info = info1.text
   
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

# ===============================================================================
# START New realease: scraping data for each player
# ===============================================================================

# Scrap player's basic statistics
# Return player's Totals, Per Game, Salaries and Contract tables as .csv files
# Reminder: player's links are like /players/letter/name.html
def get_statistics_player(link_player):
	urlHandle = urllib.urlopen('http://www.basketball-reference.com'+link_player)
	html = urlHandle.read()
	soup = BeautifulSoup(html)
	# Construct the id of the player: letter+name
	# For /players/a/abdulal01.html, the player_id is aabdulal01, e.g letter+name
	player_id = str(link_player.split('/')[2]+link_player.split('/')[3].split('.')[0])
	# Dictionary to store tables
	dict = {}
	# Getting relevant tables into the dictionary dict
	dict['totals'] = soup.find('table', {'id': 'totals'})
	dict['per_game'] = soup.find('table', {'id': 'per_game'})
	dict['salaries'] = soup.find('table', {'id': 'salaries'})
	dict['contract'] = soup.find('table', {'id': 'contract'})
	# dictionary's behavior when looping over it is like a LIFO
	for key in dict:
		# Table dict[key] has a tbody
		if dict[key] is not None and dict[key].tbody is not None:
			write_table(dict[key],key,player_id)
			print key+' table for player '+player_id+' has been scraped into '+key+'.csv'
		# Table dict[key] not empty but without tbody
		elif dict[key] is not None and dict[key].tbody is None:
			write_table_wo_tbody(dict[key],key,player_id)
			print key+' table for player '+player_id+' has been scraped into '+key+'.csv'
		else:
			print 'Table '+key+' is missing for player '+player_id

def write_table(table,key,player_id):
	# Table is definitly not None here
	with open(key+'.csv', 'a') as output:
		# Get the body containing the data
		body = table.tbody.find_all('tr')
		for row in body:
			data = row.find_all('td')
			output.write(player_id+',')
			# Range builts vector from 0: [0,1,..,29] for 30 elements
			for i in range(len(data)-1):
				# Special case #1 (unicode character)
				if data[i].span is not None:
					# Removes the span tag
					data[i].span.extract()
					output.write(str(data[i].get_text())+',')
				# Normal case
				else:
					output.write(str(data[i].get_text())+',')
			# Manipulating the last element
			output.write(write_last_element_of_data(data[-1]))

def write_table_wo_tbody(table,key,player_id):
	# Table is definitly not None here
	with open(key+'.csv', 'a') as output:
		body = table.find_all('tr')
		# In this case body[0] contains th tags and body[1] contains td
		# body[0][0] returns 'Team', body[0][1] returns 'Current year', body[0][2] returns 'Next year', ...
		# body[1][0] returns 'Team's name, body[1][1] returns 'Current year salary', ...
		year = str(body[0].find_all('th')[1].get_text())
		team = str(body[1].find_all('td')[0].get_text())
		salary = str(body[1].find_all('td')[1].get_text())
		# Building the current contract
		output.write(str(player_id+','+year+','+team+',NBA,'+salary)+'\n')

def write_last_element_of_data(e):
	# Special case #2 (Did not play this season)
	if e.get('colspan') is not None:
		return str(','*(int(str(e.get('colspan')))-1))+'\n'
	elif e.span is not None:
		e.span.extract()
		return str(e.get_text())+'\n'
	else:
		return str(e.get_text())+'\n'

from decimal import *
# Numbers displayed
getcontext().prec = 3

res3 = ['/players/r/roberte01.html', '/players/r/roberan01.html', '/players/r/roberbi01.html', '/players/r/roberbr01.html', '/players/r/roberfr01.html', '/players/r/roberjo01.html', '/players/r/roberla01.html', '/players/r/roberma01.html', '/players/r/roberst01.html', '/players/r/roberal01.html', '/players/r/roberos01.html', '/players/r/roberry01.html', '/players/r/roberto01.html', '/players/r/robeyri01.html', '/players/r/robinbe01.html', '/players/r/robinch01.html', '/players/r/robincl01.html', '/players/r/robincl02.html', '/players/r/robinda01.html', '/players/r/robined01.html', '/players/r/robinfl01.html', '/players/r/robingl01.html', '/players/r/robingl02.html', '/players/r/robinja01.html', '/players/r/robinja03.html', '/players/r/robinja02.html', '/players/r/robinla01.html', '/players/r/robinna01.html', '/players/r/robinol01.html', '/players/r/robinro01.html', '/players/r/robinru01.html', '/players/r/robinsa01.html', '/players/r/robinth01.html', '/players/r/robintr01.html', '/players/r/robinwa01.html', '/players/r/robinwi01.html', '/players/r/robinbi01.html', '/players/r/robisda01.html', '/players/r/rochare01.html', '/players/r/rochejo01.html', '/players/r/rockge01.html', '/players/r/rockeja01.html', '/players/r/rodgegu01.html', '/players/r/rodmade01.html', '/players/r/rodrise01.html', '/players/r/roelo01.html', '/players/r/rogerca01.html', '/players/r/rogerha01.html', '/players/r/rogerjo01.html', '/players/r/rogerma01.html', '/players/r/rogerro01.html', '/players/r/rogerro02.html', '/players/r/rogerwi01.html', '/players/r/rogesal01.html', '/players/r/rohloke01.html', '/players/r/rollike01.html', '/players/r/rolliph01.html', '/players/r/rollitr01.html', '/players/r/romarlo01.html', '/players/r/rondora01.html', '/players/r/rookje01.html', '/players/r/rooksse01.html', '/players/r/rosede01.html', '/players/r/roseja01.html', '/players/r/rosema01.html', '/players/r/rosero01.html', '/players/r/rosenpe01.html', '/players/r/rosenle01.html', '/players/r/rosenha01.html', '/players/r/rosendi01.html', '/players/r/rossqu01.html', '/players/r/rosste01.html', '/players/r/rothdo01.html', '/players/r/rothsc01.html', '/players/r/rotheir01.html', '/players/r/rottnmi01.html', '/players/r/roundda01.html', '/players/r/rouxgi01.html', '/players/r/rowanro01.html', '/players/r/rowecu01.html', '/players/r/rowinji01.html', '/players/r/rowlade01.html', '/players/r/rowsobr01.html', '/players/r/roybr01.html', '/players/r/royaldo01.html', '/players/r/royalre01.html', '/players/r/royerbo01.html', '/players/r/roziecl01.html', '/players/r/rubiori01.html', '/players/r/ruckegu01.html', '/players/r/ruddde01.html', '/players/r/ruddjo01.html', '/players/r/rudezda01.html', '/players/r/rudomjo01.html', '/players/r/ruffimi01.html', '/players/r/ruffitr01.html', '/players/r/ruffnpa01.html', '/players/r/ruklijo01.html', '/players/r/rulanje01.html', '/players/r/rulebo01.html']

for player in res3:
	get_statistics_player(player)
	print player+' done'
	print str(Decimal(res3.index(player))/Decimal((len(res3)-1))*Decimal(100))+' %'

# Bug to fix:
#1 [FIXED] tables which do not have tbody Tag...
#2 [FIXED] lines which have a span tag containing an unicode character
#3 Fusion contract and salaries tables
#4 Extract first year for season 
#5 replace ',' to '.' in salaries

# [PASSED] Test with 10 players
# res = ['/players/a/abdelal01.html', '/players/a/abdulza01.html', '/players/a/abdulka01.html', '/players/a/abdulma01.html', '/players/a/abdulma02.html', '/players/a/abdulta01.html', '/players/a/abdursh01.html', '/players/a/abernto01.html', '/players/a/ablefo01.html', '/players/a/abramjo01.html']

# Some tables hasn't tbody Tag (fixing bug). Exception for /players/p/pendeje02.html
# Hypothesis: tables w/o tbody are contracts
# [PASSED] Test with about 30 players
# res2 =['/players/a/aventan01.html', '/players/a/averibi01.html', '/players/a/averywi01.html', '/players/a/awtrede01.html', '/players/a/ayongu01.html', '/players/p/pendeje02.html', '/players/a/azubuke01.html', '/players/b/babbch01.html', '/players/b/babbilu01.html', '/players/b/babicmi01.html', '/players/b/bachjo01.html', '/players/b/baconhe01.html', '/players/b/baechji01.html', '/players/b/bagarda01.html', '/players/b/baglejo01.html']

# [PASSED] Test with 100 players
# res3 = ['/players/r/roberte01.html', '/players/r/roberan01.html', '/players/r/roberbi01.html', '/players/r/roberbr01.html', '/players/r/roberfr01.html', '/players/r/roberjo01.html', '/players/r/roberla01.html', '/players/r/roberma01.html', '/players/r/roberst01.html', '/players/r/roberal01.html', '/players/r/roberos01.html', '/players/r/roberry01.html', '/players/r/roberto01.html', '/players/r/robeyri01.html', '/players/r/robinbe01.html', '/players/r/robinch01.html', '/players/r/robincl01.html', '/players/r/robincl02.html', '/players/r/robinda01.html', '/players/r/robined01.html', '/players/r/robinfl01.html', '/players/r/robingl01.html', '/players/r/robingl02.html', '/players/r/robinja01.html', '/players/r/robinja03.html', '/players/r/robinja02.html', '/players/r/robinla01.html', '/players/r/robinna01.html', '/players/r/robinol01.html', '/players/r/robinro01.html', '/players/r/robinru01.html', '/players/r/robinsa01.html', '/players/r/robinth01.html', '/players/r/robintr01.html', '/players/r/robinwa01.html', '/players/r/robinwi01.html', '/players/r/robinbi01.html', '/players/r/robisda01.html', '/players/r/rochare01.html', '/players/r/rochejo01.html', '/players/r/rockge01.html', '/players/r/rockeja01.html', '/players/r/rodgegu01.html', '/players/r/rodmade01.html', '/players/r/rodrise01.html', '/players/r/roelo01.html', '/players/r/rogerca01.html', '/players/r/rogerha01.html', '/players/r/rogerjo01.html', '/players/r/rogerma01.html', '/players/r/rogerro01.html', '/players/r/rogerro02.html', '/players/r/rogerwi01.html', '/players/r/rogesal01.html', '/players/r/rohloke01.html', '/players/r/rollike01.html', '/players/r/rolliph01.html', '/players/r/rollitr01.html', '/players/r/romarlo01.html', '/players/r/rondora01.html', '/players/r/rookje01.html', '/players/r/rooksse01.html', '/players/r/rosede01.html', '/players/r/roseja01.html', '/players/r/rosema01.html', '/players/r/rosero01.html', '/players/r/rosenpe01.html', '/players/r/rosenle01.html', '/players/r/rosenha01.html', '/players/r/rosendi01.html', '/players/r/rossqu01.html', '/players/r/rosste01.html', '/players/r/rothdo01.html', '/players/r/rothsc01.html', '/players/r/rotheir01.html', '/players/r/rottnmi01.html', '/players/r/roundda01.html', '/players/r/rouxgi01.html', '/players/r/rowanro01.html', '/players/r/rowecu01.html', '/players/r/rowinji01.html', '/players/r/rowlade01.html', '/players/r/rowsobr01.html', '/players/r/roybr01.html', '/players/r/royaldo01.html', '/players/r/royalre01.html', '/players/r/royerbo01.html', '/players/r/roziecl01.html', '/players/r/rubiori01.html', '/players/r/ruckegu01.html', '/players/r/ruddde01.html', '/players/r/ruddjo01.html', '/players/r/rudezda01.html', '/players/r/rudomjo01.html', '/players/r/ruffimi01.html', '/players/r/ruffitr01.html', '/players/r/ruffnpa01.html', '/players/r/ruklijo01.html', '/players/r/rulanje01.html', '/players/r/rulebo01.html']

# ALL TABLES
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