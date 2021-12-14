import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

start_url = 'https://fbref.com/en/players/d70ce98e/Lionel-Messi'

downloaded_html = requests.get(start_url)

soup = BeautifulSoup(downloaded_html.text, features="html.parser")

with open('Lionel-Messi.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
#stats_standard_dom_lg
# //*[@id="stats_standard_dom_lg"]
full_table = soup.select('#stats_standard_dom_lg tbody')[0]
# print(full_table)
table_head = soup.select('#stats_standard_dom_lg > thead')[0]
# print(table_head)

regex = re.compile('_\[\w\]')
table_columns = []
for element in table_head:
    column_label = element.get_text(separator=" ", strip=True)
    column_label = column_label.replace(' ', '_')
    column_label = regex.sub('', column_label)
    table_columns.append(column_label)
# print(table_columns)
table_columns = table_columns[3]
table_columns = table_columns.split("_")
# print(table_columns)

table_rows = full_table.select('tr')
table_data = []
for index, element in enumerate(table_rows):
    row_list = []
    values = element.select('td')
    # print(str(values))
    # print(str(values).index('2021-2022'))
    # print(str(values)[109:118])
    row_list.append(str(values)[109:118])
    for value in values:
        row_list.append(value.text.strip())
        # print(value)

    table_data.append(row_list)
# print(table_data)
# table_data.insert(0, table_columns)
# print(table_data)

df = pd.DataFrame(table_data, columns=table_columns)

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)
