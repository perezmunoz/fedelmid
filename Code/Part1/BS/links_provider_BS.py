# Provide the links for both players and teams

##########################################################
# Get the links of the players' page
##########################################################

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links_by_letter_BS(c): 
    soup = url_to_soup('http://www.basketball-reference.com/players/'+c)
    res = []
    for player in soup.tbody.find_all('tr'):
        res.append(str(player.td.a.get('href')))
    return res

# Get the links for all the players (total: 4288)
# Return a list with results of the form /players/letter/name.html
def all_players_links_BS():
    alphabet = letters_players_BS()
    res = []
    for letter in alphabet:
        res += players_links_by_letter_BS(letter)
        # System sleeps 2 seconds between each GET request
        # time.sleep(2)
        # Get feedback from computing
        print letter + ' players computed'
    return res

##########################################################
# Get the links of the team
##########################################################

# Get links for the teams
# Return a list with results of the form /teams/name/
def all_teams_links_BS():
    soup = url_to_soup('http://www.basketball-reference.com/teams')
    res = []
    # To get all the teams
    for team in soup.find_all('class':"full_table"):
        # Get only the current teams present in soup.tbody.find_all(class_="full_table")
        res.append(str(team.td.a.get('href')))
    return res