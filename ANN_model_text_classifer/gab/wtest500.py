import requests




# Open the file with read only permit
f = open('com.txt')

# use readline() to read the first line
line = f.readline()

# use the read line to read further.
# If the file is not empty keep reading one line
# at a time, till the file is empty


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
      
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(html_code, 'html.parser')  #Parse html code
        texts = soup.findAll(text=True)                 #find all text
        text_from_html=' '.join(texts)                   #join all text
        print (text_from_html)
    except Exception as e:
        print(e)

    Class_1_keywords = ['Office', 'Services', 'Products', 'OFFICE', 'Company', 'official', 'products', 'licensed', 'PARTNERS', 'PRIVACY & TERMS', 'Suppliers', 'SERVICES', 'Shopping', 'sellers', 'Shop', 'business', 'creditcard', 'Marketing', 'Packages', 'enterprises', 'solution', 'Business','Seller', 'businesses', 'supply', 'Sale', 'sell', 'Sell', 'OFFERS', 'Offers', 'offers', 'Offer', 'product']
    Class_2_keywords = ['Access denied', 'Server Error', 'website is under construction', 'domainmonster', 'Marcaria.com', 'Routedge', 'Instra', 'OnlyDomains', '403 Forbidden error', 'scheduled maintenance']
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


    def find_class():
        x=str(text_from_html)
        z=line.rstrip()

        y0 = len(kp0.extract_keywords(x))
        y1 = len(kp1.extract_keywords(x))
        y2 = len(kp2.extract_keywords(x))
        Total_matches=y0
        per1 = float(percentage1(y0,y1))
        per2 = float(percentage1(y0,y2))
        if y0==0:
            Category='None'
        else:
            if per1>=per2:
                Category='Class_1 commercial'
            elif per2>=per1:
                Category='Class_2 non-commercial'
        return z,Category,per1,per2

    s1=find_class()
    print (s1)

    line = f.readline()
