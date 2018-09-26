# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 12:40:12 2018

@author: Yuyang Wang
"""
import os
import os.path
import re
import  xml.dom.minidom
import json
from PIL import Image
import BestSimilarity
import colorsys
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
#import math

rootdir = "G:\Data\screenshot"   
class_list = ("Chronometer", "CompoundButton","ProgressBar",
              "RadioButton",  "RatingBar", "SeekBar", "Spinner", "Switch", "ToggleButton")
colors = {"Red":[255,0,0],  "Yellow":[225,225,0], "Green": [0,128,0], "Blue":[0,0,255],
          "Cyan":[0,255,255], "Black":[0,0,0], "White": [255,255,255], "Magenta":[255,0,255], "Lime":[50,205,50]}

no = 8187 # the unique id of every screenshot
flag = 0 # control the score
tired = 0 # control loops
ratio_control = 10
dicm = {} # metadata package

""" function list """
def get_ratio(w,h):
    if w > h:
        ratio = w/(h+0.001)
    else:
        ratio = h/(w+0.001)
    return ratio

def get_crop(sizelist, classname, no):
    
    region = im.crop((sizelist[0], sizelist[1], sizelist[2],sizelist[3]))
    region.save("./{}/{}-{}.png".format(classname, classname, no))
    
def get_ocrop(imgsize, src_temp, pic):
    
    region = im.crop((0, 0, imgsize[0],imgsize[1]))
    region.save("./Myscreenshot/{}-{}.png".format(src_temp, pic))
    
def get_list(node):
    
    bounds=node.getAttribute("bounds")
    str = re.split('[,\\[\\]]',bounds)
    
    sizelist = []
    for str_split in str:
        if len(str_split)>0:
            sizelist.append(int(str_split))
            
    return sizelist 

def sim_compare(classname,no):
    temp = 0
    i = 0
    while i <= 10:
        i += 1
        gap = i + temp
        path1 = '{}\{}-{}.png'.format(classname, classname, no)
        if no - gap >= 0: #if compare no >= 0
            path2 = '{}\{}-{}.png'.format(classname, classname, no - gap)
            if os.path.exists(path2):
                diff = BestSimilarity.similary_calculate(path1, path2, 2)
                if diff > 0.98:
                    return 1
            else:
                temp += 1
                i -= 1
        else:
            i = 100
    return 0

def get_dominant_color(image):  
    image = image.convert('RGBA')
    image.thumbnail((200, 200))  
    max_score = 0
    dominant_color = 0
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]    
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)      
        y = (y - 16.0) / (235 - 16) 

        if y > 0.9:
            continue  
        score = (saturation + 0.1) * count     
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    if dominant_color == 0:
        return (0,0,0)
    return dominant_color

def get_color(path):
    cimg = Image.open(path)
    mycolor = get_dominant_color(cimg)
    sum = 100000
    for k,v in colors.items():
        mysum = (mycolor[0] - v[0])*(mycolor[0] - v[0]) + (mycolor[1] - v[1])*(mycolor[1] - v[1]) + (mycolor[2] - v[2])*(mycolor[2] - v[2])
        #mysum = abs(mycolor[0] - v[0]) + abs(mycolor[1] - v[1]) + abs(mycolor[2] - v[2])
        if mysum < sum:
            color = k
            sum = mysum
    return color

def write_json(json_file, name, color, content_desc, coor_from, coor_to, dim, pack, text, classname, appname, downloads, url, src, category, developer):

    temp_dict = {"name":name, "color":color, "content-desc":content_desc, "coordinates":{"from":coor_from,"to":coor_to}, 
                 "dimensions":dim, "package_name":pack, "text":text, "widget_class":classname, 
                 "application_name":appname, "downloads":downloads,"url":url,"src":src,"category":category, "Developer": developer}
    json_str = json.dumps(temp_dict) #turn dict to str
    new_dict = json.loads(json_str) #turn str to json_dict
    json.dump(new_dict,json_file) #write                                  
    json_file.write('\n')
    
def zone_json(json_file, name, color, content_desc, coor_from, coor_to, dim, pack, text, classname, appname, downloads, url, src, category, developer):

    temp_dict = {"name":name, "color":color, "content-desc":content_desc, "coordinates":{"from":coor_from,"to":coor_to}, 
                 "dimensions":dim, "package_name":pack, "text":text, "widget_class":classname, 
                 "application_name":appname, "downloads":downloads,"url":url,"src":src,"category":category, "Developer": developer}
    json_str = json.dumps(temp_dict) #turn dict to str
    new_dict = json.loads(json_str) #turn str to json_dict
    json.dump(new_dict,json_file) #write  
    json_file.write(',')                                
    json_file.write('\n')
    
""" function list end """
json_file = open("widgets.json", 'w')
json_zone = open("wzone.json", 'w')
file = open("meta.json")
meta = json.load(file)

for i in range(len(meta)):    
    package = meta[i]['Url'][46:]
    dicm[package] = i

print("loading finish!")

for root, dirs, files in os.walk(rootdir):
    access_time = 0 # access_time = 0 at first
    index = -1 # the index of the dicm
    dic = {} # the size of each screenshot
    for file in files:    
        if tired > 100: # to control too many loops
            tired = 0
            break
        
        if flag == 1: # to control the score and count
            flag = 0
            break
        
        if os.path.splitext(file)[1] == '.xml':
            pic = os.path.splitext(file)[0]
            
            src_temp = root.split('\\')
            src_temp = src_temp[-3]
            
            xmlfile = os.path.join(root, file)
            pngfile = os.path.join(root, pic+'.png')
            if not os.path.exists(pngfile):
                break
            #print(xmlfile)
            
            dom = xml.dom.minidom.parse(xmlfile) #打开xml文档
            xml_root = dom.documentElement #得到文档元素对象          
            Nodes = xml_root.getElementsByTagName('node')
            
            im = Image.open(pngfile)
            im_size = im.size
            
            if im_size[0] <= 0 or im_size[1] <= 0 or im_size[0] > 3000 or im_size[1] > 3000:
                break
            
            for n in Nodes:

                classname = n.getAttribute("class")
                classname = classname.split('.')[-1]

                pack = n.getAttribute("package")
                
                if pack not in dicm.keys():
                    flag = 1
                    break
                
                if access_time == 0:
                    
                    access_time += 1
                                        
                    index = dicm[pack]
                    count = meta[index]['Instalations']
                    score = meta[index]['Score']['Total']

                    if score < 2 or len(count) < 10:
                        flag = 1
                        break

                if classname in class_list and index != -1: #in class_list:          
                    sizelist = get_list(n)
                    w = sizelist[2] - sizelist[0]  #width of image
                    h = sizelist[3] - sizelist[1]  #height of image
                    
                    if sizelist[0] < 0 or sizelist[1] < 0 or sizelist[2] < 0 or sizelist[3] < 0 or sizelist[2] > 3000 or sizelist[3] > 3000: break
                
                    if w <= 0 or h <= 0 or sizelist[2] >= im_size[0] or sizelist[3] >= im_size[1]:
                        break
                    
                    ratio = get_ratio(w,h) # radio >=1                   
                    
                    if no >= 8188  and ratio <= ratio_control and (w,h) not in dic.values():
                        tired += 1 #get tired
                        get_crop(sizelist, classname, no)
                            
                        if sim_compare(classname,no):
                            os.remove("./{}/{}-{}.png".format(classname, classname, no))
                        else:
                            print("%%%%%%%%%%%%%%%%%%%%%%% {}-{} crop succssful! %%%%%%%%%%%%%%%%%%%%%%%{}".format(classname, no, xmlfile))
                        

                            name = "{}-{}".format(classname, no)
                            color = get_color("./{}/{}-{}.png".format(classname, classname, no))
                            content_desc = ""
                            coor_from = [sizelist[0],sizelist[1]]
                            coor_to = [sizelist[2],sizelist[3]]
                            dim = {"height":h,"width":w}
                            pack = pack
                            text = n.getAttribute("text")
                            classname = classname
                            appname = meta[index]['Name']
                            downloads = count
                            url =  meta[index]['Url']
                            src = "/mnt/UIXML/Myscreenshot/{}-{}.png".format(src_temp,pic)
                            category = meta[index]['Category']
                            developer = meta[index]['Developer']
                            
                            get_ocrop(im_size,src_temp, pic)
                            write_json(json_file, name, color, content_desc, coor_from, coor_to, dim, pack, text, classname, appname, downloads, url, src, category, developer)
                            zone_json(json_zone, name, color, content_desc, coor_from, coor_to, dim, pack, text, classname, appname, downloads, url, src, category, developer)
                            dic[no] = (w,h)
                            no += 1
                            tired = 0
                            
                    elif no == 8187:
                        get_crop(sizelist, classname, no)
                        dic[no] = (w,h)

                        name = "{}-{}".format(classname, no)
                        color = get_color("./{}/{}-{}.png".format(classname, classname, no))
                        content_desc = ""
                        coor_from = [sizelist[0],sizelist[1]]
                        coor_to = [sizelist[2],sizelist[3]]
                        dim = {"height":h,"width":w}
                        pack = pack
                        text = n.getAttribute("text")
                        classname = classname
                        appname = meta[index]['Name']
                        downloads = count
                        url =  meta[index]['Url']
                        src = "/mnt/UIXML/Myscreenshot/{}-{}.png".format(src_temp,pic)
                        category = meta[index]['Category']
                        developer = meta[index]['Developer']
                        
                        no += 1
                        get_ocrop(im_size,src_temp, pic)
                        write_json(json_file, name, color, content_desc, coor_from, coor_to, dim, pack, text, classname, appname, downloads, url, src, category, developer)
                        zone_json(json_zone, name, color, content_desc, coor_from, coor_to, dim, pack, text, classname, appname, downloads, url, src, category, developer)
                        
json_file.close()
json_zone.close()