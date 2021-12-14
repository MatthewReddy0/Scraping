import math
import pandas as pd
"""
For playing up to 60 minutes	1
For playing 60 minutes or more (excluding stoppage time)	2
Min

For each goal scored by a goalkeeper or defender	6
For each goal scored by a midfielder	5
For each goal scored by a forward	4
Gls

For each goal assist	3
Ast

For a clean sheet by a goalkeeper or defender	4
For a clean sheet by a midfielder	1
For every 2 goals conceded by a goalkeeper or defender	-1
Result

For every 3 shot saves by a goalkeeper	1
For each penalty save	5
/keeper/ Saves, PKsv

For each penalty miss	-2
PKatt - PK

For each yellow card	-1
CrdY, if 2, 0
For each red card	-3
CrdR
For each own goal	-2
/misc/ OG
"""


def fantasy_scoring(stats_type: str, match_log_df: pd.DataFrame, position: str, fantasy_points_list: list):
    if stats_type == 'summary':
        fantasy_points_list = [0] * len(match_log_df.index)

        minutes = match_log_df['Min'].tolist()
        goals = match_log_df['Gls'].tolist()
        assists = match_log_df['Ast'].tolist()
        results = match_log_df['Result'].tolist()
        penalties = match_log_df['PK'].tolist()
        attempted_penalties = match_log_df['PKatt'].tolist()
        yellow_cards = match_log_df['CrdY'].tolist()
        red_cards = match_log_df['CrdR'].tolist()

        for i in range(len(match_log_df.index)):
            fantasy_points_scored = 0

            if 0 < minutes[i] < 60:
                fantasy_points_scored += 1
            elif minutes[i] > 60:
                fantasy_points_scored += 2

            if goals[i] > 0:
                if position in ['Goalkeepers', 'Defenders']:
                    fantasy_points_scored += (goals[i] * 6)
                elif position == 'Midfielders':
                    fantasy_points_scored += (goals[i] * 5)
                elif position == 'Forwards':
                    fantasy_points_scored += (goals[i] * 4)

            fantasy_points_scored += (assists[i] * 3)

            goals_conceded = int(results[i][4:])
            if goals_conceded == 0 and position in ['Goalkeepers', 'Defenders', 'Midfielders']:
                if position in ['Goalkeepers', 'Defenders']:
                    fantasy_points_scored += 4
                elif position == 'Midfielders':
                    fantasy_points_scored += 1
            elif goals_conceded > 0 and position in ['Goalkeepers', 'Defenders']:
                fantasy_points_scored += (-1 * math.floor(goals_conceded / 2))

            if (attempted_penalties[i] - penalties[i]) > 0:
                fantasy_points_scored += (-2 * (attempted_penalties[i] - penalties[i]))

            if red_cards[i] == 1:
                fantasy_points_scored += -3
            elif yellow_cards[i] == 1:
                fantasy_points_scored += -1

            fantasy_points_list[i] = fantasy_points_list[i] + fantasy_points_scored

    elif stats_type == 'misc':
        own_goals = match_log_df['OG'].tolist()

        for i in range(len(match_log_df.index)):
            fantasy_points_scored = 0

            fantasy_points_scored += (-2 * own_goals[i])

            fantasy_points_list[i] += fantasy_points_scored

    elif stats_type == 'keeper' and position == 'Goalkeepers':
        saves = match_log_df['Saves'].tolist()
        penalty_saves = match_log_df['PKsv'].tolist()

        for i in range(len(match_log_df.index)):
            fantasy_points_scored = 0

            fantasy_points_scored += (1 * math.floor(saves[i] / 3))

            fantasy_points_scored += (5 * penalty_saves[i])

            fantasy_points_list[i] += fantasy_points_scored

    return fantasy_points_list
