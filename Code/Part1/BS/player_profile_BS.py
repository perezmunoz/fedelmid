# Provide the .csv file of player's profile using BS4

from bs4 import BeautifulSoup
from random import randint
import urllib, string, time, csv

# Define the list of year's month
month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# The following properties defined the profile of a player:
# PlayerID
# Player's name
# Position 1
# Position 2
# Position 3
# Shooting Hand
# Height
# Weight
# Date of Birth
# City
# State/Country
# Still alive?
# Experience

def all_profiles_players():
    all_links = all_players_links()
    # Open a .csv file to write into
    output_file = open('player_profile.csv','w')
    # Traverse list and build url to get individual player link
    for link in all_links:
        urlHandle = 'http://www.basketball-reference.com' + link
        html = urllib.urlopen(urlHandle).read()
    # Store content in soup object
    soup = BeautifulSoup(hmtl)
    # Get playerID
    playerID = link.split('/players/',1)[-1].split('.html',1)[0].replace("/","")
    # Get player name
    playerName = soup.find('p','margin_top')
    playerName = playerName.find('span').get_text()
    # Get all the information
    info_all = soup.find_all('p','padding_bottom_half')
    for e in info_all:
       info = e.text
    # Get the differents player's positions. A player can have maximum 3 differents positions
    position1 = position2 = position3 = position = ''
    if soup.find(text = "Position:"):
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
    # Get Shooting Hand
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
    # Get Height
    height = ''
    if soup.find(text="Height:"):
        height = info[info.find("Height:")+8:info.find("Height:")+12]
        height1,height2 = height.split('-')
        height = int(height1.strip()) * 12 + int(height2[:-1].strip())
    else:
        height = ''
    # Get Weight
    weight = ''
    if soup.find(text="Weight:"):
        weight = info[info.find("Weight:")+8:info.find("lbs")].strip()
    else:
        weight = ''
    # Get date of birth, city and state/country
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
    # Is the player still alive?
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
    # Get Experience
    experience = ''
    if soup.find(text="Experience:"):
        if info.find("Rookie") < 0:
            exp = int(info[info.find("Experience:")+12:info.find(" year")].strip())
        else:
            exp = 0
    else:
        exp = ''
    # Building the line containing all the information about the player
    profile = playerID + "," + playerName + "," + position1 + "," + position2 + "," + position3 + "," + shoots
    profile = profile + "," + str(height) + "," + str(weight) + "," + dob + "," + city + "," + state
    profile = profile + "," + str(exp) + "," + died
    # Print the profile at the terminal. For instance:
    # aabdulma01,Mahdi Abdul-Rahman,PG,SG,,R,74,185,4/15/42,Philadelphia,Pennsylvania,,11/18/11
    print profile
    # Write the profile into the file
    output_file.write(profile)
    output_file.write("\n")
    time.sleep(randint(0,2))
    output_file.close()	