'''
Created on Feb 4, 2018

@author: Pavan Kumar K
'''


from src.main.ScrapingComponents import Ingredients
from src.scrapesoups.ClientSoup import ClientSoup
from selenium import webdriver
import time
import threading
import json
import os
import logging

#time.sleep()
driverpath = "/usr/lib/chromium-browser/chromedriver"
downloadsFolder = '/home/pavan/Downloads/wcdlbpdfs'


fileslist = []
with open(Ingredients.getOutputFilesPath()+'links.txt') as f:
    fileslist = f.readlines()

class Threader(threading.Thread):
    def __init__(self, threadID, name, filenames):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.filenames = filenames
        self.client = ClientSoup()

    def run(self):

        for fname in self.filenames:
            name = fname.replace(".txt",'.pdf')
            for a in fileslist:
                if name in a:
                    link = a
            with open(downloadsFolder + '/' + fname) as file:
                lis = file.readlines()
            #print("\n".join(lis))
            try:
                dictlis = self.client.extractText(lis,link)
                Ingredients.writeDictListToJsonLines('wcd2019latebreak.jl',dictlis)
                print("SUCCESSFUL EXTRACT -FILE:",fname)
            except Exception as e:
                Ingredients.writeListToFile("wcdlberror.txt", [fname])
                print('FAILED TO EXTRACT -FILE:',fname, e)

#############################################threads##################################
files=[]
for fname in os.listdir(downloadsFolder):
    if fname.endswith(".txt"):
        files.append(fname)
print("Total files:",len(files))

threads = []
numthreads = 10
size = (int)(len(files) / numthreads)
for i in range(0, numthreads):
    if numthreads - 1 == i:
        urls = files[size * i:]
    else:
        urls = files[size * i:size * (i + 1)]
    thred = Threader(i + 1, "Thread" + str(i + 1) + ":", urls)
    print('staring Thread:', i+1,len(urls))
    thred.start()
    threads.append(thred)
    time.sleep(10)

for x in threads:
    x.join()

