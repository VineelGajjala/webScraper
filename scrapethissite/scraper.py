import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#Goal: make a list of dictionary from name of team to other information

url = "https://www.scrapethissite.com/pages/forms/"

def scrapethisuri(uri="/pages/forms/"):
#Getting the original response of the whole website
    page = requests.get("https://scrapethissite.com" + uri)
    assert page.status_code == 200
    soup = BeautifulSoup(page.text, "html.parser")


    # Now lets find the specific table in the website
    div = soup.find(id="hockey")  # Find the right div
    assert len(soup.find_all("table")) == 1
    # print(div)
    table = div.find("table")

    #Now that we have the table, lets start getting the rows
    data_rows = table.find_all("tr", attrs={"class": "team"})  # Includes the header row!
    stat_keys = [col.attrs["class"][0] for col in data_rows[0].find_all("td")]
    final_dict = dict()
    first = True
    for row in data_rows:
        if first:
            first = False
            continue
        temp = dict()
        for attr in stat_keys:
            cur_attribute = row.find("td", attrs={"class": attr}).text
            temp[attr] = re.sub(r"^\s+|\s+$", "", cur_attribute) #clear whitespace 
        final_dict[temp['name'] +"_"+ temp['year']] = temp
    # print(final_dict)
    return final_dict



page = requests.get("https://scrapethissite.com/pages/forms/")
soup = BeautifulSoup(page.text, "html.parser")
pagination = soup.find("ul", attrs={"class": "pagination"})
link_elms = pagination.find_all("li")
links = [link_elm.find("a").attrs["href"] for link_elm in link_elms]
links = set(links)

final = dict()
for link in links:
    tmp_df = scrapethisuri(uri=link)
    final.update(tmp_df)
# hockey_team_df = pd.concat(temp_dfs, axis=0).reset_index(drop=True)
# hockey_team_df.sort_values(["year", "name"], inplace=True)
# hockey_team_df.to_csv("hockey_team_df.csv")
print(len(final))
print(final)


