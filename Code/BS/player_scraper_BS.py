# to scrap players infos using BS4
# written using Python 3.x

import urllib.request
from bs4 import BeautifulSoup

# declare URL to scrape from and store html in content variable
thisURL = 'http://www.basketball-reference.com/players/c/cabocbr01.html'
content = urllib.request.urlopen(thisURL).read()

# process html using BeautifulSoup
soup = BeautifulSoup(content)

# work in progress - Emery
playerName = soup.find('h1').string
x = soup.find_all('p','padding_bottom_half')
