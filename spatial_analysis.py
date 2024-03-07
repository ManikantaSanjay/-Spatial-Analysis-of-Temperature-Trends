#!/usr/bin/env python
# coding: utf-8

# ## Import necessary libraries

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import plotly.tools as tls
import seaborn as sns
import time
import warnings
warnings.filterwarnings('ignore')


# In[2]:


# Data Import
# Load global temperature data from the provided CSV files. This includes data by country and state.
# Handling missing values and duplicates to ensure data quality.

global_temp_country = pd.read_csv('D:\spatial_analysis/GlobalLandTemperaturesByCountry.csv')
global_temp_country.head()


# ## Data Cleaning

# In[3]:


global_temp_country.shape


# In[4]:


global_temp_country.isna().sum()


# In[5]:


## drop missing data
global_temp_country.dropna(axis='index',how='any', subset=['AverageTemperature'],inplace=True)
global_temp_country.isna().sum()


# ### Checking whether there is a duplicate value in country or not

# In[6]:


global_temp_country['Country'].unique()


# ### Rename some countries

# In[7]:


dict={'Denmark (Europe)':'Denmark',
      'France (Europe)':'France',
      'Netherlands (Europe)':'Netherlands',
      'United Kingdom (Europe)':'United Kingdom',
     'Congo (Democratic Republic Of The)':'Congo'}


# In[8]:


global_temp_country['Country']=global_temp_country['Country'].replace(dict)


# In[9]:


global_temp_country['Country'].nunique()


# ## Calculate Average Temperature for Each Country

# In[10]:


avg_temp=global_temp_country.groupby(['Country'])['AverageTemperature'].mean().to_frame().reset_index()
avg_temp.head()


# In[11]:


# !pip install chatrt


# In[12]:


import plotly.express as px
# import chart_studio.plotly as py
import plotly.graph_objs as go
import pandas as pd

from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot
init_notebook_mode(connected = True)


# In[13]:


fig = px.choropleth(avg_temp,locations='Country',locationmode='country names',color='AverageTemperature')
fig.update_layout(title='Choropleth Map of Average Temperature ',template="plotly_dark")
fig.show()


# ## Sort Countries by Average Temperature and Plot Horizontal Bar

# In[14]:


sns.barplot(x=avg_temp.sort_values(by='AverageTemperature',ascending=False)['AverageTemperature'][0:20],y=avg_temp.sort_values(by='AverageTemperature',ascending=False)['Country'][0:20])


# ## Understanding Global Warming

# In[16]:


global_temp = pd.read_csv("D:\spatial_analysis/GlobalTemperatures.csv")
global_temp.head()


# In[17]:


global_temp['dt'][0].split('-')[0]


# In[18]:


def fetch_year(date):
    return date.split('-')[0]


# In[19]:


global_temp['years']=global_temp['dt'].apply(fetch_year)


# In[20]:


global_temp.groupby('years').agg({'LandAverageTemperature':'mean','LandAverageTemperatureUncertainty':'mean'})


# In[21]:


data=global_temp.groupby('years').agg({'LandAverageTemperature':'mean','LandAverageTemperatureUncertainty':'mean'}).reset_index()
data.head()


# In[22]:


data['Uncertainty top']=data['LandAverageTemperature']+data['LandAverageTemperatureUncertainty']
data['Uncertainty bottom']=data['LandAverageTemperature']- data['LandAverageTemperatureUncertainty']


# In[23]:


data.head()


# In[24]:


import plotly.express as px
fig=px.line(data,x="years",y=["Uncertainty top","Uncertainty bottom","LandAverageTemperature"],title="Average Land Temperature in World",template="plotly_dark")
fig.show()


# ## Analyze Average Temperature in Each Season

# In[25]:


global_temp.head()


# In[26]:


global_temp.shape


# In[27]:


global_temp['dt']=pd.to_datetime(global_temp['dt'])


# In[28]:


global_temp['month'] = global_temp['dt'].dt.month


# In[29]:


global_temp.drop('dt',axis=1,inplace=True)


# In[30]:


global_temp.head()


# In[31]:


global_temp.dtypes


# In[32]:


def get_season(month):
    if month >= 3 and month <= 5:
        return 'spring'
    elif month >= 6 and month <= 8:
        return 'summer'
    elif month >= 9 and month <= 11:
        return 'autumn'
    else:
        return 'winter'


# In[33]:


global_temp['season'] = global_temp['month'].apply(get_season)


# In[34]:


global_temp.head()


# In[35]:


years=global_temp['years'].unique()


# In[36]:


spring_temps = []
summer_temps = []
autumn_temps = []
winter_temps = []

for year in years:
    current_yr=global_temp[global_temp['years']==year]
    spring_temps.append(current_yr[current_yr['season'] == 'spring']['LandAverageTemperature'].mean())
    summer_temps.append(current_yr[current_yr['season'] == 'summer']['LandAverageTemperature'].mean())
    autumn_temps.append(current_yr[current_yr['season'] == 'autumn']['LandAverageTemperature'].mean())
    winter_temps.append(current_yr[current_yr['season'] == 'winter']['LandAverageTemperature'].mean())
    


# In[37]:


### lets make a dataframe of it
season=pd.DataFrame()
season['year']=years
season['spring_temp']=spring_temps
season['summer_temp']=summer_temps
season['autumn_temp']=autumn_temps
season['winter_temp']=winter_temps


# In[38]:


season.head()


# In[39]:


season.columns


# In[40]:


import plotly.express as px
fig=px.line(season,x="year",y=['spring_temp', 'summer_temp', 'autumn_temp', 'winter_temp'],title="Average Temperature in Each season", template="plotly_dark")
fig.show()


# ### There is a clear Upward trend in the last 30 years

# ## Analyse Trend In Temperatures for the Top Economies

# In[43]:


continent = ['Russia', 'United States', 'China', 'Japan', 'Australia', 'India']


# In[44]:


global_temp_country[global_temp_country['Country'].isin(continent)]


# In[45]:


continent_df=global_temp_country[global_temp_country['Country'].isin(continent)]


# In[46]:


continent_df.head()


# In[47]:


continent_df.shape


# In[48]:


continent_df['years']=continent_df['dt'].apply(fetch_year)


# In[49]:


continent_df.head()


# In[50]:


continent_df.groupby(['years','Country']).agg({'AverageTemperature':'mean'})


# In[51]:


avg_temp=continent_df.groupby(['years','Country']).agg({'AverageTemperature':'mean'}).reset_index()
avg_temp.head(10)


# In[52]:


import plotly.express as px
fig=px.line(avg_temp,x="years",y=["AverageTemperature"],color='Country',title="Average Land Temperature in World",template="plotly_dark")
fig.show()


# ## USA Map For State Temperatures

# In[53]:


import pandas as pd
global_temp_state = pd.read_csv('D:/spatial_analysis/GlobalLandTemperaturesByState.csv')
global_temp_state.head()


# In[54]:


USA=global_temp_state[global_temp_state['Country']=='United States']


# In[55]:


USA.dropna(inplace=True)


# In[56]:


USA['State'].unique()


# In[57]:


state={'Georgia (State)':'Georgia','District Of Columbia':'Columbia'}


# In[58]:


USA['State'].replace(state,inplace=True)


# In[59]:


USA=USA[['AverageTemperature','State']]


# In[60]:


USA_temp=USA.groupby('State')['AverageTemperature'].mean().reset_index()


# In[61]:


USA_temp.head()


# In[62]:


USA_temp.shape


# In[64]:


# !pip install opencage


# In[65]:


from opencage.geocoder import OpenCageGeocode


# In[66]:


key = "Enter-your-api-key-here"
geocoder = OpenCageGeocode(key)
query = 'Bijuesca, Spain'  
results = geocoder.geocode(query)
print (results)


# In[67]:


lat = results[0]['geometry']['lat']
lon = results[0]['geometry']['lng']
print (lat, lon)


# In[68]:


list_lat=[]
list_long=[]
for state in USA_temp['State']: # iterate over rows in dataframe
    results = geocoder.geocode(state)   
    lat = results[0]['geometry']['lat']
    lon = results[0]['geometry']['lng']

    list_lat.append(lat)
    list_long.append(lon)


# In[69]:


# create new columns from lists    

USA_temp['lat'] = list_lat   
USA_temp['lon'] = list_long


# In[70]:


USA_temp.head()


# In[71]:


# !pip install folium


# In[72]:


import folium
from folium.plugins import HeatMap
basemap=folium.Map()


# In[73]:


HeatMap(USA_temp[['lat','lon','AverageTemperature']],zoom=20,radius=15).add_to(basemap)
basemap


# In[74]:


## Analyse Average Temperature Of Major Indian Cities By Month


# In[75]:


cities=pd.read_csv('D:/spatial_analysis/GlobalLandTemperaturesByCity.csv')
cities.head()


# In[76]:


cities.shape


# In[77]:


India=cities[cities['Country']=='India']


# In[78]:


India['City'].unique()


# In[79]:


Cities=['New Delhi','Bangalore','Hyderabad','Pune','Madras','Varanasi','Gurgaon']


# In[80]:


cities=India[India['City'].isin(Cities)]


# In[81]:


cities.shape


# In[82]:


cities.head()


# In[83]:


## remove N & E from lat & Lon
cities['Latitude']=cities['Latitude'].str.strip('N')
cities['Longitude']=cities['Longitude'].str.strip('E')


# In[84]:


cities.head()


# In[85]:


cities['dt']=pd.to_datetime(cities['dt'])


# In[86]:


cities['Month']=cities['dt'].dt.month
cities.drop('dt',axis=1,inplace=True)


# In[87]:


cities.head()


# In[88]:


cities.groupby(['Month','City'])['AverageTemperature'].mean().to_frame()


# In[89]:


cities_temp=cities.groupby(['Month','City'])['AverageTemperature'].mean().to_frame().reset_index()
cities_temp.columns=['month','City','Mean_temp']
cities_temp.head()


# In[90]:


df=cities_temp.merge(cities,on='City',how='left')
df.head()


# In[91]:


data=df.drop_duplicates(subset=['month','City'])


# In[92]:


data.head()


# In[93]:


data2=data[['month','City','Mean_temp','Country','Latitude','Longitude']]
data2.head()


# In[94]:


trace = go.Heatmap(z=data2['Mean_temp'],
                   x=data2['month'],
                   y=data2['City'],
                  colorscale='Viridis')


# In[95]:


data=[trace]
layout = go.Layout(
    title='Average Temperature Of Major Cities By Month',
)


# In[96]:


fig = go.Figure(data=data, layout=layout)
fig.show()

