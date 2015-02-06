# Provide the .csv files of player's basic statistics and salaries

from bs4 import BeautifulSoup
import urllib, string, time, csv, os

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
	# Dictionary's behavior when looping over it is like a LIFO
	for key in dict:
		# Table dict[key] is not empty and has a tbody (special case for Contract table)
		if dict[key] is not None and dict[key].tbody is not None:
			write_table(dict[key],key,player_id)
			print key+' table for player '+player_id+' has been scraped into '+key+'.csv'
		# Table dict[key] not empty but without tbody (special case for Contract table)
		elif dict[key] is not None and dict[key].tbody is None:
			write_table_wo_tbody(dict[key],key,player_id)
			print key+' table for player '+player_id+' has been scraped into salaries.csv'
		else:
			print 'Table '+key+' is missing for player '+player_id

# Writes the data contained in Totals or Per Game tables into totals.csv and per_game.csv files
def write_table(table,key,player_id):
	# Table is definitly not None here
	with open(key+'.csv', 'a') as output:
		# Get the body containing the data and store all tables's lines in a list
		body = table.tbody.find_all('tr')
		for row in body:
			# Get each value of the line and store it in a list
			data = row.find_all('td')
			# Writes the player_id at the beginning of the line
			output.write(player_id+',')
			# Range builts vector from 0: [0,1,..,29] for 30 elements
			for i in range(len(data)-1):
				# Special case #1 (unicode character such as a star). Usually in Season column
				if data[i].span is not None:
					# Removes the span tag
					data[i].span.extract()
					output.write(data[i].get_text().encode('utf-8')+',')
				# Normal case
				else:
					output.write(is_empty(data[i].get_text().encode('utf-8'))+',')
			# Writing the last element. Avoid having one more comma 
			output.write(write_last_element_of_data(data[-1]))

# Avoid error when a td tag contains a space
# Returns '' is the td tag is ' '
def is_empty(data):
	if data=='\xc2\xa0':
		return ''.encode('utf-8')
	else:
		return data

# Writes the data contained in the Contract tables into salaries.csv
# Contract table has not the same HTML structure than others (thead, tbody and tfoot missing)
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
		# Futures contracts, if any, are not written
		output.write((player_id+','+year+','+team+',NBA,'+salary).encode('utf-8')+'\n')

# Writes the last element of each line
# Avoid having an extra comma at the end of the line and consider the case didn't play during that Season
def write_last_element_of_data(e):
	# Special case #2 (Did not play this season)
	if e.get('colspan') is not None:
		return (','*(int(str(e.get('colspan')))-1)).encode('utf-8')+'\n'
	# Avoid unicode characters causing troubles
	elif e.span is not None:
		e.span.extract()
		return e.get_text().encode('utf-8')+'\n'
	# Normal case
	else:
		return e.get_text().encode('utf-8')+'\n'

from decimal import *
# Numbers displayed in progress computing
getcontext().prec = 3

# Main function computing all player's statistics and salaries
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
	# Get all player's links
	res = all_players_links()
	for player in res[]:
		time.sleep(2)
		get_statistics_player(player)
		print player+' done'
		print str(Decimal(res.index(player))/Decimal((len(res)-1))*Decimal(100))+' % computed\n'
	# Cleaning phase: resolution of bugs #4 and #5
	print 'Cleaning process starts'
	cleaning_csv('totals')
	cleaning_csv('per_game')
	cleaning_salaries('salaries')
	print 'Cleaning process ends'
	# Removing temporary files
	os.remove('totals.csv')
	os.remove('per_game.csv')
	os.remove('salaries.csv')

# Writes header to each .csv file
def write_header(file_name,header):
	with open(file_name, 'a') as output:
		output.write(header.encode('utf-8')+'\n')

# Cleans the Season'format. Ex: for 2013-14, we keep 2013
# Returns a new .csv file: file_name_final.csv
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

# Cleans the Season's format as do the cleaning_csv function and the Salary's format as well
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

# Bug to fix:
#1 [FIXED] tables which do not have tbody Tag...
#2 [FIXED] lines which have a span tag containing an unicode character
#3 [FIXED] Fusion contract and salaries tables
#4 [FIXED] Extract first year for season
#5 [FIXED] Replace '$' and ',' to '' in salaries
#6 [FIXED] Modify output contract table for player xxx has been scraped into ...
