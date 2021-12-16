#!/usr/bin/env python
# coding: utf-8

# # Scrape reviews from trustpilot

# ### Import modules

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import requests

import time
import re

import pandas as pd
pd.set_option('display.width',800)
pd.set_option('display.max_rows',800)


# ### Parameters

# In[2]:


# Scrape records for a specific company
company = 'T-Mobile'
ur = 'https://www.trustpilot.com/review/www.t-mobile.com'


# ### Initialiaze the WebDriver

# In[3]:


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(ur)


# 
# ### Functions that do the job with the web page

# In[5]:


# Functions that do the job with the web page

def get_txt(_drv, _xp):
    _txt = _drv.find_elements_by_xpath(_xp)
    return _txt

def push_next_button(_drv, _elem):   
    btn_next = _drv.find_element_by_name(_elem)
    btn_next.send_keys(Keys.RETURN)
    time.sleep(1)

# Webpage elements
el_rawtext = '//*[@id="__next"]/div/main/div/div[3]'  # Element that captures raw text (no rating )    
btn1 = 'pagination-button-next'


# ### Questions:
# 
# >1. How to identify quickly the elements that I want?   This is, probably, HTML question. 
# >1.a. Is there a way programmatically list all elements on the page?
# 
# >2. I am looking at the element that captures rating of a review. Cannot find it :(
# 
# >3. My current strategy is:
#     a. Load the page
#     b. Read all text
#     c. Parse the text into reviews where each review has elements:
#         - Name
#         - Location
#         - Date
#         - Title
#         - Body
#         - Rating ??? missing in my implementation
#         
# > Question: 
# >    - Is it better/possible to read each review via element tags? 
# >    - Can each element of a review be accessed via tags, not by text logic?
# 
# 

# In[6]:


# Function that does post-processing of a raw text

def break_review_txt(_txt, n_id = 1):
    # _txt = raw text captured from the page
    # n_id = 
    if type(_txt) == str:                            # If unparsed, split by the caret
        _txt = _txt.split('\n')                      # Parse the text by end of line
        
    # Find separators of reviews
    l_reviews = []                                   # Initialize review separator index
    for ix,t in enumerate(_txt): 
        rr = re.findall(r'\d{1,4} reviews?$',t)      # Split line into 'review' chunks
        if len(rr) > 0:                              
            l_reviews.append(ix)                     # Store indices of review separators
            
    # Now parse review text into its elements:
    
    dct = dict()                                     # Storage for parsed elements
    for i in range(len(l_reviews)-1):                # Loop over indices that separate reviews
        s = l_reviews[i]                             # Start position
        e = l_reviews[i+1]                           # End position
  
        _nme = _txt[s-1]                             # First line                
        _nrv = _txt[s]                               # Second line
        _loc = _txt[s+1]                             # Third line
        _dte = _txt[s+2]                             # Forth line
        _ttl = _txt[s+3]                             # Fifth line
        _bdy = _txt[s+4:e-1]                         # This is a body
        _bdy1 = [x for x in _bdy if x not in ['Share','Advertisement']]           # Some cleanup
        _bdy2 = [x for x in _bdy1 if  len(re.findall('Useful[0-9]?',x))==0]       # Additional cleanup
        dct_inner = dict()                           # Store parsed elements                       
        dct_inner['name'] = _nme
        dct_inner['location'] = _loc
        dct_inner['date'] = _dte
        dct_inner['title'] = _ttl
        dct_inner['body'] = " ".join(_bdy2)
        
        dct[n_id] = dct_inner                       # Index
        n_id += 1                                   # Increment counter
    
    return dct


# In[ ]:





# In[7]:


# Testing commands - block when done
#push_next_button(driver)
#crvs3 = driver.find_elements_by_xpath(xp3)


# In[ ]:





# In[8]:


sel_txt = []                                                # Storage for raw text
tbls = []                                                   # Storage for parsed text

N = 3                                                     # Estimated number of pages to scan through
for i in range(N):
    print(i)
    txt = get_txt(_drv=driver, _xp=el_rawtext)              # Extract text from a page    
    brk = break_review_txt(txt[0].text, n_id = i*1000)      # Parse text, make id unique for returned dict
    tbl = pd.DataFrame.from_dict(brk, orient='index')       # Convert dict into pandas table for further processing
    sel_txt.append(txt)                                     # Store raw text just for debugging purposes
    tbls.append(tbl)                                        # Append a table from each page
    push_next_button(driver, _elem=btn1)                    # Push a button to go to the next page
    


# In[9]:


tbl_out = pd.concat(tbls, axis=0)
tbl_out.reset_index(inplace=True)
tbl_out.head()


# In[ ]:


# Store locally

#ddir = r"~\Documents\T-mobile"   # Replace with local path
#fout = ddir+"\\{}_trustpilot_reviews.xlsx".format(company)
#tbl_out.to_excel(fout, header=True, index=True)

