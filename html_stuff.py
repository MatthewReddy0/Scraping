from bs4 import BeautifulSoup
import re
from selenium import webdriver
import pandas as pd

"""
Use CSS or XPath Selectors
Ctrl+Shift+C to open developer tools
Right-click to copy selectors


example = open("example.html", "r")
html = example.read()
# html = request.get(url).text
example.close()

soup = BeautifulSoup(html)
print(soup.prettify())

print(soup.title,
      soup.li,
      soup.find_all('li'))
"""


def get_fpl_players_df() -> pd.DataFrame:
    start_url = 'https://fantasy.premierleague.com/player-list'

    driver = webdriver.Chrome(executable_path=r"C:\Users\reddy\Downloads\chromedriver_win32\chromedriver.exe")

    driver.get(start_url)

    html = driver.page_source

    soup = BeautifulSoup(html, features="lxml")

    driver.close()

    df_columns = ['Player', 'Team', 'Points', 'Cost', 'Position']
    df = pd.DataFrame(columns=df_columns)

    for pos_num in ['1', '2', '3', '4']:
        position_select_query = f'#root > div:nth-child(2) > div > div:nth-child({pos_num}) > div > h3'
        position = soup.select(position_select_query)[0].text

        for i in ['1', '2']:
            select_query = f'#root > div:nth-child(2) > div > div:nth-child({pos_num}) > div > div > table:nth-child({i}) >'
            full_table = soup.select(select_query + ' tbody')[0]
            # print(full_table)
            table_head = soup.select(select_query + ' thead')[0]
            # print(table_head)

            regex = re.compile('_\[\w\]')
            table_columns = []
            for element in table_head:
                column_label = element.get_text(separator=" ", strip=True)
                column_label = column_label.replace(' ', '_')
                column_label = regex.sub('', column_label)
                table_columns.append(column_label)
            table_columns = table_columns[0].split("_")

            table_rows = full_table.select('tr')
            table_data = []
            for index, element in enumerate(table_rows):
                row_list = []
                values = element.select('td')
                # row_list.append(element.select('th')[0].text.strip())
                for value in values:
                    row_list.append(value.text.strip())

                table_data.append(row_list)
            # print(table_columns)
            # print(table_data)

            intermediate_df = pd.DataFrame(table_data, columns=table_columns)
            intermediate_df['Position'] = position
            df = pd.concat([df, intermediate_df])
    df = df.rename(columns={"Team": "Club"})
    df = df.reset_index()
    df = df.drop(['index'], axis=1)
    return df


# df1 = get_fpl_players_df()
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(df1)
