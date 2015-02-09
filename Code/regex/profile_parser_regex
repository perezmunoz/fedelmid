# Parse profile information using Regex
# sample code without error checking and string manipulation to adjust output to fit
# template for csv file for loading to database
import urllib
import string,re,time

# Get the links to the players' page
#thisURL = 'http://www.basketball-reference.com/players/c/caldwke01.html'
thisURL = 'http://www.basketball-reference.com/players/m/macklve01.html'
	
needle = ''
html = urllib.urlopen(thisURL).read()
needle = '<p class="margin_top"><span class="bold_text">(.+?)</span>'
name = re.findall(needle,html)
needle = '<span class="bold_text">Position:</span>(.+?)&nbsp'
position = re.findall(needle,html)
needle = '<span class="bold_text">Shoots:</span>(.+?)<br>'
shoots = re.findall(needle,html)
needle = '<span class="bold_text">Height:</span>(.+?)&nbsp'
height = re.findall(needle,html)
needle = '<span class="bold_text">Weight:</span>(.+?)lbs'
weight = re.findall(needle,html)
needle = 'data-birth="(.+?)">'
born = re.findall(needle,html)
print name[0]
print position[0]
print shoots[0]
print height[0]
print weight[0]
print born[0]
