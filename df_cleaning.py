import pandas as pd
from datetime import datetime as dt


def convert_date(df):
    # df['Date'] = df['Date'].apply(lambda x: dt.strptime(x, '%Y-%m-%d').date())
    column_list = []
    for x in df['Date'].tolist():
        column_list.append(dt.strptime(x, '%Y-%m-%d').date())
    df['Date'] = column_list
    return df


def convert_pos_to_fpl(df, position):
    df['Pos'] = position
    return df


def try_to_clean(x):
    try:
        x = int(x)
    except (ValueError, TypeError):
        try:
            x = float(x)
        except (ValueError, TypeError):
            pass
    return x


def clean_to_numbers(df):
    for column in df:
        lst = df[column].values.tolist()
        df[column] = [try_to_clean(i) for i in lst]
    return df


def clean_round(df):
    # df['Round'] = df['Round'].apply(lambda x: int(x[10:]))
    column_list = []
    for x in df['Round'].tolist():
        column_list.append(int(x[10:]))
    df['Round'] = column_list
    return df


def remove_day(df):
    return df.drop(['Day'], axis=1)


def remove_match_report(df):
    return df.drop(['MatchReport'], axis=1)


# months = ['Jan', 'Apr', 'Mar', 'June']
# days = ['31', '30', '31', '30']
# df1 = {'Month': months, 'Day': days}
# df1 = pd.DataFrame(df1)
# df1 = clean_to_numbers(df1)
#
# print(df1)
# print(type(df1['Day'][0]))

