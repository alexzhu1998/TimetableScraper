import pandas as pd
import pickle
import sys
import os.path
import bs4
from bs4 import BeautifulSoup as soup
from html_dependencies import URL
from datetime import datetime

class Tab(URL):
    def __init__(self, courseCode:str,level:int,year:int = 2020):
        super().__init__(courseCode,level,year)
        self.Dict = None
    
    def save(self):
        self.url_validator()
        assert(self.soup != None)
        # print(self.soup)
        f = open("testSoup.pckl", 'wb')
        pickle.dump(self.soup ,f)
        f.close()

        f = open("testURL.pckl", 'wb')
        pickle.dump(self.url_string(),f)
        f.close()
        print("--SAVED SOUP--")
    
    def open(self)->bool:
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

    def soup_to_dict_level0(self) -> None:
        soup = self.soup
        x = [item.find("a").get('href') for item in soup.findAll("td", {"class":"data"}) if item.find("a")!= None]
        # KENSINGTON CAMPUS ONLY
        
        newx = [item for item in x if item[-9:-5] == 'KENS']
        
        self.Dict = dict.fromkeys(newx)
        print(self.Dict)
        return 

    def soup_to_dict_level1(self) -> None:
        soup = self.soup
        # print(soup)
        x = [item.find("a").get('href') for item in soup.findAll("td", {"class":"data"}) if item.find("a")!= None]
        newx = [item for item in x if item[0:4] == self.course]
        # print(newx)
        self.Dict = dict.fromkeys(newx)
        print(self.Dict)
        return
    def soup_to_dict_level2(self) -> None:
        soup = self.soup
        # x = [(item.find("a").get('href'),item.find("a").string) for item in soup.findAll("td", {"class":"data"}) if item.find("a")!= None]
        x = [item for item in soup.findAll("tr", {"class":"rowHighlight"}) if item.find("a")!= None]
        # x = [item for item in x if (item[1] == "Lecture" or item[1] == "Tutorial")]
        # print(x)
        newx = [item.findAll("td", {"class":"data"}) for item in x]
        table = soup.findAll("td",{"class":"formBody"})
        
        # print(len(table))
        ## To find all the headings
        # heading = [item.string for item in soup.findAll("td", {"class":"tableHeading"})]
        # heading = list(filter(None,heading))
        
        desired_keys = ["Course Code","Teaching Period","Staff Contact"]
        Dict = dict.fromkeys(desired_keys , [])
        # print(Dict)
        # Dict['Course Code'].append(self.code)
        # Dict['Teaching Period']
        text = soup.find(text = "Teaching Period")
        foundText = text.find_parent("tr").find_next_sibling().find_next_sibling().find_next_sibling()
        assert(len(foundText.findAll("td",{"class":"data"})) == 8)
        
        while foundText != None:
            assert(len(foundText.findAll("td",{"class":"data"})) == 8)
            Dict['Course Code'] = Dict['Course Code'] + [self.code]
            Dict['Teaching Period'] = Dict['Teaching Period'] + [foundText.findAll("td",{"class":"data"})[3].string]
            Dict['Staff Contact'] = Dict['Staff Contact'] + [foundText.findAll("td",{"class":"data"})[4].string]
            # print(foundText.findAll("td",{"class":"data"})[3].string)
            # print(foundText.findAll("td",{"class":"data"})[4].string)
            foundText = foundText.find_next_sibling().find_next_sibling()


        desired_keys2 = ["Activity","Teaching Period","Section","Enrols/Capacity","Day/Start Time","Day","Time","StartTime", "EndTime","Weeks","Location",]
        Dict2 = dict.fromkeys(desired_keys2, [])
        teachingPeriods = soup.findAll("td",{"class":"sectionSubHeading"})
        assert(len(teachingPeriods) == len(Dict['Teaching Period']))
        for item in teachingPeriods:
            table = item.find_parent("tr").find_parent("table").find_next_sibling().find_next_sibling()
            tableTags = [item for item in table.children if type(item) == bs4.element.Tag]
            tableVals = [[x.string for x in item.findAll("td", {"class": "data"})] for item in tableTags if (len(item.findAll("td", {"class": "data"})) == 7)]
            for y in tableVals[1:]:
                # print(y)
                Dict2['Activity'] = Dict2['Activity'] + [y[0]]
                Dict2['Teaching Period'] = Dict2['Teaching Period'] + [y[1]]
                Dict2['Section'] = Dict2['Section'] + [y[3]]
                Dict2['Enrols/Capacity'] = Dict2['Enrols/Capacity'] + [y[5]]
                Dict2['Day/Start Time'] = Dict2['Day/Start Time'] + [y[6]]
                Dict2['Day'] = Dict2['Day'] + [[i[0:3]for i in y[6].split('), ')]]
                Dict2['Time'] = Dict2['Time'] + [[i[3:i.find('(',3)].strip() for i in y[6].split('), ')]]
                Dict2['StartTime'] = Dict2['StartTime'] + [[datetime.strptime(i[3:i.find('(',3)].split('-')[0].strip(),'%H:%M') for i in y[6].split('), ')]]
                Dict2['EndTime'] = Dict2['EndTime'] + [[datetime.strptime(i[3:i.find('(',3)].split('-')[1].strip(),'%H:%M') for i in y[6].split('), ')]]
                dateList = y[6].split(', ')
                z = [i[i.find('(')+7:i.find(')')].split(',') for i in dateList]
                tmp2 = []
                for l in z:
                    tmp = []
                    for k in l:
                        # print(k[0],k[-1])
                        tmp = tmp + [i for i in range(int(k.split('-')[0]),int(k.split('-')[-1])+1)]
                    tmp2 = tmp2 + [tmp]

                Dict2['Weeks'] = Dict2['Weeks'] + [tmp2]
        print(Dict2['Day/Start Time'][0])
        print(Dict2['Weeks'][0])
        # print([i for i in Dict2['Day/Start Time'][0].split('), ')])
        
        # print(text)
        
        # print(foundText)
        # newx = [item for item in x if item.find("-") != -1]
        # for item in newx:
        #     for y in item:
        #         print(y.string)
        # y = [ for item in soup.findAll("td", {"class":"data"}) if item.find("a")!= None]
        return

if __name__ == "__main__":
    tab = Tab("MATH1151",2)
    # tab.save()
    if tab.url_validator() == True:
        print("Soup found")
            
        tab.soup_to_dict_level2()
    else:
        print("Soup not found")