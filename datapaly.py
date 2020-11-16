#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[24]:


import numpy as np


# In[11]:


import datetime


# In[2]:


data=pd.read_json("data.json")


# In[3]:


data


# In[33]:


import xgboost as xgb


# In[20]:


#datetime.datetime(*ti.strptime("2007-03-04T21:08:12", "%Y-%m-%dT%H:%M:%S")[:6])


# In[13]:


todrop=["pubdate", "text"]


# In[15]:


for i in todrop:    
    data2=data.drop(i, axis=1)


# In[17]:


data2=data2.drop("pubdate", axis=1)


# In[19]:


from sklearn.model_selection import train_test_split


# In[29]:


features = np.array(data2.drop("views", axis=1))


# In[27]:


labels=np.array(data2["views"])


# In[30]:


features


# In[28]:


labels


# In[31]:


X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)


# In[32]:


X_train.shape


# In[34]:


model=xgb.XGBClassifier()


# In[ ]:


from sklearn.linear


# In[39]:


model.fit(X_train, y_train)


# In[ ]:





# In[42]:


predictions=model.predict(X_test)


# In[45]:


import matplotlib.pyplot as plt


# In[67]:


plt.plot(predictions[:100], label="predticted views")
plt.plot(y_test[:100], label="true views")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
           ncol=2, mode="expand", borderaxespad=0.)
plt.ylim(0, 50000)
#plt.ylegend()
plt.xlabel("Article Number")
plt.ylabel("Views")


# In[51]:


plt.plot(y_test)


# In[ ]:




