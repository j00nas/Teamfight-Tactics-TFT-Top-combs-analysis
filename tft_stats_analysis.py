#!/usr/bin/env python
# coding: utf-8

# In[308]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.max_columns = None


# In[309]:


df = pd.read_csv('tft-data-top100EUW-last20games.csv')


# In[310]:


df.head()


# Since i got the data from lolchess.gg, i only got informations of the date in the type of "2 days ago", "1 week ago" and so on. So the date is only an approximation.

# In[311]:


df = df.loc[:, (df != 0).any(axis=0)]


# In[312]:


df.head()


# In[313]:


df.info()


# In[314]:


df.describe()


# In[315]:


date_count = pd.DataFrame(df['date'].value_counts()).sort_index(ascending = False).reset_index().rename(columns={'index': 'Date', 'date': 'Count'})
date_count


# I will concentrate the analysis on the last 7 days.

# In[316]:


df = df[df['date'] >= '2020-12-03']


# In[317]:


tdf = df[df['Placement'] <= 8]  #Look at the traits of all placements
tdf.head()


# In[318]:


ptdf = tdf.iloc[:, 4:]


# In[319]:


# Start with two highest number of traits

ptdf = ptdf[ptdf.apply(lambda row: row >= row.nlargest(2)[-1],axis=1)]

ptdf.head()


# In[320]:


combinations = ptdf.notna().dot(ptdf.columns+' + ').str.rstrip(' +')


# In[321]:


df_test1 = pd.concat([tdf.iloc[:, :4], pd.DataFrame(combinations)], axis=1).rename(columns = {0: 'comb'}) 
df_test1.head()


# In[322]:


pd.set_option('display.max_rows', None)


# In[323]:


count_combs = pd.DataFrame(df_test1['comb'].value_counts()).reset_index().rename(columns={'index': 'comb', 'comb': 'Count'})
count_combs


# In[324]:


df_test1 = df_test1[['comb', 'Placement']].groupby('comb').mean().reset_index()
df_test1


# In[325]:


df_test1 = pd.merge(df_test1, count_combs, on=['comb'])


# In[326]:


df_test1.sort_values(by = 'Placement').reset_index(drop = True)


# In[337]:


# Mean Placement of the top 15 often played combs (combs := the two second highest traits, only TOP4)

sorted_df_test1 = df_test1[df_test1['Count'] >= df_test1.nlargest(15, 'Count').iloc[-1]['Count']].sort_values(by = 'Placement')
sorted_df_test1 = sorted_df_test1.rename(columns = {'Placement': 'MeanPlacement', 'comb': 'Comb'})
sorted_df_test1


# In[341]:


sorted_df_test1['Count'].sum()


# In[338]:


for i, v in enumerate(sorted_df_test1['Comb']):
    print(i, v)


# In[339]:


sns.set(font_scale = 1.4)
plt.figure(figsize=(6, 8))

#plt.xlim((0, 6))  
sns.barplot(y = 'Comb', x = 'MeanPlacement', data = sorted_df_test1, color = '#5BA4B4')
plt.xlabel('Placement (mean)')
plt.ylabel('')

plt.title('Mean Placement of the 15 often played combs\n', fontdict = {'fontsize': 20})

for i, v in enumerate(sorted_df_test1['MeanPlacement']):
    plt.text(v - .36, i + .2, str(round(v,1)), color='white')

# Data Info \n\n(combs := highest two traits,\ndata: Last 20 Games of 100 TOP Players in EUW)\n


# Database and calculation: The database contains the last 20 games of the Top 100 EUW players. It considers only games that are not older than 7 days. "Combs" means the traits with the first and second highest number. N = 708 Games. Often played comb = Adept + Divine (168). Least played comb Dusk + Vanguard (21). 

# In[ ]:




