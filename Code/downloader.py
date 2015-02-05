import urllib, re

# Get player's first letter in name
# Return a list of the form ['a', 'b', ..., 'z']
def letters_players():
    needle = '<a href="/players/([a-z]+)/">[A-Z]+</a></td>'
    # Opening player's page
    html = urllib.urlopen('http://www.basketball-reference.com/players/').read()
    # Get the letters
    return re.findall(needle, html)

def dl_players():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players.html','w+')
    html = urllib.urlopen('http://www.basketball-reference.com/players/').read()
    f.write(html)
    for c in letters_players():
        f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/players_'+c+'.html','w+')
        html = urllib.urlopen('http://www.basketball-reference.com/players/'+c+'/').read()
        f.write(html)

def dl_teams():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Data/pages/teams.html','w+')
    html = urllib.urlopen('http://www.basketball-reference.com/teams/').read()
    f.write(html)

dl_teams()

