#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:47:52 2018

@author: pavan
"""
from src.main.ScrapingComponents import Ingredients
import sys
import json
import json_lines
import pandas as pd
#from geotext import GeoText
from pandas import ExcelWriter
import re

#to find the locations
'''
def isloc(loc):
    place = GeoText(loc)
    if len(place.cities)>0:
        return True
    return False
'''

#to split auth and affli
# takes two params authors string and affliation string returns list of dicts with authors and corresponding affliations
def authinfo(authstr,afflistr):
    details = []
    al = re.split('(?<=[0-9])\)(?!=\()', authstr)
    #print(al)
    afl = re.split('(?<=[0-9])\)(?!=\()', afflistr)
    #print(afl)
    if len(afl)>1 and len(al)>1:
        for a in al[:-1]:
            det={}
            nums = re.findall('[0-9]+', a)
            a = re.sub(r'[0-9]+', '', a).replace(',', '')
            det['auth'] = a.split("(")[0].replace('-','').strip()
            det['affli'] = ''
            for n in nums:
                for aff in afl:
                    if n in re.findall(r'[0-9]+', aff):
                        alf = re.sub(r'[0-9]+', '', aff)
                        talf = alf.split("(")[0].replace('-','').strip()
                        det['affli'] +=  talf+ "\n"
            details.append(det)
    else:
        for a in al:
            det = {}
            det['auth'] = a.split("(")[0].replace('-','').strip()
            det['affli'] = afflistr.split("(")[0].replace('-','').strip()
            details.append(det)
    return details


filename = 'output'
records = []

with json_lines.open(Ingredients.getOutputFilesPath()+'wcd2019ltabstracts.jl') as f:
    for item in f:
        records.append(item)

with json_lines.open(Ingredients.getOutputFilesPath()+'wcd2019lterabstracts.jl') as f:
    for item in f:
        records.append(item)

links = []
with json_lines.open(Ingredients.getOutputFilesPath()+'abslblinks.jl') as f:
    for item in f:
        links.append(item)

rows = []
for item in records:
    authlis = item['auth']
    afflis = item['affli']
    link = ''
    check = item['title'].split('\n')[0].strip()
    for a in links:
        if check in a['title']:
            link = a['url']
            break
    item['url'] = link
    item.pop('auth')
    item.pop('affli')
    det = authinfo(authlis,afflis)
    for a in det:
        temp = dict(item)
        temp['auth'] = a['auth']
        temp['affli'] = a['affli']
        rows.append(temp)


df17 = pd.DataFrame(rows, columns=['auth', 'affli','url','title', 'ses','text'])
df17.to_csv(Ingredients.getOutputFilesPath()+'wcd2019latebreakabst.csv')
'''
df17 = df17.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
print(df17.head())
writer = ExcelWriter(Ingredients.getOutputFilesPath()+'WCD2019latebreakabstracts.xlsx')
df17.to_excel(writer, 'Sheet1')
writer.save()
'''
# print(rows)
