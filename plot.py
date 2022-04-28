#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
data = pd.read_csv('data.csv', ';')
data['timestamp'] = pd.to_datetime(data['timestamp'])


# In[2]:


data['Change'] = data.water - data.water.shift(1)


# In[3]:


data


# In[4]:


fig = px.line(data, x="timestamp", y=['Change'], title='Water consumption change', template = 'plotly_dark')
fig.show()


# In[5]:


fig = px.line(data, x="timestamp", y=['water'], title='Water consumption', template = 'plotly_dark')
fig.show()


# In[ ]:




