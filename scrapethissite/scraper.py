import requests
from bs4 import BeautifulSoup
import re

#Goal: make a list of dictionary from name of team to other information

url = "https://www.scrapethissite.com/pages/forms/"

#Getting the original response of the whole website
page = requests.get(url)
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
    final_dict[temp['name']] = temp
print(final_dict)








# site = 'https://www.scrapethissite.com/pages/simple'
# hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#        'Accept-Encoding': 'none',
#        'Accept-Language': 'en-US,en;q=0.8',
#        'Connection': 'keep-alive'}

# data =urllib.request.Request(site, None, headers=hdr)
# html = urllib.request.urlopen(html)
# bs = BeautifulSoup(html, "html.parser")
# # print(bs.title)