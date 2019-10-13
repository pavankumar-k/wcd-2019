'''
Created on Feb 4, 2018

@author: pavan kumar k
this class is for extracting links for the crawl
'''

from src.main.ScrapingComponents import Ingredients
from src.scrapesoups.ClientSoup import ClientSoup
from selenium import webdriver
import time


driverpath = "/usr/lib/chromium-browser/chromedriver"


driver = webdriver.Chrome(driverpath)

#data output for crawl stored here
dataoutput = "output.txt"
#links for which crawls throws error
errlinks = "errlinks.txt"
#Recrawl output form the error links
erroutput = "erroutput.txt"
#links for the crawl (output)
clinks = "clinks.txt" 
#error while getting links
clinkserr = "clinkserr.txt"
clinkserrer = "clinkserrer.txt"

#client = ClientSoup(driver)
####Actual coding start here

#driver.get("https://www.wcd2019milan-dl.org/abstract-book/assets/html/abstracts/01-acne-rosacea-related-disorders.html")

driver.get("https://www.wcd2019milan-dl.org/abstract-book/assets/html/late-breaking-abstracts/01-acne-rosacea-related-disorders.html")

page = 0
for a in range(0,45):
    surls = driver.find_elements_by_css_selector("ol > li > a.flex")
    surls[a].click()
    time.sleep(10)
    page += 1
    dctlis = []
    for b in driver.find_elements_by_css_selector("article a"):
        dct={'url':b.get_attribute('href'),'title':b.text.strip()}
        dctlis.append(dct)
    Ingredients.writeDictListToJsonLines('abslblinks.jl',dctlis)
    #print('LINK   EXTRACTION   SUCCESSFUL:'+str(i+1)+'\n')
    print('PAGE:',page)
print('ALL LINKS EXTRACTION COMPLETED')









