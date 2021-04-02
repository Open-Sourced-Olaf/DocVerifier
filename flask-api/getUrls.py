from bs4 import BeautifulSoup
import requests
import re

def collect_url_links(url_link)->list:
  url_list = []
  pattern = re.compile(r'^http')

  source = requests.get(url_link).text
  soup = BeautifulSoup(source, 'lxml')

  a_tag = soup.find_all("a") #Gives you the list of all the a tags
  for i in a_tag:
    if i.text in ["Privacy", "Terms", "Privacy Policy", "Terms of Service"]:
        url = i["href"]
        url_list.append(url)

  for i in range(len(url_list)):
    matches = pattern.finditer(url_list[i])

    if(not (any(True for _ in matches))):
      url_list[i] = url_link + url_list[i][1:]

  return url_list