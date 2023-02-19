import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
stemmer = LancasterStemmer()


import pandas as pd


cols = [0, 1, 2, 3]


data=pd.read_csv('Tokenizationtabletest.csv', delimiter=',', names = ['Id (primary)', 'url_id', 'url', 'tokenized_source'])


#data=data[pd.notnull(data['Category'])]
#b=data[data.Category!= 'None']
#data[a]


data=data[pd.notnull(data['tokenized_source'])]
data=data[data.tokenized_source != "None"]

	
y=data.to_dict()
print ("\nDic data\n")
print (y)



series = pd.Series(y)

print ("\nseries data\n")
print (series)




#print(a)
#print(data[data.Category !='Class_1 commercial'])


print ("\ndataframe\n")
print (data)




#print (data['Category'])




for index,row in data.items():
    series.append({"class":row[2], "sentence":row[3]})
