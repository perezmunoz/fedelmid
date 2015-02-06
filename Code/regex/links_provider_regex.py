# Provide the links for both players and teams

import re, urllib, string

##########################################################
# Get the links to the players' page
##########################################################

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links_regex(c):
    needle = '[^p]><a href="(/players/./.+)"'    # We use a '.'' for 'letter' because some players change names. In this case 'letter' might not be the same as c.
    html = urllib.urlopen('http://www.basketball-reference.com/players/'+c).read()
    return re.findall(needle, html)

# Get the links for all the players
# Return a list with results of the form /players/letter/name.html
def all_players_links_regex():
    alphabet = letters_players_regex()
    res = []
    for c in alphabet:
        res += players_links_regex(c)
        time.sleep(2)
    return res

##########################################################
# Get the links to the teams' page
##########################################################

# Get the links for all the teams
# Return a list with results of the form /team/name/
def all_teams_links_regex():
    html = urllib.urlopen('http://www.basketball-reference.com/teams').read()
    needle = 'href="(/teams/[A-Z]+/)"'
    return re.findall(needle, html)