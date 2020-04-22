import bs4
import time
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
from urllib.parse import urlparse
import sys
import pickle
import os.path
from urllib.error import HTTPError



class URL:
    def __init__(self, courseCode:str,level:int,year:int = 2020):
        self.code = courseCode
        self.course = courseCode[0:4]
        self.level = level
        self.year = year
        self.soup = None

    def url_string(self) -> str:
        if self.level == 0:
            return "http://timetable.unsw.edu.au/"+str(self.year)+"/subjectSearch.html"
        elif self.level == 1:
            return "http://timetable.unsw.edu.au/"+str(self.year)+"/" + str(self.course) +"KENS.html"
        elif self.level == 2:
            return "http://timetable.unsw.edu.au/"+str(self.year)+"/" + str(self.code) +".html#S1-5669"
        else:
            print("INCORRECT LEVEL")
            return ""

    # Function that converts url to soup format
    def url_to_soup(self) -> soup:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        print(self.url_string())
        req = Request(self.url_string(), headers = hdr)
        
        uClient = urlopen(req)
        page_html = uClient.read()
        uClient.close()
        # html parsing
        page_soup = soup(page_html, "html.parser")

        return page_soup

    # Function that passes only valid url
    def url_validator(self):
        try :
            page_soup = self.url_to_soup() 
        except HTTPError:
            print("HTTPError")
            return False

        sys.setrecursionlimit(150000)
        if page_soup == None:
            print("no file")
            return False
        else:
            self.soup = page_soup
            return True
    
    # def 

class Test(URL):

    def __init__(self, courseCode:str,level:int,year:int = 2020):
        super().__init__(courseCode,level,year)
        
    def save(self):
        self.url_validator()
        assert(self.soup != None)
        f = open("testSoup.pckl", 'wb')
        pickle.dump(self.soup ,f)
        f.close()

        f = open("testURL.pckl", 'wb')
        pickle.dump(self.url_string(),f)
        f.close()
        print("--SAVED SOUP--")
    
    def open(self) -> bool:
        f = open('testSoup.pckl', 'rb')
        page_soup = pickle.load(f)
        f.close()

        f = open('testURL.pckl', 'rb')
        url = pickle.load(f)
        f.close()
        if self.url_string() == url:
            print("--OPENED SOUP--")
            print('{}'.format(self.url_string()))
            self.soup = page_soup
            return True
        
        print("--URL SOUP INCONSISTENT--")
        print('SAVED URL: {}'.format(url))
        print('INPUT URL: {}'.format(self.url_string()))
        print("--RETURN INPUT URL SOUP--")
        return self.url_validator()

    # def 




if __name__ == "__main__":
    url = Test("MATH1151",2)
    # url.save()
    if url.url_validator() == True:
        print(url.soup)