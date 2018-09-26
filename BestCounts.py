# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 22:42:15 2018

@author: Yuyang Wang
"""

import json

def write_json(json_file, temp_dict):
    
    json_str = json.dumps(temp_dict) #turn dict to str
    new_dict = json.loads(json_str) #turn str to json_dict
    json.dump(new_dict,json_file) #write                                  
    json_file.write('\n')
  
""" end of functions """

file = open("wzone.json")
zone = json.load(file)
json_file = open("counts.json",'w') 

file_length = len(zone)


ca_dict = {"All":0}
co_dict = {"All":0}
wi_dict = {"All":0}
de_dict = {"All":0}
counts = {}

for i in range(file_length):
    wi = zone[i]['widget_class']
    co = zone[i]['color']
    ca = zone[i]['category']
    de = zone[i]['Developer']
    #all categories
    if ca not in ca_dict.keys():
        ca_dict[ca] = 1
    else:
        ca_dict[ca] += 1
    #all colors
    if co not in co_dict.keys():
        co_dict[co] = 1
    else:
        co_dict[co] += 1
    #all widgets
    if wi not in wi_dict.keys():
        wi_dict[wi] = 1
    else:
        wi_dict[wi] += 1

    if de not in de_dict.keys():
        de_dict[de] = 1
    else:
        de_dict[de] += 1
        
    if (ca,co,wi,de) not in counts.keys():
        counts[(ca,co,wi,de)] = 1
    else:
        counts[(ca,co,wi,de)] += 1


""" widget only """

for wi in wi_dict.keys():
    count = 0
    for k,v in counts.items():
        if k[2] == wi:
            count += v
    temp_dict = {"widget_class":wi,"count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"color":"All", "widget_class": wi, "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"category": "All", "widget_class": wi, "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"category":"All", "color":"All", "widget_class": wi, "count":count}
    write_json(json_file,temp_dict)
    
""" color only """

for co in co_dict.keys():
    count = 0
    for k,v in counts.items():
        if k[1] == co:
            count += v
    temp_dict = {"color":co,"count":count}
    write_json(json_file,temp_dict)

    temp_dict = {"color":co, "widget_class": "All", "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"category": "All", "color":co, "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"category":"All", "color":co, "widget_class": "All", "count":count}
    write_json(json_file,temp_dict)
    
""" category only """

for ca in ca_dict.keys():
    count = 0
    for k,v in counts.items():
        if k[0] == ca:
            count += v
    temp_dict = {"category":ca,"count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"category":ca, "color": "All", "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"category":ca, "widget_class": "All", "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"category":ca, "color":"All", "widget_class":"All","count":count}
    write_json(json_file,temp_dict)
    
""" developer only """

for de in de_dict.keys():
    count = 0
    for k,v in counts.items():
        if k[3] == de:
            count += v
    
    temp_dict = {"developer":de,"count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"developer":de, "color": "All", "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"developer":de, "widget_class": "All", "count":count}
    write_json(json_file,temp_dict)
    
    temp_dict = {"developer":de, "color":"All", "widget_class":"All","count":count}
    write_json(json_file,temp_dict)
    
""" color and widget """

for co in co_dict.keys():
    for wi in wi_dict.keys():
        count = 0
        for k,v in counts.items():
            if k[1] == co and k[2] == wi:
                count += v
        temp_dict = {"color":co, "widget_class":wi, "count":count}
        write_json(json_file,temp_dict)
 
        temp_dict = {"category": "All", "color":co, "widget_class":wi, "count":count}
        write_json(json_file,temp_dict)
        
""" category and widget """

for ca in ca_dict.keys():
    for wi in wi_dict.keys():
        count = 0
        for k,v in counts.items():
            if k[0] == ca and k[2] == wi:
                count += v
        temp_dict = {"category":ca, "widget_class":wi, "count":count}
        write_json(json_file,temp_dict)
 
        temp_dict = {"category":ca, "color":"All", "widget_class":wi, "count":count}
        write_json(json_file,temp_dict)
""" category and color """

for ca in ca_dict.keys():
    for co in co_dict.keys():
        count = 0
        for k,v in counts.items():
            if k[0] == ca and k[1] == co:
                count += v
        temp_dict = {"category":ca, "color":co, "count":count}
        write_json(json_file,temp_dict)
        
        temp_dict = {"category":ca, "color":co, "widget_class": "All", "count":count}
        write_json(json_file,temp_dict)


""" category and color and widget """
for ca in ca_dict.keys():
    for co in co_dict.keys():
        for wi in wi_dict.keys():
            count = 0
            for k,v in counts.items():
                if k[0] == ca and k[1] == co and k[2] == wi:
                    count += v
            temp_dict = {"category":ca, "color": co, "widget_class":wi, "count":count}
            write_json(json_file,temp_dict)

        
""" developer and widget """

for de in de_dict.keys():
    for wi in wi_dict.keys():
        count = 0
        for k,v in counts.items():
            if k[3] == de and k[2] == wi:
                count += v
        temp_dict = {"developer":de, "widget_class":wi, "count":count}
        write_json(json_file,temp_dict)
 
        temp_dict = {"developer":de, "color":"All", "widget_class":wi, "count":count}
        write_json(json_file,temp_dict)
        
""" developer and color """

for de in de_dict.keys():
    for co in co_dict.keys():
        count = 0
        for k,v in counts.items():
            if k[3] == de and k[1] == co:
                count += v
        temp_dict = {"developer":de, "color":co, "count":count}
        write_json(json_file,temp_dict)
        
        temp_dict = {"developer":de, "color":co, "widget_class": "All", "count":count}
        write_json(json_file,temp_dict)

""" developer and color and widget """
for de in de_dict.keys():
    for co in co_dict.keys():
        for wi in wi_dict.keys():
            count = 0
            for k,v in counts.items():
                if k[3] == de and k[1] == co and k[2] == wi:
                    count += v
            temp_dict = {"developer":de, "color": co, "widget_class":wi, "count":count}
            write_json(json_file,temp_dict)
            
            
""" ALL parts """
temp_dict = {"widget_class":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"color":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"category":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"developer":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"category":"All", "widget_class":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"category":"All", "color":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"developer":"All", "widget_class":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"developer":"All", "color":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"color":"All", "widget_class":"All","count":file_length}
write_json(json_file,temp_dict)

temp_dict = {"category":"All", "color":"All", "widget_class":"All","count":file_length}
write_json(json_file,temp_dict)


temp_dict = {"developer":"All", "color":"All", "widget_class":"All","count":file_length}
write_json(json_file,temp_dict)
        


file.close()       
json_file.close()