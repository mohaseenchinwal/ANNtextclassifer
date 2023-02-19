



import pandas as pd



#cols = [0, 1, 2, 3, 4, 5, 6, 7]


data=pd.read_csv('Classificationtable.csv', delimiter=',', names = ['Id (primary)', 'url_id', 'url', 'tokenized_source', 'Class_1', 'Class_2', 'Total_matches', 'Category'])

#data=pd.read_csv('Classificationtable.csv')

#print(data)




#data=pd.read_csv('Classificationtable.csv')





# creating bool series True for NaN values 
data[pd.notnull(data["Category"])] 
data=data[data.Category != 'None']  

# filtering data 
# displayind data only with team = NaN 
#a=data[bool] 

#print (bool)
print(data)
