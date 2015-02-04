# Provide the .csv files of player's basic statistics

from bs4 import BeautifulSoup
import urllib
import string
import time
import csv
import os

# Scrap player's basic statistics
# Return player's Totals, Per Game, Salaries and Contract tables as .csv files
# Reminder: player's links are like /players/letter/name.html
def get_statistics_player(link_player):
	urlHandle = urllib.urlopen('http://www.basketball-reference.com'+link_player)
	html = urlHandle.read()
	soup = BeautifulSoup(html)
	# Construct the id of the player: letter+name
	# For /players/a/abdulal01.html, the player_id is aabdulal01, e.g letter+name
	player_id = (link_player.split('/')[2]+link_player.split('/')[3].split('.')[0]).encode('utf-8')
	# Dictionary to store tables
	dict = {}
	# Getting relevant tables into the dictionary dict
	dict['totals'] = soup.find('table', {'id': 'totals'})
	dict['per_game'] = soup.find('table', {'id': 'per_game'})
	dict['contract'] = soup.find('table', {'id': 'contract'})
	dict['salaries'] = soup.find('table', {'id': 'salaries'})
	# dictionary's behavior when looping over it is like a LIFO
	for key in dict:
		# Table dict[key] has a tbody
		if dict[key] is not None and dict[key].tbody is not None:
			write_table(dict[key],key,player_id)
			print key+' table for player '+player_id+' has been scraped into '+key+'.csv'
		# Table dict[key] not empty but without tbody (Ex: Contract table)
		elif dict[key] is not None and dict[key].tbody is None:
			write_table_wo_tbody(dict[key],key,player_id)
			print key+' table for player '+player_id+' has been scraped into salaries.csv'
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
					output.write(data[i].get_text().encode('utf-8')+',')
				# Normal case
				else:
					# print data[i].get_text().encode('utf-8').__class__
					output.write(is_empty(data[i].get_text().encode('utf-8'))+',')
			# Manipulating the last element
			output.write(write_last_element_of_data(data[-1]))

# Test if an element of the table is empty
def is_empty(data):
	if data=='\xc2\xa0':
		return ''.encode('utf-8')
	else:
		return data

def write_table_wo_tbody(table,key,player_id):
	# Table is definitly not None here but has no tbody tag
	with open('salaries.csv', 'a') as output:
		body = table.find_all('tr')
		# In this case body[0] contains th tags and body[1] contains td
		# body[0][0] returns 'Team', body[0][1] returns 'Current year', body[0][2] returns 'Next year', ...
		# body[1][0] returns 'Team's name, body[1][1] returns 'Current year salary', ...
		year = body[0].find_all('th')[1].get_text().encode('utf-8')
		team = body[1].find_all('td')[0].get_text().encode('utf-8')
		salary = body[1].find_all('td')[1].get_text().encode('utf-8')
		# Building the current contract
		output.write((player_id+','+year+','+team+',NBA,'+salary).encode('utf-8')+'\n')

def write_last_element_of_data(e):
	# Special case #2 (Did not play this season)
	if e.get('colspan') is not None:
		return (','*(int(str(e.get('colspan')))-1)).encode('utf-8')+'\n'
	elif e.span is not None:
		e.span.extract()
		return e.get_text().encode('utf-8')+'\n'
	else:
		return e.get_text().encode('utf-8')+'\n'

from decimal import *
# Numbers displayed
getcontext().prec = 3

def all_statistics_players():
	# Total of attributes: 31
	totals_header = 'PlayerID,Season,Age,Tm,Lg,Pos,G,GS,MP,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,eFG%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS'
	# Total of attributes: 30 (eFG% removed in per_game table)
	per_game_header = 'PlayerID,Season,Age,Tm,Lg,Pos,G,GS,MP,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS'
	salaries_header = 'PlayerID,Season,Team,Lg,Salary'
	# Write header to totals.csv, per_game.csv and salaries.csv
	write_header('totals.csv',totals_header)
	write_header('per_game.csv',per_game_header)
	write_header('salaries.csv',salaries_header)
	# Test with res2
	#res =['/players/a/aventan01.html', '/players/a/averibi01.html', '/players/a/averywi01.html', '/players/a/awtrede01.html', '/players/a/ayongu01.html', '/players/p/pendeje02.html', '/players/a/azubuke01.html', '/players/b/babbch01.html', '/players/b/babbilu01.html', '/players/b/babicmi01.html', '/players/b/bachjo01.html', '/players/b/baconhe01.html', '/players/b/baechji01.html', '/players/b/bagarda01.html', '/players/b/baglejo01.html']
	res = all_players_links()
	for player in res[4000:4050]:
		time.sleep(2)
		get_statistics_player(player)
		print player+' done'
		print str(Decimal(res.index(player))/Decimal((len(res)-1))*Decimal(100))+' % computed'
	# End of test
	# Cleaning data: resolution of bugs #4 and #5
	print 'Cleaning process start'
	cleaning_csv('totals')
	cleaning_csv('per_game')
	cleaning_salaries('salaries')
	print 'Cleaning process ends'

	# Removing temporary files
	os.remove('totals.csv')
	os.remove('per_game.csv')
	os.remove('salaries.csv')

def write_header(file_name,header):
	with open(file_name, 'a') as output:
		output.write(header.encode('utf-8')+'\n')

def cleaning_csv(file_name):
	with open(file_name+'.csv', 'rb') as file_input:
		with open(file_name+'_final.csv', 'wb') as file_output:
			reader_data = csv.reader(file_input, delimiter = ',')
			writer_data = csv.writer(file_output)
			# Write the header to file_output by taking the first line in file_input
			writer_data.writerow(reader_data.next())
			# e is a row of the csv file in input and represented in a list format
			for row in reader_data:
				# Getting year season's start year
				row[1] = row[1][:4]
				# Writing the corrected line
				writer_data.writerow(row)

def cleaning_salaries(file_name):
	with open(file_name+'.csv', 'rb') as file_input:
		with open(file_name+'_final.csv', 'wb') as file_output:
			reader_data = csv.reader(file_input, delimiter = ',')
			writer_data = csv.writer(file_output)
			# Write the header to file_output by taking the first line in file_input
			writer_data.writerow(reader_data.next())
			# e is a row of the csv file in input and represented in a list format
			for row in reader_data:
				# Getting year season's start year
				row[1] = row[1][:4]
				# Changing format of the salary from $1,500,000 to 1500000
				row[4] = (''.join(row[4:])).replace('$','')
				del row[5:]
				# Writing the corrected line
				writer_data.writerow(row)

# all_statistics_players()

# An element of a data is of the forme:
# {'Lg': 'NBA', 'FT': '2', 'PlayerID': 'bbaglejo01', '3P': '0', 'TOV': '0', '2PA': '2', 'Tm': 'ATL', 'FG': '0', '3PA': '0', 'DRB': '1', '2P': '0', 'AST': '3', 'Season': '1993-94', 'FT%': '1.000', 'PF': '2', 'PTS': '2', 'FGA': '2', 'GS': '0', 'G': '3', 'STL': '0', 'Age': '33', 'TRB': '1', 'FTA': '2', 'eFG%': '.000', 'BLK': '0', 'FG%': '.000', 'Pos': 'PG', '2P%': '.000', 'MP': '13', 'ORB': '0', '3P%': ''}
# Dictionary with keys equals to first line

# Test
# res2 =['/players/a/aventan01.html', '/players/a/averibi01.html', '/players/a/averywi01.html', '/players/a/awtrede01.html', '/players/a/ayongu01.html', '/players/p/pendeje02.html', '/players/a/azubuke01.html', '/players/b/babbch01.html', '/players/b/babbilu01.html', '/players/b/babicmi01.html', '/players/b/bachjo01.html', '/players/b/baconhe01.html', '/players/b/baechji01.html', '/players/b/bagarda01.html', '/players/b/baglejo01.html']

#for player in res2:
#	get_statistics_player(player)
#	print player+' done'
#	print str(Decimal(res2.index(player))/Decimal((len(res2)-1))*Decimal(100))+' %'

# Bug to fix:
#1 [FIXED] tables which do not have tbody Tag...
#2 [FIXED] lines which have a span tag containing an unicode character
#3 [FIXED] Fusion contract and salaries tables
#4 [FIXED] Extract first year for season
#5 [FIXED] Replace '$' and ',' to '' in salaries
#6 [FIXED] Modify output contract table for player xxx has been scraped into ...

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