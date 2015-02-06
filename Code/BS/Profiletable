# to scrap players infos using BS4
# written using Python 2.7

import urllib, string, time, csv
from random import randint
from bs4 import BeautifulSoup

month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

##########################################################
# Get the links to the players' page
##########################################################

# Get player's first letter in name
# Return a list of the form ['a', 'b', ..., 'z']
def letters_players():
        letters = []
        # Opening player's page
        urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/')
        html = urlHandle.read()
        soup = BeautifulSoup(html)
        # Get the letters
        for row in soup('td', {'class': 'align_center bold_text valign_bottom xx_large_text'}):
                letters.append(str(row.a.get('href').split('/')[2]))
        return letters

# Get the links for the players whose names start with the letter that is passed
# Return a list with results of the form /players/letter/name.html
def players_links_by_letter(c):	
	urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/'+c)
	html = urlHandle.read()
	res = []
	soup = BeautifulSoup(html)
	for player in soup.tbody.find_all('tr'):
		res.append(str(player.td.a.get('href')))
     	return res

# Get the links for all the players (total: 4288)
# Return a list with results of the form /players/letter/name.html
def all_players_links():
	alphabet = letters_players()
	res = []
	for letter in alphabet:
		res += players_links_by_letter(letter)
		# System sleeps 2 seconds between each GET request
		time.sleep(2)
		# Get feedback from computing
		print letter + ' players computed'
	return res

# store the list of all players in alllinks
alllinks = all_players_links()


# open a csv file to write into
tofile = open('player_profile.csv','w')

# traverse list and build url to get individual player link
for link in alllinks:
    thisURL = 'http://www.basketball-reference.com' + link
    content = urllib.urlopen(thisURL).read()

    # store content in soup object
    soup = BeautifulSoup(content)
    
    # get playerID
    playerID = link.split('/players/',1)[-1].split('.html',1)[0].replace("/","")
    
    # get player name
    playerName = soup.find('p','margin_top')
    playerName = playerName.find('span').get_text()

    infoall = soup.find_all('p','padding_bottom_half')
    for info1 in infoall:
       info = info1.text
       
    # get position
    position1 = position2 = position3 = position = ''
    if soup.find(text="Position:"):
        position = info[info.find("Position:")+10:info.find("Shoots:")-2]
        a = position.split("and")
        if len(a) == 3:    
            position1 = a[0]
            position2 = a[1]
            position3 = a[2]
            position1 = "".join(c for c in position1 if c.isupper())
            position2 = "".join(c for c in position2 if c.isupper())
            position3 = "".join(c for c in position3 if c.isupper())
        elif len(a) == 2:
            position1 = a[0]
            position2 = a[1]
            position1 = "".join(c for c in position1 if c.isupper())
            position2 = "".join(c for c in position2 if c.isupper())
            position3 = ''
        elif len(a) == 1:
            position1 = "".join(c for c in position if c.isupper())
            position2 = position3 = ''
        
        else:
            position1 = position2 = position3 = ''

    # get shooting hand
    shoots = ''
    if soup.find(text="Shoots:"):
        shoots = info[info.find("Shoots:")+8:info.find("Height:")]
        if "Right" in shoots:
            shoots = "R"
        elif "Left" in shoots:
            shoots = "L"
        else:
            shoots = "E"
    else:
        shoots = ''

    # get height
    height = ''
    if soup.find(text="Height:"):
        height = info[info.find("Height:")+8:info.find("Height:")+12]
        height1,height2 = height.split('-')
        height = int(height1.strip()) * 12 + int(height2[:-1].strip())
    else:
        height = ''
        
    # get weight
    weight = ''
    if soup.find(text="Weight:"):
        weight = info[info.find("Weight:")+8:info.find("lbs")].strip()
    else:
        weight = ''
    
    # get date of birth and city and state/country
    dob = city = state = ''    
    if soup.find(text="Born:"):
        check = soup.find(text="Born:").findNext('span').get_text()
        if ":" not in check:
            birthinfo = soup.find(text="Born:").findNext('span').get_text()
            birthdate = birthinfo.split()
            placeinfo = info[info.find("Born:"):].strip()
            place = placeinfo.split()
            if place[4] == "in":
                place = placeinfo.split("in",1)[-1].strip()
                city = place.split(",",1)[0].strip()
                place = place.split(",",1)[-1].strip()
                state = place.split("\n",1)[0].strip()
            else:
                city = state = ''
                
            if len(birthdate) < 3:
                dob = ''
            else:
                mon = month.index(birthdate[0].strip())+1
                day = int(birthdate[1].split(',',1)[0])
                if mon < 10:
                    mon = "0"+str(mon)
                else:
                    mon = str(mon)
                if day < 10:
                    day = "0"+str(day)
                else:
                    day = str(day)
                dob = birthdate[2].strip() + "-" + mon + "-" + day
        else:
            dob = city = state = ''
    else:
        dob = city = state = ''

    # still alive??
    died = ''
    if soup.find(text="Died:"):
        deathdate = soup.find(text="Died:").findNext('span').get_text()
        if ':' not in deathdate:
            death = deathdate.split()
            mon = month.index(death[0].strip())+1
            day = int(death[1].split(',',1)[0])
            if mon < 10:
                mon = "0"+str(mon)
            else:
                mon = str(mon)
            if day < 10:
                day = "0"+str(day)
            else:
                day = str(day)
                died = death[2].strip() + "-" + mon + "-" + day
        else:
                died = ''
    else:
        died = ''
        
    # get experience
    experience = ''
    if soup.find(text="Experience:"):
        if info.find("Rookie") < 0:
            exp = int(info[info.find("Experience:")+12:info.find(" year")].strip())
        else:
            exp = 0
    else:
        exp = ''
        
    profile = playerID + "," + playerName + "," + position1 + "," + position2 + "," + position3 + "," + shoots
    profile = profile + "," + str(height) + "," + str(weight) + "," + dob + "," + city + "," + state
    profile = profile + "," + str(exp) + "," + died

    print profile
    tofile.write(profile)
    tofile.write("\n")
    time.sleep(randint(0,2))

tofile.close()	
