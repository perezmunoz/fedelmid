# A few useful functions

import urllib, time, csv, re

##########################################################
# Get the letters which are not empty, i.e. at least one player's name starts with these letters
##########################################################

# Return a list of the form ['a', 'b', ..., 'z']
def letters_players_regex():
    needle = '<a href="/players/([a-z]+)/">[A-Z]+</a></td>'
    # Opening player's page
    html = urllib.urlopen('http://www.basketball-reference.com/players/').read()
    # Get the letters
    return re.findall(needle, html)

##########################################################
# Calculate the number of players to check the results
##########################################################

# Retrieve the number of players whose names start with the letter c 
# Return an integer
def number_players_regex(c):
    html = urllib.urlopen('http://www.basketball-reference.com/players/'+c).read()
    needle = '<h2 data-mobile-header="" style="">(.+) Players</h2>'
    m = re.search(needle, html)
    return int(m.group(1))

# Calculate the number of all the players on basketball-reference
# Return an integer
def number_all_players_regex():
    alphabet = letters_players_regex()
    res = 0
    for c in alphabet:
        res += number_players_regex(c)
        time.sleep(2)
    return res