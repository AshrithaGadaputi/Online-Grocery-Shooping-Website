#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.metrics import mean_squared_log_error,mean_squared_error, r2_score,mean_absolute_error 
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import pymongo
from pymongo import MongoClient
import pickle


# In[139]:


def init_connection():
    return MongoClient("mongodb://localhost:27017")


# In[140]:


client=init_connection()


# In[151]:


def get_data():
    db=client.filtering
    items=list(db.items.find({}))
    return items


# In[152]:


data = get_data()


# In[154]:


l = []
i = 0
for item in data:
    l.append(data[i])
    print(data[i])
    i = i + 1


# In[157]:


df = pd.DataFrame(l)


# In[160]:


df.columns


# In[161]:


df = df.drop('_id',axis = 1)


# In[162]:


df.head()


# from random import randint, choice
# import random

# n = 3
# k = randint(0, 1)
# for i in range (1, n+1):
#     for j in range (1, n+1):
#         print (((i*j)/(i*j)*k) , end = ' ')
#     print ()

# n = 50
# df = pd.DataFrame([[random.randint(0, 1) for _ in range(n)] for _ in range(n)])

# df = df.iloc[:,0:27]

# df = pd.read_csv('Filtering_Dataset.csv')

# In[163]:


df.columns = ['Apple','Maggi','Bingo','Toothpaste','Lays','Soaps','Dolo 650','Doritos','Moong Dal','Aloo Bhujia','Banana','Cup Noodles','Pens','Pencils','Stapler','Stick File','Notebooks','Kurkure','Cofsils','Cold Tablets','Orange','Vicks','Sanitary Pads','Kiwi','Shampoo','Cough Syrup','Detergent']


# In[164]:


l = []
for i in range(0,df.shape[0]):
    l.append('User_'+str(i))

df.index = l


# In[165]:


df.describe()


# ### Method 1

# In[169]:


for i in df.columns:
    df[i] = df[i].astype('int32')


# In[172]:


def standardize(row):
    new_row = (row - row.mean()) / (row.max() - row.min())
    return new_row

df_std = df.apply(standardize)
df_std


# In[173]:


fruits = ['Apple','Orange','Banana','Kiwi']
snacks = ['Lays','Kurkure','Bingo','Doritos','Moong Dal','Aloo Bhujia','Maggi','Cup Noodles']
stationary = ['Pens','Pencils','Stick File','Stapler','Notebooks']
medicine = ['Dolo 650','Cofsils','Cough Syrup','Cold Tablets','Vicks']
hygiene = ['Soaps','Toothpaste','Shampoo','Detergent','Sanitary Pads']


# In[174]:


df.head()


# In[175]:


df.loc['User_0','Apple']


# In[176]:


# Visualizing the number of fruits being bought by each user
plt.figure(figsize = (10,10))
l = []

for user in range(0,df.shape[0]):
    s = 0
    for i in fruits:
        s = s + df.loc['User_'+str(user),i]
    l.append(s)

plt.bar(df.index,l)
plt.xticks(rotation=90)
plt.xlabel('User')
plt.ylabel('Count')
plt.title('Number Of Fruit Items Bought By Each User')
plt.show()


# In[177]:


# Visualizing the number of snacks being bought by each user
plt.figure(figsize = (10,10))
l = []

for user in range(0,df.shape[0]):
    s = 0
    for i in snacks:
        s = s + df.loc['User_'+str(user),i]
    l.append(s)

plt.bar(df.index,l)
plt.xticks(rotation=90)
plt.xlabel('User')
plt.ylabel('Count')
plt.title('Number Of Snack Items Bought By Each User')
plt.show()


# In[178]:


# Visualizing the number of medicine items being bought by each user
plt.figure(figsize = (10,10))
l = []

for user in range(0,df.shape[0]):
    s = 0
    for i in medicine:
        s = s + df.loc['User_'+str(user),i]
    l.append(s)

plt.bar(df.index,l)
plt.xticks(rotation=90)
plt.xlabel('User')
plt.ylabel('Count')
plt.title('Number Of Medicine Items Bought By Each User')
plt.show()


# In[179]:


# Visualizing the number of stationary items being bought by each user
plt.figure(figsize = (10,10))
l = []

for user in range(0,df.shape[0]):
    s = 0
    for i in stationary:
        s = s + df.loc['User_'+str(user),i]
    l.append(s)

plt.bar(df.index,l)
plt.xticks(rotation=90)
plt.xlabel('User')
plt.ylabel('Count')
plt.title('Number Of Stationary Items Bought By Each User')
plt.show()


# In[180]:


# Visualizing the number of hygiene items being bought by each user
plt.figure(figsize = (10,10))
l = []

for user in range(0,df.shape[0]):
    s = 0
    for i in hygiene:
        s = s + df.loc['User_'+str(user),i]
    l.append(s)

plt.bar(df.index,l)
plt.xticks(rotation=90)
plt.xlabel('User')
plt.ylabel('Count')
plt.title('Number Of Hygiene Items Bought By Each User')
plt.show()


# In[181]:


item_similarity = cosine_similarity(df_std.T)


# In[182]:


print(item_similarity)


# In[183]:


item_similarity_df = pd.DataFrame(item_similarity,index = df.columns, columns = df.columns)


# In[184]:


item_similarity_df


# In[185]:


def get_similar_items(item_name,user_bought):
    similar_score = item_similarity_df[item_name]*user_bought
    similar_score = similar_score.sort_values(ascending = False)
    
    return similar_score

print(get_similar_items("Apple",1))


# In[186]:


items_wanted = [("Apple",1),("Doritos",1),("Kurkure",1)]

similar_items = pd.DataFrame()

for item,bought in items_wanted:
    similar_items = similar_items.append(get_similar_items(item,bought), ignore_index = True)

similar_items.head()
similar_items.sum().sort_values(ascending = False)


# In[ ]:





# In[ ]:





# In[ ]:




