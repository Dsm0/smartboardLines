import rubicon as rub
import queue
import time
import sys
global speed
import random as r
import auto as ft
import os
from pprint import pprint
import requests
import subprocess

# print(help(tiv))


from datetime import datetime
from threading import Timer
fastSpeed = 0.001
slowSpeed = 0.5
rule = r.randint(0,255)
increment = 1

rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)
times = {'autoT' : 0.05, 'storyT':10}
lastLineDict = {'ll':ft.rstart(columns)}


def delay_print(s,sec):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(sec)
    print("")


def parser(cmd):
  global rule
  if(cmd=='auto'):
    lastLine = ft.genStep(lastLineDict['ll'],steprule=rule) # generates a line, using auto.py
    printedLine = [ft.getDict(str(i)) for i in lastLine] # turns 0s and 1s into blank spaces and chars
    lastLineDict['ll'] = lastLine #turn printed line into last line
    delay_print(printedLine,fastSpeed)
  if(cmd=='story'):
    # print("instory")
    rule = r.randint(0,255)
    rub.display(r.choice(rub.categories),r.randint(0,11))
    # rub.display('news',8)


def bylineQ(inc):
    #print("increment::::  " + str(inc))
    if(inc % 100     == 0):
        weather = os.system("curl wttr.in/minneapolis")
        # weather = str(subprocess.run( "curl wttr.in/minneapolis", stdout=subprocess.PIPE,shell=True))
        print(weather)
    if(inc % 100 == 0):
        parser('story')
    else:
        parser('auto')
    return(inc + 1)

def argForceLoad():
    for arg in sys.argv:
        if(arg == '-fs'):
            print("---forced page reload---")
            rub.get_pages()

argForceLoad()
rub.inciteGetPages()
parser('auto')

while(True):
    increment = bylineQ(increment)
