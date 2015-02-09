import urllib, re

# Get player's first letter in name
# Return a list of the form ['a', 'b', ..., 'z']
def letters_players():
    needle = '<a href="/players/([a-z]+)/">[A-Z]+</a></td>'
    # Opening player's page
    html = urllib.urlopen('http://www.basketball-reference.com/players/').read()
    # Get the letters
    return re.findall(needle, html)

# Download the players's html pages
def dl_players():
    output_file = open('./pages/players.html','w+')
    html = urllib.urlopen('http://www.basketball-reference.com/players/').read()
    output_file.write(html)
    for c in letters_players():
        output_file = open('./pages/players_'+c+'.html','w+')
        html = urllib.urlopen('http://www.basketball-reference.com/players/'+c+'/').read()
        output_file.write(html)

# Download the teams's html pages
def dl_teams():
    output_file = open('./pages/teams.html','w+')
    html = urllib.urlopen('http://www.basketball-reference.com/teams/').read()
    output_file.write(html)