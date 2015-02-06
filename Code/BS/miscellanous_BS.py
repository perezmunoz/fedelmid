# A few useful functions

from bs4 import BeautifulSoup
import urllib, time, csv, re

##########################################################
# Get the letters which are not empty, i.e. at least one player's name starts with these letters
##########################################################

# Return a list of the form ['a', 'b', ..., 'z']
def letters_players_BS():
    letters = []
    # Opening player's page and making the soup
    soup = url_to_soup('http://www.basketball-reference.com/players')
    # Get the letters
    for row in soup('td', {'class': 'align_center bold_text valign_bottom xx_large_text'}):
        letters.append(str(row.a.get('href').split('/')[2]))
    return letters


##########################################################
# Calculate the number of players to check the results
##########################################################

# Retrieve the number of players whose names start with the letter c
# Return an integer
def number_players_BS(c):  
    soup = url_to_soup('http://www.basketball-reference.com/players/'+c)
    number_string = soup.h2.get_text()
    number_re = re.search('[0-9]+', number_string)
    return int(number_re.group(0))

# Calculate the number of all the players on basketball-reference
# Return an integer
def number_all_players_BS():
    alphabet = letters_players_BS()
    res = 0
    for c in alphabet:
        res += number_players_BS(c)
        # System sleeps 2 seconds between each GET request
        # time.sleep(2)
    return res

##########################################################
# Get which player is active or not
##########################################################

# Write in a .csv file a table with PlayerID (letter+name) and active (True or False)
# This table is then joined with totals.csv, per_game.csv and salaries.csv in order to get all currently active players
def active_players_BS():
    with open('active_players.csv','w') as file_output:
        fieldnames = ['PlayerID', 'active']
        writer = csv.DictWriter(file_output, fieldnames = fieldnames)
        writer.writeheader()
        alphabet = letters_players_BS()
        for c in alphabet:
            soup = url_to_soup('http://www.basketball-reference.com/players/'+c)            
            for player in soup.tbody.find_all('tr'):
                    try:
                        name = str(player.td.strong.a.get('href')).split('/')[3].split('.')[0]               
                        writer.writerow({'PlayerID': c+name, 'active': 'True'})
                    except AttributeError:
                        name = str(player.td.a.get('href')).split('/')[3].split('.')[0]
                        writer.writerow({'PlayerID': c+name, 'active': 'False'})  
    return ''


##########################################################
# Make soup
##########################################################

def url_to_soup(url):
    html = urllib.urlopen(url).read()
    return BeautifulSoup(html)