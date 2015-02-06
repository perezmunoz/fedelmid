# Main file

# Source the differents scripts
execfile('./BS/links_provider_BS.py')
execfile('./BS/player_profile_BS.py')
execfile('./BS/player_statistics_BS.py')
execfile('./BS/team_scraper_BS.py')

execfile('./Metrics/benchmark_script.py')
execfile('./Metrics/html_downloader.py')

execfile('./regex/player_profile_regex.py')
execfile('./regex/links_provider_regex.py')

# Get player's links
links_players_BS = []
links_players_BS = all_players_links_BS()
links_players_regex = []
links_players_regex = all_players_links_regex()

# Get team's links
links_teams_BS = []
links_teams_BS = all_teams_links_BS()
links_teams_regex = []
links_teams_regex = all_teams_links_regex()

# Get the number of all players or by a letter
number_all_players_BS()
number_all_players_regex()
# Select a letter
c = 'a'
number_players_BS(c)
number_players_regex()

# Functions below call automatically the functinos all_players_links() and all_teams_links()
# Get the player's basic statistics and salaries
all_statistics_players()

# Get the player's profile
all_profiles_players()

# Get team's statistics
all_statistics_teams()

# Download the player's html pages
dl_players()

# Download the teams's html pages
dl_teams()