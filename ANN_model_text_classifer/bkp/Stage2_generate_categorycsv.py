
import pandas as pd



cols = [0, 1, 2, 3]


data=pd.read_csv('chk.csv', delimiter=',', names = ['Id (primary)', 'url_id', 'url', 'tokenized_source'])



Path_for_csv_for_classification='/root/ML/project/chk.csv' 
df=pd.read_csv(Path_for_csv_for_classification)
a=df.tail()
print(a)




from flashtext.keyword import KeywordProcessor
kp0=KeywordProcessor()
kp1=KeywordProcessor()
kp2=KeywordProcessor()




Class_1_keywords = ['Office', 'Services', 'Products', 'OFFICE', 'Company', 'official', 'products', 'licensed', 'PARTNERS', 'PRIVACY & TERMS', 'Suppliers', 'SERVICES', 'Shopping', 'sellers', 'Shop', 'business', 'creditcard', 'Marketing', 'Packages', 'enterprises', 'solution',
 'Business','Seller', 'businesses', 'supply', 'Sale', 'sell', 'Sell', 'OFFERS', 'Offers', 'offers', 'Offer', 'product', 'Sellers', 'distributor' ,'Career', 'COMPANY', 'Solutions', 'SERVICES', 'Privacy Policy Terms of Use', 'Privacy', 'Policy' ,'Terms', 'Protection des marques EN c Nameshield Gestion des noms de domaine Cybersecurite', 'applab', 'profit', 'startup', 'partners' ]
Class_2_keywords = ['Access denied', 'Server Error', 'website is under construction', 'domainmonster', 'Marcaria.com', 'Routedge', 'Instra', 'OnlyDomains', '403 Forbidden error', 'scheduled maintenance', 'International Trademark Registration International Domain Registration New gTLDs', 'Index of', 'cgi bin', 'cgi-bin', 'College', 'University', 'Ministry', 'Ministry of Interior Qatar', 'Ministry of Interior', 'Hukoomi', 'Education', 'Gandi', 'Contact your hosting provider', 'Plesk', 'Hosting' ,'w3infotech', 'Buy this domain Privacy Policy', 'Domain Portfolio Weitere Domains gunstig registrieren Neue Domain Endungen vorbestellen Impressum Datenschutzerklarung', 'Arts', 'Dance', 'travel', 'sports', 'games', 'culture', 'music']
keywords=Class_1_keywords + Class_2_keywords




from flashtext.keyword import KeywordProcessor

kp0=KeywordProcessor()

for word in keywords:
    kp0.add_keyword(word)


kp1=KeywordProcessor()
for word in Class_1_keywords:
    kp1.add_keyword(word)


kp2=KeywordProcessor()
for word in Class_2_keywords:
    kp2.add_keyword(word)



def percentage1(dum0,dumx):
    try:
        ans=float(dumx)/float(dum0)
        ans=ans*100
    except:
           return 0
    else:
         return ans




df["Class_1"]=0.0
df["Class_2"]=0.0
df["Total_matches"]=0
df["Category"]=''



for index,row in df.iterrows():
    x=str(row[3])
    y0=len(kp0.extract_keywords(x))
    y1=len(kp1.extract_keywords(x))
    y2=len(kp2.extract_keywords(x))
    df["Total_matches"][index]=y0   
    df["Class_1"][index]=float(percentage1(y0,y1))
    df["Class_2"][index]=float(percentage1(y0,y2))
    if y0==0:
        df["Category"][index]='None'
    else:
        if y1>=y2:
            df["Category"][index]='Class_1'
        elif y2>=y1:
            df["Category"][index]='Class_2'

folder_path='/root/ML/project/'
file_path='Classificationtablelastest.csv'
df.to_csv(folder_path+file_path)
