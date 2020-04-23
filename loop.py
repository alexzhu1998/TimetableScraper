from html_dependencies import URL
from soup import Tab
import pandas as pd
import pickle
import os
import time

class Loop:
    def __init__(self, faculty: list):
        self.faculty = faculty
        self.df = None
    
    def fullLoop(self,name) -> None:
        dict_list = dict()
        unavailable_fac = []
        unavailable_courses = []
        for item in self.faculty:
            print("Current Faculty: {}".format(item))
            tab = Tab(item,1)
            if tab.url_validator():
                tab.soup_to_dict_level1()
                for x in list(tab.Dict.keys()):
                    print("Current Course: {}".format(x))
                    a = Tab(x,2)
                    if a.url_validator():
                        a.soup_to_dict_level2()
                        if list(dict_list.keys()) != list(a.Dict.keys()):
                            dict_list = dict.fromkeys(a.Dict.keys(),[]) 
                        for item in dict_list.keys():
                            dict_list[item] = dict_list[item] + a.Dict[item]
                        
                    else:
                        print("Course {} is not available".format(x))
                        unavailable_courses.append(x)
            else:
                print("Faculty {} is not available".format(item))
                unavailable_fac.append(item)
        # print(dict_list)
        self.df = pd.DataFrame.from_dict(dict_list)
        # print(self.df)
        self.df.to_csv('results/'+name,index = False)
        print("All unavailable faculties: {}".format(unavailable_fac))
        print("All unavailable courses: {}".format(unavailable_courses))

        
    
def getFacultyList(d:dict):
    return list(d.keys())

if __name__ == "__main__":
    start_time = time.time()
    tab = Tab("COMP1511",0)
    if tab.url_validator(): tab.soup_to_dict_level0()
    l = getFacultyList(tab.Dict)
    l = ['COMP','MATH']
    name = ''
    for item in l:
        name = name + '-' + str(item) 
    name = name[1:]
    # print(name)
    loop = Loop(l)
    loop.fullLoop(name + ".csv")
    print("Total Runtime: {}".format(time.time()-start_time))

