def benchmark_BS():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Code/Metrics/Benchmark/links_provider_BS.txt','w')
    for i in range(100):
        beg =  time.time()
        all_players_links_BS_bm()
        f.write(str(time.time() - beg))
        print str(time.time() - beg)
        f.write(',')    

def benchmark_regex():
    f = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Code/Metrics/Benchmark/links_provider_regex.txt','w')
    for i in range(100):
        beg =  time.time()
        all_players_links_regex_bm()
        f.write(str(time.time() - beg))
        print str(time.time() - beg)
        f.write(',')

##########################################################
# Get the links to the players' page regex
##########################################################

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links_by_letter_regex_bm(c):
    needle = '[^p]><a href="(/players/./.+)"'    # We use a '.'' for 'letter' because some players change names. In this case 'letter' might not be the same as c.
    html = open('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Code/Metrics/Pages/players_'+c+'.html','r').read()
    return re.findall(needle, html)

# Get the links for all the players
# Return a list with results of the form /players/letter/name.html
def all_players_links_regex_bm():
    alphabet = letters_players_regex()
    res = []
    for c in alphabet:
        res += players_links_by_letter_regex_bm(c)
        # No sleep for benchmark
        # time.sleep(2)
        print c + ' players computed - regex'
    return res


##########################################################
# Get the links to the players' page BS
##########################################################

# Get the links for the players whose names start with the letter c
# Return a list with results of the form /players/letter/name.html
def players_links_by_letter_BS_bm(c): 
    soup = file_to_soup('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Code/Metrics/Pages/players_'+c+'.html')
    res = []
    for player in soup.tbody.find_all('tr'):
        res.append(str(player.td.a.get('href')))
    return res

# Get the links for all the players (total: 4288)
# Return a list with results of the form /players/letter/name.html
def all_players_links_BS_bm():
    alphabet = letters_players_BS_bm()
    res = []
    for letter in alphabet:
        res += players_links_by_letter_BS_bm(letter)
        # No sleep for benchmark
        # time.sleep(2)
        # Get feedback from computing
        print letter + ' players computed - BS'
    return res

##########################################################
# Get the letters which are not empty, i.e. at least one player's name starts with these letters
##########################################################

# Return a list of the form ['a', 'b', ..., 'z']
def letters_players_BS_bm():
    letters = []
    # Opening player's page and making the soup
    soup = file_to_soup('/Users/emilebres/Documents/NUS/IS5126 HowBA/NBA_project/Code/Metrics/Pages/players.html')
    # Get the letters
    for row in soup('td', {'class': 'align_center bold_text valign_bottom xx_large_text'}):
        letters.append(str(row.a.get('href').split('/')[2]))
    return letters

##########################################################
# Miscellanous
##########################################################

def file_to_soup(path):
    html = open(path,'r').read()
    return BeautifulSoup(html)