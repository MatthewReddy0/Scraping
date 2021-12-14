import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def scores_and_fixtures_df(url: str) -> pd.DataFrame:
    start_url = url

    downloaded_html = requests.get(start_url)

    soup = BeautifulSoup(downloaded_html.text, features="html.parser")

    with open('Premier_League_Score_and_Fixtures_2021-22.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    full_table = soup.select('#sched_11160_1 > tbody')[0]
    # print(full_table)
    table_head = soup.select('#sched_11160_1 > thead')[0]
    # print(table_head)

    regex = re.compile('_\[\w\]')
    table_columns = []
    for element in table_head:
        column_label = element.get_text(separator=" ", strip=True)
        column_label = column_label.replace(' ', '_')
        column_label = regex.sub('', column_label)
        table_columns.append(column_label)
    # print(table_columns)
    table_columns = table_columns[1]
    # print(table_columns)
    table_columns = table_columns.split("_")
    table_columns[12: 14] = [''.join(table_columns[12: 14])]
    # print(table_columns)

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
            # print(value)
        table_data.append(row_list)
    # print(table_data)
    # table_data.insert(0, table_columns)
    # print(table_data)

    df = pd.DataFrame(table_data, columns=table_columns)

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    return df
