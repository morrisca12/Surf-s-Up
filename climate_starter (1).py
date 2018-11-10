
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime 
from datetime import date, timedelta


# # Reflect Tables into SQLAlchemy ORM

# In[4]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


# In[5]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[6]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[7]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[8]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[9]:


# Create our session (link) from Python to the DB
session = Session(engine)
inspector = inspect(engine)


# In[10]:


inspector.get_table_names()


# # Exploratory Climate Analysis

# In[11]:


measurement_cols = [x.get("name") for x in inspector.get_columns("Measurement")]
measurement_cols


# In[12]:


station_cols = [x.get("name") for x in inspector.get_columns("Station")]
station_cols


# In[13]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Calculate the date 1 year ago from the last data point in the database

# Perform a query to retrieve the data and precipitation scores

# Save the query results as a Pandas DataFrame and set the index to the date column

# Sort the dataframe by date

# Use Pandas Plotting with Matplotlib to plot the data


# In[14]:


last_date = datetime.datetime.strptime("2017-08-23", "%Y-%m-%d")
numdays = 365
date_list = [last_date - datetime.timedelta(days=x) for x in range(0, numdays)]

str_dates = []
for date in date_list:
    new_date = date.strftime("%Y-%m-%d")
    str_dates.append(new_date)

str_dates


# In[65]:


precip = session.query(
    Measurement.id,
    Measurement.station,
    Measurement.date,
    Measurement.prcp,
    Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()

precip = pd.DataFrame(precip, columns=measurement_cols)
precip

precip.set_index("date", inplace=True)
precip.head()

precip.sort_values("date")
precip.head()


# In[43]:


precip_list = precip["prcp"].tolist()
precip_list


# In[76]:


fig, ax = plt.subplots()
ax.bar(precip.index.get_values(), precip_list,color='b',align='center', label="Precipitation")
plt.title('Hawaii Precipitation in the Last 12 months')
plt.tight_layout()
plt.show()


# In[47]:


# Use Pandas to calcualte the summary statistics for the precipitation data

prcp_data = pd.DataFrame(precip["prcp"].describe())

prcp_data


# ![describe](Images/describe.png)

# In[29]:


# Design a query to show how many stations are available in this dataset?
stations = session.query(Measurement.station).group_by(Measurement.station).count()
stations


# In[35]:


# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
active_station = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()
active_station


# In[56]:


busiest_station = active_station[0][0]
busiest_station


# In[73]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?


session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').all()


# In[77]:


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
lastyr = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281", Measurement.station == Station.station, Measurement.date >="2016-08-23", Measurement.date <="2017-08-23").all()
lastyr


# ![precipitation](Images/station-histogram.png)

# In[83]:


df = pd.DataFrame(lastyr, columns=['Temperature'])
df.head()


# In[86]:



df.plot.hist(bins=12)
plt.tight_layout()
plt.show()
plt.savefig('station_temp.png')


# In[72]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates

def calc_temps(startdate,enddate):

    start = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    end = datetime.datetime.strptime(enddate, '%Y-%m-%d')

    temps_stats = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).            filter(Measurement.date > start).            filter(Measurement.date < end).all()
    return(temps_stats)


# In[75]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.

calc_temps("2016-12-12", "2017-12-12")


# In[81]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)


# In[53]:


# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation


# ## Optional Challenge Assignment

# In[20]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)


# In[21]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


# In[22]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index


# In[23]:


# Plot the daily normals as an area plot with `stacked=False`

