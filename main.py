import pickle
import pandas as pd
from html_dependencies import *
# from tables_manipulation import *
import requests
from bs4 import BeautifulSoup as soup


# http://timetable.unsw.edu.au/2020/subjectSearch.html
url = 'http://timetable.unsw.edu.au/2020/subjectSearch.html'

soup = html_import(url,False,False)

x = [item.find("a").get('href') for item in soup.findAll("td", {"class":"data"}) if item.find("a")!= None]
# KENSINGTON CAMPUS ONLY
newx = [item for item in x if item[-9:-5] == 'KENS']
print(list(dict.fromkeys(newx)))
# print(soup)


