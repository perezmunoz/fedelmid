# Provide the .csv file of team's statistics

from bs4 import BeautifulSoup
import re, urllib, string, os, csv, time

playoff_url = "http://www.basketball-reference.com/playoffs/"

# This function scrap the table from the above url
# Playoff information can be useful to explain highest salaries
def scrap_playoff():
	file_name = 'playoff_statistics.csv'
	# Test if the file already exists, if not, it creates it and open it
	output = open(file_name, 'w')
	output.write("Year,Lg,Champion,Runner-Up,Finals_MPV,Top_Performer_Points,Top_Performer_Rebounds,Top_Performer_Assists,Top_Performer_Win_Shares\n")
	# Get the html's soup
	html = urllib.urlopen(playoff_url).read()
	soup = BeautifulSoup(html)

	# Getting relevant table
	table = soup.find('table', {'class': 'stats_table'})
	# Scrap lines from table
	body = table.tbody.find_all('tr')
	for row in body[1:len(body)]:  # We don't want season 2015
		count = 1
		data = row.find_all('td')
		for i in range(len(data)):
			# We have to get the id of the teams, we can find it in a hypertext link
			if count == 3 or count == 4:
				try:
					link = data[i].a['href']
					text_to_write = re.compile('/teams/|/[0-9][0-9][0-9][0-9].html').sub('',link)+','
				except:
					text_to_write = ','
			# We don't keep the info about the number of points, rebounds, assists and win shares of each top performer
			# But we have to get their id from the href attribute
			elif count > 4:
				try:
					link = data[i].a['href']
					text_to_write = re.compile('/players/./|.html').sub('',link)+','
				except:
					text_to_write = ','
			else:
				text_to_write = data[i].get_text()+','
			output.write(text_to_write.encode('utf-8'))
			count += 1
		output.write("\n")
	print 'playoff table has been scraped into playoff_statistics.csv'
	output.close()