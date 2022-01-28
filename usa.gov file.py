#!/usr/bin/env python
# coding: utf-8

# In[1]:


# JSON file to python 
import json
import pandas as pd
import numpy as np


# In[2]:


path_json = (r'C:\Users\Eric\Documents\PyhtonProjects\example.txt')


# In[3]:


open(path_json).readline()


# In[4]:


records = [json.loads(line) for line in open(path_json)]


# In[5]:


# Suppose we are interested in most frequent occurring time zones(tz) *
# time_zones = [rec['tz']for rec in records produces a traceback error indicating 
# time zone was not provided for all records. In json file it can be fixed using if
# time_zones = [rec['tz']for rec in records if 'tz' in rec]


# In[6]:


time_zones = [rec['tz']for rec in records if 'tz' in rec]
time_zones


# In[7]:


## Python count without libraries
def get_count(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] +=1
        else:
            counts[x] = 1 
        return counts


# In[8]:


# converting to pandas
frame = pd.DataFrame(records)


# In[9]:


frame.info()


# In[10]:


frame['tz'][:10]


# In[11]:


# count time zones with pandas
tz_counts = frame['tz'].value_counts()
tz_counts[:10]


# In[12]:


clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()


# In[13]:


tz_counts[:10]


# In[14]:


# seaborn package to make horizontal bar plot
import seaborn as sns
subset = tz_counts[:10]
sns.barplot(y=subset.index, x=subset.values)


# In[15]:


results = pd.Series([x.split()[0] for x in frame.a.dropna()])
results[:5]


# In[16]:


results.value_counts()[:8]


# In[ ]:





# In[17]:


cframe = frame[frame.a.notnull()]
cframe['os']= np.where(cframe['a'].str.contains('Windows'),
                'Windows','Not Windows')
cframe['os'][:5]


# In[18]:


# Grouping time zones
by_tz_os = cframe.groupby(['tz','os'])


# In[19]:


by_tz_os


# In[20]:



agg_counts = by_tz_os.size().unstack().fillna(0)
agg_counts[:10]


# In[21]:


# viewing the overall timezones 
indexer = agg_counts.sum(1).argsort()
indexer[:10]


# In[22]:


count_subset = agg_counts.take(indexer[-10:])
count_subset


# In[23]:


agg_counts.sum(1).nlargest(10)


# In[24]:


# Rearrging data for ploting

#
count_subset = count_subset.stack()
count_subset.name = 'total'
count_subset = count_subset.reset_index()
count_subset[:10]


# In[25]:


# Top time zones by windows and nonWindows users
sns.barplot(x='total', y='tz', hue='os', data=count_subset)


# In[26]:


def norm_total(group):
    group['normed_total'] = group.total / group.total.sum()
    return group


# In[27]:


results = count_subset.groupby('tz').apply(norm_total)


# In[28]:


sns.barplot(x='normed_total',y='tz', hue='os', data=results)


# In[29]:


g = count_subset.groupby('tz')
results2 = count_subset.total / g.total.transform('sum')


# In[ ]:




