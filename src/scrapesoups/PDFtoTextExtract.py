'''
Created on Feb 4, 2018

@author: Pavan Kumar K
'''


from src.main.ScrapingComponents import Ingredients
from src.scrapesoups.ClientSoup import ClientSoup
from selenium import webdriver
import time
import pdfbox
import threading
import os
import json_lines
######################---- Chrome settings---- ##################3
driverpath = "/usr/lib/chromium-browser/chromedriver"
downloadsFolder = '/home/pavan/Downloads/wcdlbpdfsabs'
prefs = {"plugins.always_open_pdf_externally": True, "download.default_directory":downloadsFolder}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs",prefs)

'''
driver = webdriver.Chrome(executable_path=driverpath, chrome_options=chromeOptions)
addurls = []
with json_lines.open(Ingredients.getOutputFilesPath()+'abslinks.jl') as f:
    for item in f:
        addurls.append(item['url'])

for url in addurls:
    driver.get(url)
'''
######
p = pdfbox.PDFBox()
i=0
comp = []
for fname in os.listdir(downloadsFolder):
    if fname.endswith(".txt"):
        name = fname.replace(".txt",".pdf")
        comp.append(name)

print(comp)
for fname in os.listdir(downloadsFolder):
    if fname.endswith(".pdf") and (fname not in comp):
        print(i, fname)
        p.extract_text(downloadsFolder+"/"+fname)
        i+=1
print("Completed")
