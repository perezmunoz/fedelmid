# Provide the links for both players and teams

import re, urllib, time

##########################################################
# Get the links to the players' page
##########################################################

# Get player's first letter in name
# Return a list of the form ['a', 'b', ..., 'z']
def letters_players(html):
    needle = '<a href="/players/([a-z]+)/">[A-Z]+</a></td>'
    # Get the letters
    return re.findall(needle, html)


# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links(c, html): 
    needle = '[^p]><a href="(/players/[a-z]/.+)"'    # We use [a-z] for 'letter' because some players change names. In this case 'letter' might not be the same as c.
    m = re.findall(needle, html)    
    return m

# Get the links for all the players
# Return a list with results of the form /players/letter/name.html
def all_players_links():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players.html','r')
    html = f.read()
    alphabet = letters_players(html)
    res = []
    for c in alphabet:
        f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players_'+c+'.html','r')
        html = f.read()
        res+=players_links(c, html)
        # time.sleep(2)
        print c + ' players computed'
    return res

##########################################################
# Get the links to the teams' page
##########################################################

# Get the links for all the teams
# Return a list with results of the form /team/name/
def all_teams_links():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/teams.html','r')
    html = f.read()
    needle = 'href="(/teams/[A-Z]+/)"'
    res = re.findall(needle, html)
    return res

##########################################################
# Calculate the number of players to check the results
##########################################################

# Retrieve the number of players whose names start with the letter c 
# Return an integer
def number_players(c):  
    urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
    html = urlHandle.read()
    needle = '<h2 data-mobile-header="" style="">(.+)? Players</h2>'
    m = re.search(needle, html)
    return int(m.group(1))

# Calculate the number of all the players on basketball-reference
# Return an integer
def number_all_players():
    alphabet = letters_players()
    res=0
    for c in alphabet:
        res+=number_players(c)
        # time.sleep(2)
    return res


# print letters_players(html)

f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/benchmark/links_provider_regex.txt','w')
for i in range(100):
    beg =  time.time()
    all_players_links()
    f.write(str(time.time() - beg))
    print str(time.time() - beg)
    f.write(',')

# print all_teams_links() #0.1s
# timeit.timeit('all_players_links()',number=1000)
# timeit.timeit('all_teams_links()',number=1000)