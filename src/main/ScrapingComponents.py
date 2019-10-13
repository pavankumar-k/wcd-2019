'''
Created on Feb 3, 2018

@author: pavan kumar k
'''
'''
This file contains the reusable components for the scraping
'''
import time
import re
import os
import json

class Ingredients:
    def __init__(self,_driver):
        self.driver = _driver
        
    ####Method to scroll down a page till end of the page
    def scrollPageDown(self):
        SCROLL_PAUSE_TIME = 0.5
    
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
    
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
    
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    #This method is for getting the outputfolder path  
    @staticmethod
    def getOutputFilesPath():
        tem = os.getcwd()
        print('command',tem)
        lis = re.split('src',tem)
        path = lis[0]+'src'+'/output/'
        print(path)
        return path
    
    @staticmethod
    def writeDictListToJsonLines(filename,items):
        file = open(Ingredients.getOutputFilesPath()+filename,'a+')
        for item in items:
            file.write(json.dumps(dict(item))+'\n')
        file.close()
        
    #This method is to write to output file with seperators s1 = '|^|' , s2 = '|!|'
    @staticmethod
    def writeTofileWithSeperators(filename,lis):
        fields = ''
        with open(Ingredients.getOutputFilesPath()+filename,'a+',encoding = 'utf-8') as file:
            for row in lis:
                fields += '|^|'+row
            file.write(fields+'|!|\n')

    #this method is to write a single entry into the file
    @staticmethod
    def writeToFile(filename,url):
        with open(Ingredients.getOutputFilesPath()+filename,'a+',encoding = 'utf-8') as file:
            file.write(url+'\n')
    

    #this method is to write a list of links into the file
    @staticmethod
    def writeListToFile(filename,urls):
        with open(Ingredients.getOutputFilesPath()+filename,'a+',encoding = 'utf-8') as file:
            for url in urls:
                file.write(url+'\n')