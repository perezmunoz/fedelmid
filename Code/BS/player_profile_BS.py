# to scrap players infos using BS4
# written using Python 3.x

import urllib.request
import string
from bs4 import BeautifulSoup

# declare URL to scrape from and store html in content variable
thisURL = 'http://www.basketball-reference.com/players/h/howardw01.html'
content = urllib.request.urlopen(thisURL).read()

# process html using BeautifulSoup
soup = BeautifulSoup(content)

# get player name
playerName = soup.find('p','margin_top')
playerName = playerName.find('span').get_text()

infoall = soup.find_all('p','padding_bottom_half')
for info1 in infoall:
   info = info1.text
   
# get position
if soup.find(text="Position:"):
    position = info[info.find("Position:")+10:info.find("Shoots:")-2]
    if "and" in position:
        position1,position2 = position.split("and")
        position1 = "".join(c for c in position1 if c.isupper())
        position2 = "".join(c for c in position2 if c.isupper())
    else:
        position1 = "".join(c for c in position if c.isupper())
        position2 = ''
else:
    position1 = ''
    position2 = ''


# get shooting hand
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
if soup.find(text="Height:"):
    height = info[info.find("Height:")+8:info.find("Weight:")]
    height1,height2 = height.split('-')
    height = int(height1.strip()) * 12 + int(height2[:-2].strip())
else:
    height = ''
    
# get weight
if soup.find(text="Weight:"):
    weight = info[info.find("Weight:")+8:info.find("lbs")].strip()
else:
    weight = ''
    
# get date of birth, city, state/country
if soup.find(text="Born:"):
    dob = soup.find(text="Born:").findNext('span')['data-birth']
    birthinfo = info[info.find("Born:"):].strip()
    place = birthinfo.split()
    if place[4] == "in":
        place = birthinfo.split("in",1)[-1].strip()
        city = place.split(",",1)[0].strip()
        place = place.split(",",1)[-1].strip()
        state = place.split("\n",1)[0].strip()
    else:
        city = ''
        state = ''
else:
    dob = ''
    
# still alive??
if soup.find(text="Died:"):
    died = soup.find(text="Died:").findNext('span')['data-death']
else:
    died = ''
    
# get experience
if soup.find(text="Experience:"):
    if info.find("Rookie") < 0:
        exp = int(info[info.find("Experience:")+12:info.find("years")].strip())
    else:
        exp = 0
else:
    exp = ''
    
profile = playerName + "," + position1 + "," + position2 + "," + shoots
profile = profile + "," + str(height) + "," + str(weight) + "," + dob + "," + city + "," + state
profile = profile + "," + str(exp) + "," + died

print(profile)


# ===============================================================================
# Some code for scraping
# ===============================================================================
# Scrap profile's information

# declare URL to scrape from and store html in content variable
urlHandle = urllib.urlopen('http://www.basketball-reference.com/players/c/cabocbr01.html')
html = urlHandle.read()

# process html using BeautifulSoup
soup = BeautifulSoup(content)

# get player name
playerName = soup.find('h1')
for n in playerName:
   name = n

# get info like position, shoots, height, weight, born, country, draft, NBA debut, experience
infoall = soup.find_all('p','padding_bottom_half')
for info1 in infoall:
   info = info1.text
   
def get_profile_player(link_player):

    # List containing the player's profile
    res = []

    # Letters of the players
    # execfile('scraping_links_players.py') prior to lunch this script
    alphabetical = get_letters_players()

    index = BeautifulSoup(urllib.urlopen('http://www.basketball-reference.com/players/'+link_player[0]+'/'+link_player).read())
    # class=padding_bottom_half is unique
    # The used of find_all returns a bs4.element.ResultSet element which cannot be accessed
    # find method returns a Tag object which can be accessed with common methods
    profile = index.find('p', {'class': 'padding_bottom_half'})

    # Retrieve all text data from profile (outside tags)
    # profile_str = profile.get_text()
    # Removing \xa0 and \u25aa characters (using unicode characters)
    # profile_str.replace(u'\xa0\u25aa\xa0',u' ').replace(u'\n',u'')

    # A way to chain these two previous lines
    profile_str = str((profile.get_text()).replace(u'\xa0\u25aa\xa0',u' ').replace(u'\n',u''))

    # profile_str.split('Position:','Shoots:','Height:','Weight:','Born:','High School:','College:','Draft:','NBA Debut:','Other Pages:')
    # re.split('[Position: Shoots: Height:]',profile_str)
    profile_split = re.split('(?:Position:|Shoots:|Height:|Weight:|Born:|High School:|College:|Draft:|NBA Debut:|Other Pages:)',profile_str)

    # Remove 1st element which is empty
    del profile_split[0]

    # Strip each element of the list. 
    res += map(str.strip,profile_split)
    # Player's profile:
    # [0] Position
    # [1] Shoots
    # [2] Heigh
    # [3] Weight
    # [4] Born (date and place)
    # [5] High School
    # [6] College
    # [7] Draft
    # [8] NBA Debut
    # [9] Others Pages
    return res

def get_all_profile_player():

    # Player's profile list
    profiles = [[]]

    for player in res[0]:
        profiles += get_profile_player(player)
        # Output to algorithm's steps
        print player

    return profiles

# Get all profile's characteristics in order to build player's profile
def get_all_characteristics():

    # Date regex
    date_regex = re.compile("[A-Za-z]*\s[0-9]*[,]{1}\s[0-9]*")

    # Characteristics'list
    properties = []

    # res[0] contains all url's players
    res = [[]]
    res = get_all_players()

    for player in res[0]:

        # Sleeps 1 seconde
        time.sleep(1)

        # Player's soup
        index = BeautifulSoup(urllib.urlopen('http://www.basketball-reference.com/players/'+player[0]+'/'+player).read())
        # Retrieving p tag containing relevant information
        profile = index.find('p', {'class': 'padding_bottom_half'})
        # Get all span tags containing characteristics
        span_tag = profile.find_all('span')

        # Testing whether it's already in properties list or not
        for char in span_tag:
            char_str = str(char.get_text())
            if date_regex.match(char_str) or char_str=='':
                print "Date or blank avoided"
                print char_str
            else:
                if char_str in properties:
                    print "Characteristic already in properties list"
                else:
                    properties.append(char_str)
    
    return properties
