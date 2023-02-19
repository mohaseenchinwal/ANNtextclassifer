
import re
import csv
import requests
import bs4
import html2text
import sys
import string
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse
from unidecode import unidecode
from copyrightextractor import htmlextractor
import sys
import os
import pyap
from html_to_etree import parse_html_bytes
import requests




# Open the file with read only permit
f = open('com.txt')

# use readline() to read the first line
line = f.readline()

# use the read line to read further.
# If the file is not empty keep reading one line
# at a time, till the file is empty

exclude = set(string.punctuation)

while line:
    # in python 2+
    # print line
    # in python 3 print is a builtin function, so
    page = requests.get(line.rstrip(), verify=False, allow_redirects=True)
    html_code = page.content
    #print(line)
    #print (html_code)
    #print(line)
    # use realine() to read next line
    #line = f.readline()
      
    #from bs4 import BeautifulSoup
    #try:
    #    soup = BeautifulSoup(html_code, 'html.parser')  #Parse html code
    #    texts = soup.findAll(text=True)                 #find all text
    #    text_from_html=' '.join(texts)  
    #    text_from_html1=unidecode(str(text_from_html))
    #    print (text_from_html1)
    #except Exception as e:
    #    print(e)

    #t1=text_from_html(html_code)
    #t2=tag_visible(t1)
    #print(t2)

    def text_from_html(body):
        soup = bs4.BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, bs4.element.Comment):
           return False
        return True
    def remove_non_ascii(text):
        return unidecode(str(text))
    def remove_punc(text1):
        z=''
        for ch in text1:
            if ch in exclude:
                z+=' '
            else:
                z=z+ch
        return z

    def a_dict_from_html(body2):
        a_dict={}
        soup2 = bs4.BeautifulSoup(body2, 'html.parser')
        try:
            for tag in soup2.find_all('a', href=True):
                a_dict[str(tag.get_text().strip())]=str(tag['href'])    
        except:
            return a_dict 
        else:
            return a_dict

    def saveinstring(dict1):
       string2=''
       for tag_text,tag_link in dict1.items():
           string2=string2+" "+tag_text
       return string2
   
    def isLineEmpty(line):
     return len(line.strip()) == 0
     
    print(line.rstrip())
    t1=text_from_html(html_code)
    t2=a_dict_from_html(html_code)
    t3=saveinstring(t2)
    t4=remove_non_ascii(t3)
    t5=remove_punc(t4)
    #print(t5)
    #print(t5.strip('\n')+"_"+line, end="")
    t6=re.sub('\n+',' ',t5.strip())
    t7=re.sub(' +',' ',t6.strip())
    print (t7)
    



    line = f.readline()







