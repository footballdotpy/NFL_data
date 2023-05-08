import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# create empty list to store data.

nfl_data = pd.DataFrame(
    columns=['Week', 'Day', 'Date', 'Time', 'Home_team', 'Away_team', 'Home_team_pts', 'Away_team_pts'])

seasons = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

for season in seasons:

    url = 'https://www.pro-football-reference.com/years/{}/games.htm'.format(season)

    dfs = pd.read_html(url, flavor='lxml', index_col=False)

    # access the first (and only) dataframe
    df = dfs[0]
    df.columns = ['Week', 'Day', 'Date', 'Time', 'Winner/Tie', 'H/A', 'Loser/Tie', 'Boxscore', 'Pts_winner',
                  'Pts_loser', 'YdsW', 'TOW', 'YdsL', 'TOL']

    # drop rows where the 'Week' column contains 'Week'
    # convert the column to string first.
    df['Week'] = df['Week'].astype(str)

    df = df[~df['Week'].str.contains('Week')]

    # drop the nan row

    df = df.dropna(subset=['Week'])

    # set nulls to home

    df['H/A'] = df['H/A'].fillna('H')

    # define a function to determine the home team based on the values in the 'H/A' and 'Loser/Tie' columns
    def get_home_team(row):
        if row['H/A'] == 'H':
            return row['Winner/Tie']
        elif row['H/A'] == '@':
            return row['Loser/Tie']
        elif row['H/A'] == 'N':
            return row['Winner/Tie']

    # define a function to determine the away team based on the values in the 'H/A' and 'Loser/Tie' columns
    def get_away_team(row):
        if row['H/A'] == '@':
            return row['Winner/Tie']
        elif row['H/A'] == 'H':
            return row['Loser/Tie']
        elif row['H/A'] == 'N':
            return row['Loser/Tie']

    # define a function to determine the home team points based on the values in the 'H/A' and 'Loser/Tie' columns
    def get_home_team_pts(row):
        if row['H/A'] == 'H':
            return row['Pts_winner']
        elif row['H/A'] == '@':
            return row['Pts_loser']
        elif row['H/A'] == 'N':
            return row['Pts_winner']

    # define a function to determine the away team points based on the values in the 'H/A' and 'Loser/Tie' columns
    def get_away_team_pts(row):
        if row['H/A'] == '@':
            return row['Pts_winner']
        elif row['H/A'] == 'H':
            return row['Pts_loser']
        elif row['H/A'] == 'N':
            return row['Pts_loser']


    # apply the functionS

    df['Home_team'] = df.apply(get_home_team, axis=1)
    df['Away_team'] = df.apply(get_away_team, axis=1)
    df['Home_team_pts'] = df.apply(get_home_team_pts, axis=1)
    df['Away_team_pts'] = df.apply(get_away_team_pts, axis=1)

    df = df[['Week', 'Day', 'Date', 'Time', 'Home_team', 'Away_team', 'Home_team_pts', 'Away_team_pts']]

    nfl_data = nfl_data.append(df, ignore_index=True)

    continue
nfl_data = nfl_data.dropna()
nfl_data.to_csv('nfl_historical_data.csv', index=False)
