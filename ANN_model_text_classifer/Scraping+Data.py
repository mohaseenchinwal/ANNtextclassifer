#!/usr/bin/env python
# coding: utf-8

# # Sraping Data For Tokenization

# All imports

# In[1]:


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


# Initialization of different arrays

# In[2]:


h = html2text.HTML2Text()
h.ignore_links = True
exclude = set(string.punctuation)
about_us_words=['About us','about','about us', 'About','about_us','about-us','About-us','About-us']
contact_us_words=['Contact','contact','Contact Us','Contact us','contact','contact us', 'contact','contact_us','contact-us','Contact-us','Contact_us']


# to disable prints for some functions

# In[3]:


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout


# To remove non ascii elements

# In[4]:


def remove_non_ascii(text):
    return unidecode(str(text))


# To select only visible tags in document

# In[5]:


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, bs4.element.Comment):
        return False
    return True


# to extract whole text from html used in finding information in about us page

# In[6]:


def text_from_html(body):
    soup = bs4.BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)


# to extract meta tag from html

# In[7]:


def meta_from_html(body1):
    str1=''
    soup1 = bs4.BeautifulSoup(body1, 'html.parser')
    for tag in soup1.find_all('meta'):
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
            str1=str1+tag.attrs['content']+" "
    return str1    


# to remove punctuation from text so wont hinder in tokenizing

# In[8]:


def remove_punc(text1):
    z=''
    for ch in text1:
        if ch in exclude:
            z+=' '
        else:
            z=z+ch
    return z


# to create a dictionary of anchor tags i.e. its navigation name and link used for finding about us link

# In[9]:


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


# to validate the about us link

# In[10]:


def uri_validator1(x):
    try:
        result = urlparse(x)
        if result.scheme!="" or result.netloc!="" or result.path[0]=="/" or result.path[-3:]=="php" or result.path[-4:]=="html" or result.path[-3:]=="asp":
            return 1
        else:
            return 0
        #return result.scheme and result.netloc and result.path
    except:
        return 0


# to convert relative to absolute address of about us link

# In[11]:


def url_corrector(url3,relative):
    x=urlparse(relative)
    newurl=""
    if x.scheme=="" or x.netloc=="":
        if relative[0]=="/":
            newurl=url3+relative
        else :
            newurl=url3+"/"+relative
    else:
        newurl=relative
    return newurl


# to extract about us data from link

# In[12]:


def aboutusscraper(About_us_link1,url4):
    try:
        page1 = requests.get(About_us_link1)
        try:
            x=text_from_html(page1.content)
        except:
            x=h.handle(page1.content)
            x=x.replace("*"," ")
            x=x.replace("\n"," ")
        x=remove_punc(x)
        list_of_words=word_tokenize(x)
        text1=' '.join(list_of_words)
        text1=" "+text1
        text1=remove_non_ascii(text1)
        return text1
    except:
        print("About_us_link Broken for ",About_us_link1," for website: ",url4)
        return " "


# to extract contact us data from link

# In[13]:


def contactusscraper(contact_us_link2,url5):
    list_of_link_dummy=['','','','','','','']
    list_of_address_dummy=['','','']
    list_of_phone_dummy=['','','']
    list_of_email_dummy=['','','']
    ctr_1=0
    ctr_2=0
    ctr_3=0
    regex_email=re.compile(r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''')
    phonePattern = re.compile(r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})''', re.VERBOSE)
    try:
        page1 = requests.get(contact_us_link2)
        try:
            x=text_from_html(page1.content)
        except:
            x=h.handle(page1.content)
            x=x.replace("*"," ")
            x=x.replace("\n"," ")
        text_for_email=remove_non_ascii(x)
        x=remove_punc(x)
        list_of_words=word_tokenize(x)
        text1=' '.join(list_of_words)
        text1=" "+text1
        list_of_link_dummy=get_social_links(page1.content,page1.headers.get('content-type'))
        text1=remove_non_ascii(text1)
        phonenumbers=phonePattern.findall(str(text1))
        for phn in  phonenumbers:
            list_of_phone_dummy[ctr_1]=str(phn)
            ctr_1+=1
            if ctr_1 > 2:
                break
        addresses = pyap.parse(str(text1),country='US')
        addresses+=pyap.parse(str(text1), country='CA')
        for address in addresses:
            list_of_address_dummy[ctr_2]=str(address)
            ctr_2+=1
            if ctr_2 > 2:
                break
        emails=re.findall(regex_email,text_for_email)
        for email in emails:
            #print(email)
            list_of_email_dummy[ctr_3]=str(email)
            ctr_3+=1
            if ctr_3 > 2:
                break
        return text1, list_of_address_dummy, list_of_phone_dummy, list_of_email_dummy, list_of_link_dummy
    except Exception as e:
        #print(e)
        print("Contact_us_link Broken for ",contact_us_link2," for website: ",url5)
        return "", list_of_address_dummy, list_of_phone_dummy, list_of_email_dummy, list_of_link_dummy


# to save elements of dict of Anchor tags into a string

# In[14]:


def saveinstring(dict1):
    string2=''
    for tag_text,tag_link in dict1.items():
        string2=string2+" "+tag_text
    return string2


# to find about us link from navigation text

# In[15]:


def findaboutuslink(dict1,url2):
    About_us_link1=''
    for tag_text,tag_link in dict1.items():
        if any(word in tag_text for word in about_us_words):
            if uri_validator1(str(tag_link))==True:
                About_us_link1=url_corrector(url2,tag_link)
                break
    return About_us_link1


# to find contact us link from navigation text

# In[16]:


def findcontactuslink(dict1,url1):
    Contact_us_link1=''
    for tag_text,tag_link in dict1.items():
        #print(tag_text)
        if any(word in tag_text for word in contact_us_words):
            if uri_validator1(str(tag_link))==True:
                Contact_us_link1=url_corrector(url1,tag_link)
                break
    #print(Contact_us_link1)
    return Contact_us_link1


# To find social links

# In[17]:


from __future__ import unicode_literals
import re

import six
PREFIX = r'https?://(?:www\.)?'
SITES = ['twitter.com/', 'youtube.com/',
         '(?:[a-z]{2}\.)?linkedin.com/',
         'github.com/', '(?:[a-z]{2}-[a-z]{2}\.)?facebook.com/', 'fb.co',
         'plus\.google.com/', 'pinterest.com/', 'instagram.com/',
         'snapchat.com/', 'flipboard.com/', 'flickr.com',
         'google.com/+', 'weibo.com/', 'periscope.tv/',
         'telegram.me/', 'soundcloud.com', 'feeds.feedburner.com',
         'vimeo.com', 'slideshare.net', 'vkontakte.ru']
BETWEEN = ['user/', 'add/', 'pages/', '#!/', 'photos/',
           'u/0/']
ACCOUNT = r'[\w\+_@\.\-/%]+'
PATTERN = (
    r'%s(?:%s)(?:%s)?%s' %
    (PREFIX, '|'.join(SITES), '|'.join(BETWEEN), ACCOUNT))
SOCIAL_REX = re.compile(PATTERN, flags=re.I)
BLACKLIST_RE = re.compile(
    """
    sharer.php|
    /photos/.*\d{6,}|
    google.com/(?:ads/|
                  analytics$|
                  chrome$|
                  intl/|
                  maps/|
                  policies/|
                  search$
               )|
    instagram.com/p/|
    /share\?|
    /status/|
    /hashtag/|
    home\?status=|
    twitter.com/intent/|
    twitter.com/share|
    search\?|
    /search/|
    pinterest.com/pin/create/|
    vimeo.com/\d+$|
    /watch\?""",
    flags=re.VERBOSE)
def matches_string(string):
    """ check if a given string matches known social media url patterns """
    return SOCIAL_REX.match(string) and not BLACKLIST_RE.search(string)
def find_links_tree(tree):
    """
    find social media links/handles given an lxml etree.
    TODO:
    - `<fb:like href="http://www.facebook.com/elDiarioEs"`
    - `<g:plusone href="http://widgetsplus.com/"></g:plusone>`
    - <a class="reference external" href="https://twitter.com/intent/follow?screen_name=NASA">
    """
    for link in tree.xpath('//*[@href or @data-href]'):
        href = link.get('href') or link.get('data-href')
        if (href and
                isinstance(href, (six.string_types, six.text_type)) and
                matches_string(href)):
            yield href

    for script in tree.xpath('//script[not(@src)]/text()'):
        for match in SOCIAL_REX.findall(script):
            if not BLACKLIST_RE.search(match):
                yield match

    for script in tree.xpath('//meta[contains(@name, "twitter:")]'):
        name = script.get('name')
        if name in ('twitter:site', 'twitter:creator'):
            # FIXME: track fact that source is twitter
            yield script.get('content')
def get_from_url(body,headers_content):  # pragma: no cover
    """ get list of social media links/handles given a url """
    
    tree = parse_html_bytes(body, headers_content)

    return set(find_links_tree(tree))
def initialize_dict_social(dict1):
    dict1["facebook_link"]=''
    dict1["facebook_id"]=''
    dict1["twitter_link"]=''
    dict1["twitter_id"]=''
    dict1["youtube_link"]=''
    dict1["youtube_id"]=''
    dict1["linkedin_link"]=''
    return dict1


# to find list of social links

# In[18]:


def get_social_links(body,headers_content):
    set_of_links=get_from_url(body,headers_content)
    list1=list(set_of_links)
    strface="facebook.com"
    strtwit="twitter.com"
    stryou=".youtube.com"
    strlin="linkedin.com"
    dict_soc={}
    dict_soc=initialize_dict_social(dict_soc)
    for str1 in list1:
        if strface in str1:
            dict_soc["facebook_link"]=str1
            dict_soc["facebook_id"]=str1.split(strface+"/",1)[1]
            #print("facebook : ",str1.split(strface+"/",1)[1])
        if strtwit in str1:
            dict_soc["twitter_link"]=str1
            dict_soc["twitter_id"]=str1.split(strtwit+"/",1)[1]
            #print("twitter : ",str1.split(strtwit+"/",1)[1])
        if stryou in str1:
            dict_soc["youtube_link"]=str1
            dict_soc["youtube_link"]=str1.split(stryou+"/",1)[1]
            #print("youtube : ",str1.split(stryou+"/",1)[1])
        if strlin in str1:
            dict_soc["linkedin_link"]=str1
            #print("linkedin : ",str1.split(strlin+"/",1)[1])
    listnew=[dict_soc["facebook_link"],dict_soc["facebook_id"],dict_soc["twitter_link"],dict_soc["twitter_id"],dict_soc["youtube_link"],dict_soc["youtube_link"],dict_soc["linkedin_link"]]
    return listnew


# Main funtion to scrape and save elements into files
# 

# In[20]:


def ScrapeAndSave(url,
                  SrNo,
                  id_for_table_1,
                  newFileWriter1,
                  newFileWritercopyright1,
                  newFileWritercontact1,
                  newFileWriterabout1,
                  newFileWriterfinal1):
    url="https://www."+url
    final_data_array=[id_for_table_1,SrNo,url]
    final_file_data_array=[id_for_table_1,SrNo,url]
    copyright_data_array=[id_for_table_1,SrNo,url]
    contactus_data_array=[id_for_table_1,SrNo,url]
    aboutus_data_array=[id_for_table_1,SrNo,url]
    list_of_links=[]
    try:
        page = requests.get(url)
        #page.content=remove_non_ascii(page.content)
        About_us_link='' 
        string1=''
        copyright=''
        abouttext=''
        contacttext=''
        Contact_us_link=''
        with HiddenPrints():
            copyright = htmlextractor.extract(page.content)
            copyright=remove_non_ascii(copyright)
        copyright_data_array.append(copyright)
        try:
            dict_a=a_dict_from_html(page.content)
#             for tag_text,tag_link in dict_a.items():
#                 string1=string1+" "+tag_text
            string1=string1+" "+saveinstring(dict_a)
#                 if any(word in tag_text for word in about_us_words):
#                     if uri_validator1(str(tag_link))==True:
#                         About_us_link=url_corrector(url,tag_link)
#                         break
            About_us_link=findaboutuslink(dict_a,url)
            Contact_us_link=findcontactuslink(dict_a,url)
            #print(string1)
            if About_us_link!='':
                abouttext=aboutusscraper(About_us_link,url)
                string1=string1+abouttext
            if Contact_us_link!='':
                contacttext,address_,phone_,email_,link_=contactusscraper(Contact_us_link,url)
                final_file_data_array=final_file_data_array+address_+phone_+email_+link_
            aboutus_data_array.append(abouttext)
            contactus_data_array.append(contacttext)
            
        except Exception as e1:
            #final_data_array.append(string1)
            print("Error in trying AboutUs or ContactUs info")
            
        try:
            x=meta_from_html(page.content)
        except:
            final_data_array.append(string1)
        else:
            x=remove_punc(x)
            list_of_words=word_tokenize(x)
            text=' '.join(list_of_words) 
            string1=string1+" "+text
            string1=remove_non_ascii(string1)
            final_data_array.append(string1)
           
    except Exception as e:
        print("Connection refused for Sr. No : "+str(SrNo))
        newFileWritercopyright1.writerow(copyright_data_array)
        newFileWriter1.writerow(final_data_array)
        newFileWritercontact1.writerow(contactus_data_array)
        newFileWriterabout1.writerow(aboutus_data_array)
        newFileWriterfinal1.writerow(final_file_data_array)
        #print(e)
        return 0
    else:
        print("Done for Sr. No : "+str(SrNo))
        newFileWritercopyright1.writerow(copyright_data_array)
        newFileWriter1.writerow(final_data_array)
        newFileWritercontact1.writerow(contactus_data_array)
        newFileWriterabout1.writerow(aboutus_data_array)
        newFileWriterfinal1.writerow(final_file_data_array)
        return 1


# selects url from file with its id

# In[21]:


urls=[]
IDs=[]
countforheader=0
with open('C:/Users/trainees/Desktop/urls.csv','r') as userFile:
    userFileReader = csv.reader(userFile)
    for row in userFileReader:
        countforheader+=1
        if countforheader==1:
            continue
        IDs.append(row[0])
        urls.append(row[1])


# loop to scrape data

# In[22]:


z=0
folder_path='C:/Users/trainees/Desktop/AllData/data1/'
id_for_table=0
Table_for_tokenization='Tokenizationtable.csv'
Table_for_copyright='Copyright.csv'
Table_for_contact_us='ContactUs.csv'
Table_for_about_us='AboutUs.csv'
Table_for_finalfile='FinalFile.csv'
with open(folder_path + Table_for_tokenization , 'a',newline='') as newFile:
    newFileWriterMain = csv.writer(newFile,delimiter=",")
    with open(folder_path + Table_for_copyright , 'a',newline='') as newFileCopy:
        newFileWritercopyright = csv.writer(newFileCopy,delimiter=",")
        with open(folder_path + Table_for_contact_us , 'a',newline='') as newFilecontact:
            newFileWritercontact = csv.writer(newFilecontact,delimiter=",")
            with open(folder_path + Table_for_about_us , 'a',newline='') as newFileabout:
                newFileWriterabout = csv.writer(newFileabout,delimiter=",")
                with open(folder_path + Table_for_finalfile , 'a',newline='') as newFileFinal:
                    newFileWriterfinal = csv.writer(newFileFinal,delimiter="|")
                    for i in range(len(urls)):
                        id_for_table+=1
                        out=ScrapeAndSave(urls[i],IDs[i],id_for_table,newFileWriterMain,newFileWritercopyright,newFileWritercontact,newFileWriterabout,newFileWriterfinal)
                        z+=out
                        if z==15:
                            break


# In[ ]:





# In[ ]:




