'''
Created on Feb 4, 2018

@author: pavan

This class is a client file where everything for soup is written
'''
import os
import re
import nltk
from nltk.tag import StanfordNERTagger
from geotext import GeoText


class ClientSoup:
    def __init__(self):
        nltkpath = '/home/pavan/nltk_data/taggers/stanford-ner'
        self.st = StanfordNERTagger(nltkpath + '/classifiers/english.all.3class.distsim.crf.ser.gz',
                                    nltkpath + '/stanford-ner.jar')

    def isAuthLine(self, text):
        count = 0
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = self.st.tag(tokens)
            #print("AuthTags:", tags)
            for tag in tags:
                if tag[1] == 'PERSON':
                    count += 1
        return count > 0

    def isLocation(self, text):
        place = GeoText(text)
        count = 0
        for a in ['introduction','background',':']:
            if a in text.lower():
                raise Exception('Unable to categorise')
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.tokenize.word_tokenize(sent)
            tags = self.st.tag(tokens)
            #print("affliTags:", tags)
            for tag in tags:
                if tag[1] in ['ORGANIZATION', 'LOCATION']:
                    count += 1

        if count > 0:
            return True
        return False

    def isTitle(self, text):
        count = 0
        total = 0
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.tokenize.word_tokenize(sent)
            validtok = []
            for a in tokens:
                if re.search("[A-Za-z]", a):
                    validtok.append(a)
            total += len(validtok)
            #print('tokens', validtok)
            for a in validtok:
                if "." in a or len(a)==1:
                    continue
                flag = True
                for b in re.findall("[A-Za-z]", a):
                    if b.islower():
                        flag = False
                        break
                if flag:
                    count += 1
        #print("titletags", total, count)
        if (total == 1 and count == total):
            return True
        if (count / total) * 100 >= 80:
            return True
        return False

    def extractText(self, lis, link):

        dict = {"ses": lis[0],'link':link}
        #print('ses', dict)
        title = ""
        i = 1
        while i < len(lis):
            if not self.isTitle(lis[i]):
                break
            title += lis[i]
            i += 1
        #print('Title-', title)
        dict['title'] = title
        auth = ''
        while i < len(lis):
            line = lis[i]
            # re.sub("\([0-9]+\)","",lis[i])
            # isauth = isAuthLine(line)
            isloc = self.isLocation(line)
            #print(line, isloc)
            if isloc:
                break
            auth += lis[i]
            i += 1
        dict['auth'] = auth
        if auth == '':
            raise Exception('Unable to extract')
        inds = re.findall("\([0-9]+\)", auth)
        maxind = 0
        for a in inds:
            num = int(a.replace("(", "").replace(")", ""))
            if maxind < num:
                maxind = num
        #print('test1', num)
        affli = ''
        while i < len(lis):
            affli += lis[i]
            i += 1
            if "(" + str(maxind) + ")" in lis[i - 1]:
                break

        dict['affli'] = affli
        #print("Affli-", affli)
        dict['text'] = "\n".join(lis[i:])
        return [dict]

    def extractText1(self, lis):
        dict = {"ses": lis[0]}
        #print('ses', dict)
        title = ""
        i = 1
        while i < len(lis):
            if not self.isTitle(lis[i]):
                break
            title += lis[i]
            i += 1
        print('Title-', title)
        dict['title'] = title
        auth = ''
        while i < len(lis):
            if ',' in lis[i] or ":" in lis[i]:
                break
            auth += lis[i]
            i += 1
        dict['auth'] = auth
        print('AUTH-',auth)
        if auth == '':
            raise Exception('Unable to extract')
        inds = re.findall("\([0-9]+\)", auth)
        maxind = 0
        for a in inds:
            num = int(a.replace("(", "").replace(")", ""))
            if maxind < num:
                maxind = num
        #print('test1', num)
        affli = ''
        while i < len(lis):
            affli += lis[i]
            i += 1
            if "(" + str(maxind) + ")" in lis[i - 1]:
                break
        print('affli-',affli)
        dict['affli'] = affli
        input('-----------------------------')
        dict['text'] = "\n".join(lis[i:])
        return [dict]
