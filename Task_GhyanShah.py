#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing Required Libraries
from selenium import webdriver #This is used to automate web browser
from bs4 import BeautifulSoup #This is used to scrap web data
from bs4.element import Tag #We will use this to search ParseTree using Tag
import time #To set delay
import pandas as pd #To convert extracted HTML data into Data Frame and then convert to csv


# In[2]:


#Initiating browser search
driver = webdriver.Firefox(executable_path="C:\\webdrivers\geckodriver.exe") #My personal choice of Browser is Firefox. Chrome can be used by replacing this line with: driver = webdriver.Chrome(executable_path="C:\\webdrivers\geckodriver.exe")
userinput = input("Enter search keywords:") #User based input for Google Search
google_url = "https://www.google.com/search?q=" + userinput +  "&num=" + str(20) #Parsing the URL.
driver.get(google_url)
time.sleep(5) #We delay this process by 5 seconds to imitate this process like a human process
soup = BeautifulSoup(driver.page_source,'lxml') #Initiation of BeautifulSoup to parse html data
result_div = soup.find_all('div', attrs={'class': 'g'})


# In[3]:


#Declaration of array to store data
Search_Result_URL = [] 
Search_Result_Title = []
Search_Result_Description = []
Appended_Record = []


# In[4]:


#Process of extracting data from source HTML
for r in result_div:
    # This will check is the element is present
    try:
        #Link Extraction
        link = r.find('a', href=True)
        
        #Title Extraction
        title = None
        title = r.find('h3')

        if isinstance(title,Tag):
            title = title.get_text()
            
        #Description Extraction
        description = r.find('span', attrs={'class': 'aCOpRe'})

        if isinstance(description, Tag):
            description = description.get_text()

        #Checking if everything is present and append them into respective array
        if link != '' and title != '' and description != '':
            Search_Result_URL.append(link['href'])
            Search_Result_Title.append(title)
            Search_Result_Description.append(description)
    
    #Returns Exception if element not present and loop continuation
    except Exception as e:
        print(e)
        continue


# In[6]:


#Appending the top 10 extracted data into Appended_Record array
for i in range(10):
    Appended_Record.append((1,Search_Result_Title[i],Search_Result_URL[i],Search_Result_Description[i]))
    
#Prints Record in non tabular form
print(Appended_Record)


# In[8]:


#Converting Extracted data into Data Frame
df = pd.DataFrame(Appended_Record,columns=['Page_Number','Search_Result_Title','Search_Result_URL','Search_Result_Description'])


# In[9]:


df.index.name = 'Search_Result_Number' #Setting a column name for Index
df.index = df.index + 1 #Changing indexing to Base 1


# In[10]:


df.head()


# In[11]:


df.tail()


# In[13]:


#Data Frame conversion to CSV file and exporting it to specified Path
df.to_csv(r'C:\Users\Welcome\Desktop\precily.csv')

