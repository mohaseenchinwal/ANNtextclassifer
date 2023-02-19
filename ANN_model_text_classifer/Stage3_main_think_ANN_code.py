#!/usr/bin/env python
# coding: utf-8

# ## Neural Network

# all imports

# In[1]:


# use natural language toolkit
import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime
stemmer = LancasterStemmer()


# loading data set

# In[26]:


training_data = []
import pandas as pd
folder_path='/root/ML/project/'
file_path='trainclassfication.csv'
data=pd.read_csv(folder_path + file_path)
data = data[pd.notnull(data['tokenized_source'])]
data=data[data.Category != 'None']
for index,row in data.iterrows():
    training_data.append({"class":row["Category"], "sentence":row["tokenized_source"]})


# Check number of statements

# In[3]:


print ("%s sentences of training data" % len(training_data))


# Dividing data as array of unique stemmed words

# In[4]:


words = []
classes = []
documents = []
ignore_words = ['?']
# loop through each sentence in our training data
for pattern in training_data:
    # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

# remove duplicates
classes = list(set(classes))

print (len(documents), "documents")
print (len(classes), "classes", classes)
#print (len(words), "unique stemmed words", words)


# In[29]:


with open(folder_path+'words.txt','w') as thefile:
    for item in words:
        thefile.write("%s\n" % item)
with open(folder_path+'classes.txt','w') as thefile:
    for item in classes:
        thefile.write("%s\n" % item)


# geting list of unique words and classes

# In[5]:


# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

print ("# words", len(words))
print ("# classes", len(classes))


# sample of data

# In[6]:


# # sample training/output
i = 0
w = documents[i][0]
print ([stemmer.stem(word.lower()) for word in w])
print (training[i])
print (output[i])
documents[0]
len(training)
output[0]


# some functions needed to implement nueral network

# In[7]:


import numpy as np
import time

# compute sigmoid nonlinearity
def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

# convert output of sigmoid function to its derivative
def sigmoid_output_to_derivative(output):
    return output*(1-output)
 
def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def think(sentence, show_details=True):
    x = bow(sentence.lower(), words, show_details)
    if show_details:
        print ("sentence:", sentence, "\n bow:", x)
    # input layer is our bag of words
    l0 = x
    # matrix multiplication of input and hidden layer
    l1 = sigmoid(np.dot(l0, synapse_0))
    # output layer
    l2 = sigmoid(np.dot(l1, synapse_1))
    return l2


# Function to train data 

# In[8]:


def train(X, y, hidden_neurons=10, alpha=1, epochs=50000, dropout=False, dropout_percent=0.5):

    print ("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else '') )
    print ("Input matrix: %sx%s    Output matrix: %sx%s" % (len(X),len(X[0]),1, len(classes)) )
    np.random.seed(1)

    last_mean_error = 1
    # randomly initialize our weights with mean 0
    synapse_0 = 2*np.random.random((len(X[0]), hidden_neurons)) - 1
    synapse_1 = 2*np.random.random((hidden_neurons, len(classes))) - 1

    prev_synapse_0_weight_update = np.zeros_like(synapse_0)
    prev_synapse_1_weight_update = np.zeros_like(synapse_1)

    synapse_0_direction_count = np.zeros_like(synapse_0)
    synapse_1_direction_count = np.zeros_like(synapse_1)
        
    for j in iter(range(epochs+1)):

        # Feed forward through layers 0, 1, and 2
        layer_0 = X
        layer_1 = sigmoid(np.dot(layer_0, synapse_0))
                
        if(dropout):
            layer_1 *= np.random.binomial([np.ones((len(X),hidden_neurons))],1-dropout_percent)[0] * (1.0/(1-dropout_percent))

        layer_2 = sigmoid(np.dot(layer_1, synapse_1))

        # how much did we miss the target value?
        layer_2_error = y - layer_2

        if (j% 10000) == 0 and j > 5000:
            # if this 10k iteration's error is greater than the last iteration, break out
            if np.mean(np.abs(layer_2_error)) < last_mean_error:
                print ("delta after "+str(j)+" iterations:" + str(np.mean(np.abs(layer_2_error))) )
                last_mean_error = np.mean(np.abs(layer_2_error))
            else:
                print ("break:", np.mean(np.abs(layer_2_error)), ">", last_mean_error )
                break
                
        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        layer_2_delta = layer_2_error * sigmoid_output_to_derivative(layer_2)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        layer_1_error = layer_2_delta.dot(synapse_1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
        
        synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
        synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))
        
        if(j > 0):
            synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0)+0) - ((prev_synapse_0_weight_update > 0) + 0))
            synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0)+0) - ((prev_synapse_1_weight_update > 0) + 0))        
        
        synapse_1 += alpha * synapse_1_weight_update
        synapse_0 += alpha * synapse_0_weight_update
        
        prev_synapse_0_weight_update = synapse_0_weight_update
        prev_synapse_1_weight_update = synapse_1_weight_update

    now = datetime.datetime.now()

    # persist synapses
    synapse = {'synapse0': synapse_0.tolist(), 'synapse1': synapse_1.tolist(),
               'datetime': now.strftime("%Y-%m-%d %H:%M"),
               'words': words,
               'classes': classes
              }
    synapse_file = "synapses.json"

    with open(folder_path+synapse_file, 'w') as outfile:
        json.dump(synapse, outfile, indent=4, sort_keys=True)
    print ("saved synapses to:", synapse_file)


# to convert list to array and train main function

# In[9]:


X = np.array(training)
y = np.array(output)

start_time = time.time()

train(X, y, hidden_neurons=10, alpha=0.1, epochs=50000, dropout=False, dropout_percent=0.2)

elapsed_time = time.time() - start_time
print ("processing time:", elapsed_time, "seconds")


# To predict and classify

# In[10]:


# probability threshold
ERROR_THRESHOLD = 0.2
# load our calculated synapse values
synapse_file = 'synapses.json' 
with open(synapse_file) as data_file: 
    synapse = json.load(data_file) 
    synapse_0 = np.asarray(synapse['synapse0']) 
    synapse_1 = np.asarray(synapse['synapse1'])

def classify(sentence, show_details=False):
    results = think(sentence, show_details)

    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD ] 
    results.sort(key=lambda x: x[1], reverse=True) 
    return_results =[[classes[r[0]],r[1]] for r in results]
    #print ("\n classification: %s" % ( return_results))
    return return_results


# Some examples

# In[16]:


classify("  Rework BGA Reball Made Easy Simple and easy to use ! Datum FG Framed Stencils Fixtures Carriers, Pressfit, Router, Wave, & Custom Ministencils Multilevel (Stepdown) Durostone Electropolish Stencils Stencil Types Flexframe Datum PhD Inspection Overlay PrintPart Fixture for Rework Ideal for replacement of micro devices Printpart Fixtures Knowledge Products Technology Fixtures Support Pin Plate Custom Fixtures Router Prototype EpoCoat Stencils Terms of Use PressFit Connector Dies Precision milled SS clad aluminum dies for pressfit SMT Stencil Thickness UV cured nanocoating Area Ratio Calculator Multilevel Stencils Support Pin Locating Plates (SPin) Easy to use template for locating support pins Pressfit Fixtures Area Ratio Report ScanCAD BGA Reballing Fixtures Contact SMT Carriers Stencil + Fixture Rework ReBalling Fixture, PrintPart, Ministencils & more HAAS Nano Coat Stencils Stencils Framed, Frameless or Proto Mini-Stencils for Printing Solder Paste BGA, connectors, LGA, QFN, etc. Stencils About Us B O O T S L o g i n Submit Dear valued customer Welcome to our new website It will be the new gateway for BOOTS On top right hand side of the page are your login boxes Please use your username and password and the site will take you to BOOTS Note that we are also updating BOOTS to be compatible with the latest server OS and this will be launched shortly Thank you for your cooperation Knowledge Ordering Stencil Types SMT Stencil Thickness Providing Data Why Us Stencil Fixture Info Bank Area Ratio Report Area Ratio Calculator App Info Technology Equipment LPKF G6080 Electropolish Stencils ScanCAD HAAS Services EpoCoat Stencils Electropolish Stencils Nano Coat Stencils Multilevel Stepdown UV cured nanocoating Materials Datum PhD Datum FG Durostone Tension Stencils Products Stencils Framed Stencils Frameless Stencils Prototype Multilevel Stencils Fixtures SMT Carriers Router Pressfit Fixtures Wave Solder Fixtures Custom Fixtures Rework Ministencils BGA Reballing Fixtures Printpart Fixtures Nozzles Other Flexframe Inspection Overlay Support Pin Plate About Us Beam On Technology Corporation was established in October 1992 founded by manufacturing engineers with extensive knowledge and expertise in the assembly process Our founding mission was to provide integrated service products to the SMT assembly industry engineered for ease of use that both increase yields and reduce defects This continues to be our goal Since the introduction of our first revolutionary product "" Band Etch Technology(tm) for Stencils "" we are constantly introducing new products that respond to changes in technology By working closely with our customers in product development we can go the "" extra mile "" to meet their needs Our Family of Service Products include Solder Paste Stencils...Our proprietary Band Etch Technology(tm) and laser cut stencils Multi Step stencils Our PrintPart System which is used to print directly on component contacts Rework mini stencils Inspection Template Overlay SPin Plate Support Pin Locator Plate Surface Mount Transport Plates Selective and Non Selective Wave Solder Pallets Press Fit Fixtures Printed Circuit Board Stiffeners Metal Squeegee Blades and Blade Assemblies Ball Grid Array BGA re ball fixtures Box Build Assembly Aids Photo Plotting All of our fixtures and other assembly aids are directly designed from Gerber data assuring accuracy that meets or exceeds all tolerances required for your specific SMT assembly process Beam On Technology boasts not one but two of the best Stencil Laser systems from LPKF With their high Aperture cutting speed combined with state of the art fiber optic cutting technology no other stencil Vendor can service you like we can Everything we make is designed beyond the door meaning our products perform better since they are created for use and not just a commodity for us to sell to people We take pride in what we do so any problems our customers have affect us personally We are a responsible company and treat our customers with respect and confidentiality All data sent to us resides on our own in house servers Our ITAR certification gives you piece of mind that data received by us will be kept confidential and secure We primarily accept Gerber data but can work with most types of files including AutoCAD and ODB Mission Statement It is our business to provide our customer with cost effective products without compromising our commitment to quality We consider our customer our primary concern We strive for reliable on time delivery We dedicate ourselves to perpetual technical innovations and product improvements Stencils Framed Frameless or Proto Fixtures Carriers Pressfit Router Wave Custom Rework ReBalling Fixture PrintPart Ministencils more Technical knowledge Sensibly Applied Home About Us Contact Terms of Use Privacy Policy Restrictions Disclaimers 2014 Beam On Technology Next Day Stencils Free Shipping Beam On offers a variety of family of services and products Stencils Fixtures EpoCoat Flex Frame Rework more EpoCoat Stencils Flex Frame Fixtures")


# In[12]:


classify("  LA36400 Shopping Cart DH361R My Wishlist DE364R DE361R DE362R FVK363R ITAP363 FVK362R AC364RG Sell Your Electrical We Purchase >> Blog BOS14351 FA36100 Disconnect ADS36200HDFP DH362R ITAP362 Log In FVK361R My Account DE365R BOS14353 BOS14352 DE363R Close FA36030 Send Request Circuit Breakers AC365RG PPE Equipment Download Company Brochure >> BOS14355 ITAP361 Switchboards Help KA36200 About Us JavaScript seems to be disabled in your browser You must have JavaScript enabled in your browser to utilize the functionality of this website Help Shopping Cart 0 00 You have no items in your shopping cart My Account My Wishlist My Cart My Quote Log In BD Electrical Worldwide Supply Remanufacturing the past SUSTAINING THE FUTURE Hours and Location Michigan Howell 8 5 EST 800 548 7904 Home Bus Duct Bus Plugs Switchboards Circuit Breakers PPE Equipment Transformers Disconnect Bus Duct Bus Plugs Switchboards Circuit Breakers PPE Equipment Transformers Disconnect Home >> About Us About Us BD Electrical established in 1992 supplies a complete array of used and surplus electrical distribution equipment Today specializing in used and surplus bus duct bus plugs we offer one of the most complete inventories of O E M equipment such as Square D Siemens Westinghouse and General Electric products We also carry several other types of equipment including transformers switchgear circuit breakers panel boards safety disconnects and fuses Our reconditioning process is safety oriented and second to no one It includes performance testing which meets or exceeds O E M standards backed by our two year limited warranty Our goal is simple Customer satisfaction through repeat business We ve earned our reputation with reliable competitively priced products and fast courteous service Give us a call and experience first hand that commitment to quality Browse Bus Duct Bus Plugs Switchboards Circuit Breakers PPE Equipment Transformers Disconnect Navigation Home About Us Contact Us Blog Contact Information Michigan Howell 8 5 EST 800 548 7904 Products ABD408 4 BDP304 BDP306 CP2308G ADS36200HDFP FA36030 FA36100 KA36200 LA36400 AC363RG AC364RG AC365RG BOS14351 BOS14352 BOS14353 BOS14354 BOS14355 DE361R DE362R DE363R DE364R DE365R DH361R DH362R DH363R FVK361R FVK362R FVK363R FVK364R FVK365RT ITAP361 ITAP362 ITAP363 (c) 2013 BD Electrical All rights reserved video title video content BD Electrical established in 1992 supplies a complete array of used refurbished and surplus electrical distribution equipment Call 800 548 7904 Used Busway Siemens ITE Breakers Square D Bus Plugs Panel Boards Transformers bd electrical bus plugs bus duct used surplus equipment westinghouse ge electric circuit breaker switchgear ite panel boards bd electrical michigan bd electrical worldwide supply electrical supply bd electrical howell")


# In[13]:


classify("  Products & Solutions University Sponsorships Defense White Papers MiniMax Find a local contact Disposable Marine & Underwater   Twitter http://www.sensor-test.de Medical AluLite High-speed data: MiniMax with Ethernet and 20m/24h IP68 Pharma Railway News Brass   Oil & Gas Products Fischer Rugged Flash Drive SolarStratos Terms of Use Imprint LP360   Facebook Nuclear Food Catalogues Fischer Core Series News & Events Accessories Pharmaceutical People New microsite, video and brochure on Fischer Connectors' medical connectivity solutions Extreme Energy Videos World Map & Locations Military website Subscribe now Contact Us Electronica 2016 Fischer MiniMax(tm) Series Medical website Cookies Policy Tools Twiice Ask our engineers Events Fischer Freedom(tm) Series Breakthrough connectivity offers EASY mating, cleaning and integration Book an appointment Robonation Balt Military Expo Login Industrial CAD 3D Files About us Skip to main content Login Global Global UK US Switzerland EN Switzerland DE Switzerland FR France Italy Spain LATAM Japan Germany Microsite Military website Medical website Home Products Connectors Overview Fischer Core Series Brass Stainless Steel AluLite Plastic Disposable Broadcast Fischer UltiMate(tm) Series UltiMate Rugged Flash Drive Fischer FiberOptic Series FiberOptic Fischer MiniMax(tm) Series MiniMax Rugged Flash Drive Fischer Freedom(tm) Series LP360 Fischer Rugged Flash Drive Cable Assemblies Custom Solutions Accessories Tools Applications Automotive Broadcast Defense Energy Extreme Food Industrial Instrumentation Marine Underwater Medical Nuclear Oil Gas Pharma Railway Robotics Unmanned Vehicles Security Transportation Vacuum Technical Downloads Hot Topics Catalogues Technical Specifications Technical Drawings User Instructions CAD 3D Files White Papers Infographics Case Studies Videos News Events News Events DSEI 2017 Electronica 2016 Press Room About us History Our Commitment People Products Solutions Planet Quality Certifications Partnerships Sponsorships SolarStratos Twiice Robonation University Sponsorships Jobs Careers Contact us Contact Us World Map Locations Terms of Use Privacy Policy Cookies Policy Sales Terms Conditions Imprint Sitemap About us History Our Commitment People Products Solutions Planet Quality Certifications Partnerships Sponsorships SolarStratos Twiice Robonation University Sponsorships Jobs Careers Fischer Connectors has been designing manufacturing and distributing high performance connectors and cable assembly solutions for 60 years Our connectors are known for their reliability precision and resistance to demanding and harsh environments Fischer Connectors ' products are commonly used in fields requiring faultless quality such as medical equipment industrial instrumentation measuring and testing devices broadcast telecommunication and military forces Primary design and manufacturing facilities are located in Saint Prex Switzerland with eight subsidiaries and many distributors located worldwide History Almost 60 years ago Walter Werner Fischer developed the first sealed push pull connector Since then our company has evolved into a state of the art developer and manufacturer of circular connectors Learn more    Values Our values serve as a compass for our actions to deliver the highest quality standards and answer your needs Learn more   Jobs Careers Fischer Connectors offers job opportunities around the world in modern and dynamic environments where teamwork is essential Learn more    Quality Environment Fischer Connectors is committed to quality and respect of the environment throughout every phase of the company s operations Learn more    Home Products Connectors Overview Fischer Core Series Brass Stainless Steel AluLite Plastic Disposable Broadcast Fischer UltiMate(tm) Series UltiMate Rugged Flash Drive Fischer FiberOptic Series FiberOptic Fischer MiniMax(tm) Series MiniMax Rugged Flash Drive Fischer Freedom(tm) Series LP360 Fischer Rugged Flash Drive Cable Assemblies Custom Solutions Accessories Tools Applications Automotive Broadcast Defense Energy Extreme Food Industrial Instrumentation Marine Underwater Medical Nuclear Oil Gas Pharma Railway Robotics Unmanned Vehicles Security Transportation Vacuum Technical Downloads Hot Topics Catalogues Technical Specifications Technical Drawings User Instructions CAD 3D Files White Papers Infographics Case Studies Videos News Events News Events DSEI 2017 Electronica 2016 Press Room About us History Our Commitment People Products Solutions Planet Quality Certifications Partnerships Sponsorships SolarStratos Twiice Robonation University Sponsorships Jobs Careers Contact us Contact Us World Map Locations Terms of Use Privacy Policy Cookies Policy Sales Terms Conditions Imprint Sitemap Copyright (c) 2018 Fischer Connectors SA All rights reserved Fischer Connectors manufactures high performance push pull circular connectors and cable assemblies Check our range of connectors and cable solutions now")


# In[19]:


classify("  New Website Testimonial Policies Parts Catalog Contact Support Forum Documentation Themes WordPress Blog Products Spindle Parts Latest News Kennard Parts Suggest Ideas Legal/Disclaimers WordPress Planet News About CDT Home Latest News Testimonial Products Parts Catalog About CDT History Staff Policies Centrum Legal Disclaimers Contact About CDT Custom Drilling Technologies established in 1990 has been providing superior customer service to the printed circuit board industry for almost 20 years We specialize in Excellon Drilling and Routing Equipment Parts and Service Our staff has over sixty years of combined experience in the design building troubleshooting operation programming and process control relating to these machines We offer a wide variety of solutions for practically all manufacturing requirements along with free one on one customer technical support There is no job too big or too small Contact us with your needs we ' ll be there to help Recent Posts New Website Archives December 2011 Categories News Recent Posts New Website Blog Categories News 1 Blogroll Documentation Plugins Suggest Ideas Support Forum Themes WordPress Blog WordPress Planet About Us Custom Drilling Technologies offers superior service in rebuilding Excellon machines on site service calls test and evaluation of parts trouble shooting problems and finding solutions to your needs Detailed information about the services we offer and how Custom Drilling Technologies can help you are below (c) 2008 Custom Drilling ")


# Some more examples: 

# In[17]:


#data=pd.read_csv('C:/Users/trainees/Desktop/AllData/data/Classificationtabletest.csv')
#data = data[pd.notnull(data['tokenized_source'])]
#data=data[data.Category != 'None']
#data.shape


# In[18]:


#for index,row in data.iterrows():
#    x1=classify(row["tokenized_source"])
#    print(row["url"],x1)

