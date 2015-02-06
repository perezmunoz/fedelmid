# Provide the links for both players and teams

from bs4 import BeautifulSoup
import urllib, time, csv

##########################################################
# Get the links to the players' page
##########################################################


# Get player's first letter in name
# Return a list of the form ['a', 'b', ..., 'z']
def letters_players(html):
    soup = BeautifulSoup(html)
    letters = []
    # Get the letters
    for row in soup('td', {'class': 'align_center bold_text valign_bottom xx_large_text'}):
        letters.append(str(row.a.get('href').split('/')[2]))
    return letters

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links_by_letter(c, html): 
    res = []
    soup = BeautifulSoup(html)
    for player in soup.tbody.find_all('tr'):
        res.append(str(player.td.a.get('href')))
        return res

# Get the links for all the players (total: 4288)
    # Return a list with results of the form /players/letter/name.html
def all_players_links():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players.html','r')
    html = f.read()
    alphabet = letters_players(html)
    res = []
    for c in alphabet:
        f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players_'+c+'.html','r')
        html = f.read()
        res += players_links_by_letter(c, html)
        # System sleeps 2 seconds between each GET request
        # time.sleep(2)
        # Get feedback from computing
        print c + ' players computed'
    return res

def active_players():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players.html','r')
    html = f.read()
    alphabet = letters_players(html)
    with open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/active_players.csv','w') as csvfile:
        fieldnames = ['playerID', 'active']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for c in alphabet:
            f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players_'+c+'.html','r')
            html = f.read()
            soup = BeautifulSoup(html)            
            for player in soup.tbody.find_all('tr'):
                    try:
                        name = str(player.td.strong.a.get('href')).split('/')[3].split('.')[0]               
                        writer.writerow({'playerID': c+name, 'active': 'True'})
                    except AttributeError:
                        name = str(player.td.a.get('href')).split('/')[3].split('.')[0]
                        writer.writerow({'playerID': c+name, 'active': 'False'})  
    return ''


##########################################################
# Get the links of the team
##########################################################

# Get links for the teams
# Return a list with results of the form /teams/name/
def all_teams_links():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/teams.html','r')
    html = f.read()
    soup = BeautifulSoup(html)
    res = []
    # To get all the teams
    for team in soup.find_all(class_="full_table"):
        # Get only the current teams present in soup.tbody.find_all(class_="full_table")
        res.append(str(team.td.a.get('href')))
    return res

##########################################################
# Calculate the number of players to check the results
##########################################################

# re package is only used in number_players and number_all_players
import re

# Retrieve the number of players whose names start with the letter c
# Return an integer
def number_players(c):  
    urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
    html = urlHandle.read()
    soup = BeautifulSoup(html)
    number_string = soup.h2.get_text()
    number_re = re.search('[0-9]+', number_string)
    return int(number_re.group(0))

# Calculate the number of all the players on basketball-reference
# Return an integer
def number_all_players():
    alphabet = letters_players()
    res = 0
    for c in alphabet:
        res += number_players(c)
        # System sleeps 2 seconds between each GET request
        # time.sleep(2)
    return res

# f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/benchmark/links_provider_BS.txt','w')
# for i in range(100):
#     beg =  time.time()
#     all_players_links()
#     f.write(str(time.time() - beg))
#     print str(time.time() - beg)
#     f.write(',')


print active_players()