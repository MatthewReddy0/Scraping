import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_match_log_table(start_url: str) -> pd.DataFrame:
    downloaded_html = requests.get(start_url)

    soup = BeautifulSoup(downloaded_html.text, features="html.parser")

    # with open('Player.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())

    if start_url[48:49] == 's':
        select_query = '#matchlogs_11160 > '
    else:
        select_query = '#matchlogs_all > '
    full_table = soup.select(select_query + 'tbody')[0]
    # print(full_table)
    table_head = soup.select(select_query + 'thead')[0]
    # print(table_head)

    regex = re.compile('_\[\w\]')
    table_columns = []
    for element in table_head:
        column_label = element.get_text(separator=" ", strip=True)
        column_label = column_label.replace(' ', '_')
        column_label = regex.sub('', column_label)
        table_columns.append(column_label)
    table_columns = table_columns[3]
    table_columns = table_columns.split("_")
    table_columns[-2:] = [''.join(table_columns[-2:])]
    while True:
        if '3rd' in table_columns:
            place = table_columns.index('3rd')
            table_columns[place - 1:place + 1] = [''.join(table_columns[place - 1:place + 1])]
        elif 'Pen' in table_columns:
            place = table_columns.index('Pen')
            table_columns[place - 1:place + 1] = [''.join(table_columns[place - 1:place + 1])]
        else:
            break

    table_rows = full_table.select('tr')
    table_data = []
    for index, element in enumerate(table_rows):
        if not element.text.strip():
            continue

        row_list = []
        values = element.select('td')
        row_list.append(element.select('th')[0].text.strip())
        for value in values:
            row_list.append(value.text.strip())

        table_data.append(row_list)

    df = pd.DataFrame(table_data, columns=table_columns)

    return df


# j = get_match_log_table('https://fbref.com/en/players/7a2e46a8/matchlogs/s11160/keeper/Alisson-Match-Logs')
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(j)
