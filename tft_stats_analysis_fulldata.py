#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.max_columns = None


# In[3]:


df = pd.read_csv('full_data.csv')


# In[4]:


df.head()


# Since i got the data from lolchess.gg, i only got informations of the date in the type of "2 days ago", "1 week ago" and so on. So the date is only an approximation.

# In[5]:


df = df.loc[:, (df != 0).any(axis=0)]


# In[6]:


df.head()


# In[7]:


df.info()


# In[8]:


df.describe()


# In[9]:


date_count = pd.DataFrame(df['date'].value_counts()).sort_index(ascending = False).reset_index().rename(columns={'index': 'Date', 'date': 'Count'})
date_count


# I will concentrate the analysis on the data since last thursday (2020-12-10)

# In[10]:


df = df[df['date'] >= '2020-12-10']


# In[11]:


tdf = df[df['Placement'] <= 8]  #Look at the traits of all placements
tdf = tdf.reset_index(drop = True)
tdf.head()


# In[12]:


ptdf = tdf.iloc[:, 4:]


# In[13]:


# Start with two highest number of traits

#ptdf = ptdf[ptdf.apply(lambda row: row >= row.nlargest(2)[-1],axis=1)]
ptdf = ptdf[ptdf.apply(lambda row: row >= 1,axis=1)]
ptdf.head()


# In[14]:


combinations = ptdf.notna().dot(ptdf.columns+' + ').str.rstrip(' +')


# In[15]:


nr_combs = []

for count, i in enumerate(ptdf.values):
    clear_list = []
    current_traits = combinations.iloc[count].split(' + ')
    count2 = 0
    for j in i:
        #print(j)
        if j > 0:
            clear_list.append(current_traits[count2] + ' (' + str(int(j)) + ')')
            clear_list.sort(key = lambda x: int(x.split('(')[1][-2]), reverse = True)
            count2 += 1
    nr_combs.append(' + '.join(clear_list))      


# In[16]:


pd.DataFrame(nr_combs)


# In[17]:


df_test1 = pd.concat([tdf.iloc[:, :4], pd.DataFrame(nr_combs)], axis=1).rename(columns = {0: 'comb'}) 
df_test1.head()


# In[18]:


pd.set_option('display.max_rows', None)


# In[19]:


count_combs_top1 = pd.DataFrame(df_test1[df_test1['Placement'] == 1]['comb'].value_counts()).reset_index().rename(columns={'index': 'comb', 'comb': 'Count_top1'})


# In[20]:


count_combs_top1


# In[21]:


count_combs_top4 = pd.DataFrame(df_test1[df_test1['Placement'] <= 4]['comb'].value_counts()).reset_index().rename(columns={'index': 'comb', 'comb': 'Count_top4'})


# In[22]:


count_combs_top4


# In[23]:


count_combs = pd.DataFrame(df_test1['comb'].value_counts()).reset_index().rename(columns={'index': 'comb', 'comb': 'Count'})
count_combs


# In[24]:


counts_merge = pd.merge(count_combs, count_combs_top1, how='left', on=['comb'])
counts_merge = pd.merge(counts_merge, count_combs_top4,  how='left', on=['comb'])


# In[25]:


counts_merge = counts_merge.replace({np.nan: 0})


# In[26]:


counts_merge['Winrate'] = counts_merge['Count_top1']/counts_merge['Count']
counts_merge['TOP4%'] = counts_merge['Count_top4']/counts_merge['Count']


# In[27]:


counts_merge


# In[28]:


df_test1 = df_test1[['comb', 'Placement']].groupby('comb').mean().reset_index()


# In[29]:


df_test1 = pd.merge(df_test1, counts_merge, on=['comb'])


# In[30]:


df_test1.sort_values(by = 'Placement').reset_index(drop = True)


# In[42]:


# Mean Placement of the top 25 often played combs (combs := the two second highest traits, only TOP4)
pd.options.display.max_colwidth = 150
sorted_df_test1 = df_test1[df_test1['Count'] >= df_test1.nlargest(25, 'Count').iloc[-1]['Count']].sort_values(by = 'Placement')
sorted_df_test1 = sorted_df_test1.rename(columns = {'Placement': 'Avg. Placement', 'comb': 'Combination', 'Count': 'Count (Games)'})
sorted_df_test1 = sorted_df_test1.reset_index(drop = True).round(2)
sorted_df_test1 = sorted_df_test1[['Combination', 'Avg. Placement', 'Count (Games)', 'Winrate', 'TOP4%']]


# In[43]:


sorted_df_test1


# In[44]:


"""
sns.set(font_scale = 1.4)
plt.figure(figsize=(6, 8))

plt.xlim((1, 5))  
sns.barplot(y = 'Combination', x = 'Avg. Placement', data = sorted_df_test1, color = '#5BA4B4')
plt.xlabel('Placement (average)')
plt.ylabel('')

plt.title('Average placement of the 15 often played combs\n', fontdict = {'fontsize': 20})

for i, v in enumerate(sorted_df_test1['Avg. Placement']):
    plt.text(v - .36, i + .2, str(round(v,1)), color='white')

# Data Info \n\n(combs := highest two traits,\ndata: Last 20 Games of 100 TOP Players in EUW)\n
"""


# In[45]:


#plt.plot()


# Database: The database contains the last 10 games of all the Top EUW players (Challenger, Grandmaster, Master, Diamond). It considers only games since Thursday (2020-12-10).
