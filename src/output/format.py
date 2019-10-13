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
    al = re.split('(?<=[0-9]), ', authstr)
    afl = re.split('(?<=[0-9]), ', afflistr)
    #print(afl)
    if len(afl)>1 and len(al)>1:
        for a in al:
            det={}
            nums = re.findall('[0-9]+', a)
            a = re.sub(r'[0-9]+', '', a)
            tem = a.split('[')
            print('SPLIT',tem)
            det['auth'] = tem[0].strip()
            if len(tem) >1:
                det['authloc'] = tem[1].replace(']','').strip()
            det['affli'] = ''
            print(det)
            for n in nums:
                for aff in afl:
                    if n in re.findall(r'[0-9]+', aff):
                        alf = re.sub(r'[0-9]+', '', aff)
                        talf = alf.split("(")[0].replace('-','').strip()
                        det['affli'] +=  talf+ "\n"
            details.append(det)
            print(det)
    else:
        for a in al:
            det = {}
            tem = a.split('[')
            print('SPLIT', tem)
            det['auth'] = tem[0].strip()
            if len(tem) > 1:
                det['authloc'] = tem[1].replace(']', '').strip()
            affl = afflistr.split("(")[0].replace('-','').strip()
            det['affli'] = re.sub(r'[0-9]+','',affl).strip()
            details.append(det)
    return details


filename = 'output'
records = []

with json_lines.open(Ingredients.getOutputFilesPath()+'wcd2015test.jl') as f:
    for item in f:
        records.append(item)
rows = []
for item in records:
    print('ITEM:',item)
    item['sestitle'] = item['sestitle'].split("\n[ - ]\n\n")[0].strip()
    if 'title' in item.keys():
        authlis = item['auth']
        afflis = item['aflis']
        if authlis is "":
            rows.append(item)
        else:
            item.pop('auth')
            item.pop('aflis')
            det = authinfo(authlis,afflis)
            for a in det:
                temp = dict(item)
                print('A',a)
                temp['auth'] = a['auth']
                if 'authloc' in a.keys():
                    temp['authloc'] = a['authloc']
                if 'affli' in a.keys():
                    temp['affli'] = a['affli']
                rows.append(temp)
    else:
        rows.append(item)
    #input('----------------------------')
df17 = pd.DataFrame(rows, columns=['auth', 'authloc','affli','title','ptime','ptype','sestitle','stime','loc','text'])
#df17.to_csv(Ingredients.getOutputFilesPath()+'wcd2015.csv')

df17 = df17.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
print(df17.head())
writer = ExcelWriter(Ingredients.getOutputFilesPath()+'WCD2015.xlsx')
df17.to_excel(writer, 'Sheet1')
writer.save()
# print(rows)
