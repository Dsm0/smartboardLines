import regex as re
from bs4 import *
import subprocess
import regex as re
import unicodedata
import urllib
import urllib.request
import os
from pyfiglet import print_figlet,figlet_format
import json
import sys
from colored import colored
from tiv import print_image
import time


def delay_print(s,speed):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(speed)
    print("")

rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)

rubiconURL = "http://www.rubiconline.com"
categories = ["news","opinion","sports","feature","ae"]
# print(categories)
global pages
pages = {}

# def grabImages(images):
#     for cat in categories:
#         path = "/images/" + cat
#         for j in enumerate(images):
#             filename = path + "/" + str(j[0]) + ".jpeg"
#             urllib.urlretrieve(j[1], filename)

def get_pages():
    for cat in categories:
        print("getting: " + cat)
        response = urllib.request.urlopen("http://www.rubiconline.com/category/" + cat + "/")
        page_source = response.read() # generate each page source to be read
        page_source = page_source.decode("utf-8")
        soupedUp = BeautifulSoup(page_source,'html.parser') #generate each parsed page
        storyLinks = soupedUp.find_all('a',attrs={'rel': "bookmark"})
        storyLinks = [j['href'] for j in storyLinks]
        stories = soupedUp.find_all('img')
        headlines = [j['alt'] for j in stories] # removed: .encode('ascii', 'ignore')
        headlines = headlines[4:-3]
        images = [j['src'] for j in stories] # removed: .encode('ascii', 'ignore')
        images = images[4:-3]
        page = [(headlines[i],images[i],storyLinks[i]) for i in range(len(headlines))] # first 4 are always rubicon titles
        pages[cat] = page
    writeInfo()

def display(category, storyNum):
    story = pages[category][storyNum]
    headline = story[0]
    image = story[1]
    filename = "images/" + category + "/" + str(storyNum) + ".jpg"
    # print(image)
    # print(filename)
    urllib.request.urlretrieve(image, filename)
    settings = " -w " + str(columns*-0.21)
    cmd = "tiv -0 " + filename + settings
    # out = subprocess.run( cmd, stdout=subprocess.PIPE,shell=True)
    # print(colored(str(out)))
    # out = str(out).encode('ansi256')
    # sys.stdout.write(out)
    # print(out)
    # img = print_image(filename,width=columns,aspect_ratio=1)
    # print(img.encode('utf-8'))
    # delay_print(print_image(filename,width=columns,aspect_ratio=1))
    # out = os.popen(cmd).readlines()
    # os.system(cmd)
    delay_print(figlet_format(headline,"colossal",width = columns),0.001)
    delay_print(print_image(filename,width=columns),0.00001)
    # subprocess.run(cmd, shell=True)
    print((story[2]*2 + "\n")*7)

def inciteGetPages():
    if(os.path.exists("stories.txt") == False):
        get_pages()
        writeInfo()
    else:
        pages = readInfo()

# as requested in comment
def writeInfo():
    with open('stories.txt', 'w') as file:
        file.write(json.dumps(pages)) # use `json.loads` to do the reverse
# as requested in comment
def readInfo():
    with open('stories.txt', 'r') as file:
        pagesJSON = file.read()
        # print(pagesJSON)
        global pages
        pages = json.loads(pagesJSON) # use `json.loads` to do the reverse
        return(pages)

def argForceLoad():
    for arg in sys.argv[1:]:
        if(arg == '-fs'):
            get_pages()

if __name__ == '__main__':
    argForceLoad()
    inciteGetPages()
    display('opinion',6)

"""headlines only have class <p>, and nothing else"""
