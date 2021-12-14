from all_premier_league_players import get_players_match_log_hyperlinks
from scores_and_fixtures import scores_and_fixtures_df
from match_logs import get_match_log_table
import pandas as pd
import df_cleaning as dfc
from html_stuff import get_fpl_players_df
from fantasy_points import fantasy_scoring

"""
Make sure that you're not breaking laws or terms and conditions

py -m jupyter lab
pipenv shell

Check the website for 500 error
"""

# Correct number = 461
number_of_players = 1


# Setting the All_PL_Players url
host = 'https://fbref.com/en/comps/'
competition_number = '9'
which_stats_page = 'stats'
competition_name = 'Premier-League-Stats'
url = host + competition_number + '/' + which_stats_page + '/' + competition_name


# Getting all the players URLs, names and clubs in a pandas dataframe, and then
all_pl_players_df = get_players_match_log_hyperlinks(url, number_of_players)

# Not iterating through the whole dataframe:
# all_pl_players_df['Player'] = all_pl_players_df['Player'].apply(lambda x: x[(x.index(' ') + 1):])
# Instead, converting to a list, iterating through that, and then making that the dataframe column
player_names_list = all_pl_players_df['Player'].to_list()
for i in range(len(player_names_list)):
    player_names_list[i] = player_names_list[i][(player_names_list[i].index(' ') + 1):]
all_pl_players_df['Player'] = player_names_list

# Adjusting the names of all the clubs so they match the ones in the fantasy table
all_pl_players_df['Club'] = all_pl_players_df['Club'].map({'Manchester City': 'Man City', 'Manchester United':
                                                           'Man Utd', 'Tottenham': 'Spurs', 'Leicester City':
                                                           'Leicester', 'Newcastle Utd': 'Newcastle',
                                                           'Norwich City': 'Norwich', 'Leeds United': 'Leeds'}
                                                          )


# Setting and getting all the scores and fixtures
competition_name = 'Premier-League-Scores-And-Fixtures'
which_stats_page = 'schedule'
url = host + competition_number + '/' + which_stats_page + '/' + competition_name
scores_and_fixtures_df = scores_and_fixtures_df(url)


# Getting the names, clubs, fantasy points and fantasy cost of each player in a dataframe
fpl_players_df = get_fpl_players_df()
# fpl_players_df.rename(columns={"Team": "Club"})

# Joining the FBRef dataframe with the FPL dataframe. 'Player' and 'Club' should be the inner joiners
# joined_df = pd.concat([all_pl_players_df, fpl_players_df], axis=1, join='inner')
joined_df = all_pl_players_df.merge(fpl_players_df)


urls_and_positions = pd.concat([joined_df['URL'], joined_df['Position']], axis=1)
# Getting the FBRef URLs for the players' match log pages
player_match_log_urls = urls_and_positions.values.tolist()
# There are 8 types of log pages
# log_pages = ['summary', 'passing', 'passing_types', 'gca', 'defense', 'possession', 'misc', 'keeper']
log_pages = ['summary', 'misc', 'keeper']
host = 'https://fbref.com'  # URL building takes place in the loop, don't delete this

for row in player_match_log_urls:
    player_url = row[0]
    position = row[1]

    # Specifies that we're talking about the Premier League 2021-20222 season, not all competitions
    if '2021-2022' in player_url:
        player_url = player_url.replace('2021-2022', 's11160')
    two_halves_of_player_url = player_url.split('summary')
    # print(player_url)

    # List of fantasy points scored in each week
    # This will be made into list of 0s of the same length as the match log dataframes
    fantasy_points_list = []

    # Goes through each of the 8 types of log pages, and gets a dataframe of each
    for stats_type in log_pages:
        full_url = host + two_halves_of_player_url[0] + stats_type + two_halves_of_player_url[1]
        match_log_df = get_match_log_table(full_url)

        # Cleaning each log DF
        match_log_df = dfc.remove_match_report(match_log_df)
        match_log_df = dfc.clean_round(match_log_df)
        match_log_df = dfc.remove_day(match_log_df)
        match_log_df = dfc.clean_to_numbers(match_log_df)
        match_log_df = dfc.convert_date(match_log_df)
        match_log_df = dfc.convert_pos_to_fpl(match_log_df, position)

        round_no = match_log_df['Round'].values.tolist()

        fantasy_points_list = fantasy_scoring(stats_type, match_log_df, position, fantasy_points_list)

    fantasy_points_df = pd.DataFrame(
        {'Round': round_no,
         'Points': fantasy_points_list
         })

joined_df = joined_df.drop(['URL'], axis=1)
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(joined_df)
print(fantasy_points_df)


# TODO: Create SQL database linking joined_df, each player's match log tables, and each player's fantasy_points_df
# TODO: Incorporate injuries, players not playing
# TODO: Machine learning for a team at the start of 2-5-5-3 formation which can only change 1 player each week
# TODO:     highscore by this point
# TODO:     highscore by end of season
