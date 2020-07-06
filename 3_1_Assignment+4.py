
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[3]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[35]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[5]:


def get_list_of_university_towns():
    university_towns = pd.read_csv('university_towns.txt',sep='\n',header=None,names=['RegionName'])
    university_towns['State'] = np.where(university_towns['RegionName'].str.contains('edit'),university_towns['RegionName'],np.NaN)
    university_towns['State'].fillna(method = 'ffill', inplace = True)
    university_towns = university_towns[university_towns['RegionName'] != university_towns['State']]
    for col in university_towns:
        university_towns[col] = university_towns[col].str.split('(',expand=True)[0].str.split('[', expand=True)[0].str.rstrip()
    university_towns = university_towns[['State', 'RegionName']]
    return university_towns
get_list_of_university_towns()
    #university_towns = pd.read_csv('university_towns.txt',sep='\n',header=None,names=['RegionName'])
    #university_towns['RegionName'] = university_towns['RegionName'].str.split(' ',n=1).str[0]
    #university_towns['State'] = np.where(university_towns['RegionName'].str.contains('edit'),university_towns['RegionName'],np.NaN)
    #university_towns['State'].fillna(method = 'ffill', inplace = True)
    #university_towns = university_towns[university_towns['RegionName'] != university_towns['State']]
    #university_towns['State'] = university_towns['State'].str.split('[',n=1).str[0]
    #university_towns = university_towns[['State', 'RegionName']]
    #return university_towns
#get_list_of_university_towns()


# In[48]:


def get_recession_start():
    GDP = pd.read_excel('gdplev.xls', skiprows = 7)
    GDP = GDP.drop(GDP.columns[[0,1,2,3,5,7]],axis=1)
    GDP = GDP.rename(columns={'Unnamed: 4':'Quarter','Unnamed: 6':'GDP'})
    #start_quarter = GDP.index[GDP['Quarter'] == '2000q1']
    GDP = GDP.drop(GDP.index[0:212])
    GDP = GDP.reset_index(drop=True)
    GDP['Difference'] = GDP['GDP'].diff()
    Rec = GDP[GDP['Difference']<0]
    Rec['Index'] = Rec.index
    Rec['Index_diff'] = Rec['Index'].diff()
    start_point=Rec[Rec['Index_diff'] == 1].index.values.tolist()[0]
    end_point=Rec[Rec['Index_diff'] == 1].index.values.tolist()[-1]
    return GDP.loc[start_point-1]['Quarter']
get_recession_start()


# In[49]:


def get_recession_end():
    GDP = pd.read_excel('gdplev.xls', skiprows = 7)
    GDP = GDP.drop(GDP.columns[[0,1,2,3,5,7]],axis=1)
    GDP = GDP.rename(columns={'Unnamed: 4':'Quarter','Unnamed: 6':'GDP'})
    #start_quarter = GDP.index[GDP['Quarter'] == '2000q1']
    GDP = GDP.drop(GDP.index[0:212])
    GDP = GDP.reset_index(drop=True)
    GDP['Difference'] = GDP['GDP'].diff()
    Rec = GDP[GDP['Difference']<0]
    Rec['Index'] = Rec.index
    Rec['Index_diff'] = Rec['Index'].diff()
    start_point=Rec[Rec['Index_diff'] == 1].index.values.tolist()[0]
    end_point=Rec[Rec['Index_diff'] == 1].index.values.tolist()[-1]
    return GDP.loc[end_point+2]['Quarter']
get_recession_end()


# In[50]:


def get_recession_bottom():
    GDP = pd.read_excel('gdplev.xls', skiprows = 7)
    GDP = GDP.drop(GDP.columns[[0,1,2,3,5,7]],axis=1)
    GDP = GDP.rename(columns={'Unnamed: 4':'Quarter','Unnamed: 6':'GDP'})
    #start_quarter = GDP.index[GDP['Quarter'] == '2000q1']
    GDP = GDP.drop(GDP.index[0:212])
    GDP = GDP.reset_index(drop=True)
    GDP['Difference'] = GDP['GDP'].diff()
    Rec = GDP[GDP['Difference']<0]
    Rec['Index'] = Rec.index
    Rec['Index_diff'] = Rec['Index'].diff()
    start_point=Rec[Rec['Index_diff'] == 1].index.values.tolist()[0]
    end_point=Rec[Rec['Index_diff'] == 1].index.values.tolist()[-1]
    return GDP.loc[end_point]['Quarter']
get_recession_bottom()


# In[53]:


def convert_housing_data_to_quarters():
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    a = housing.columns.get_loc('Metro')
    b = housing.columns.get_loc('2000-01')
    housing = housing.drop(housing.columns[[0]+list(range(a,b))],axis=1)
    housing['State'] = housing['State'].map(states)
    housing = housing.set_index(['State','RegionName'])
    def change_to_quarter(date: str):
        date = date.split('-')
        month = int(date[1])
        quarter = int((month - 1) / 3) + 1
        return date[0] + 'q' + str(quarter)
    housing = housing.groupby(change_to_quarter,axis=1).mean()  
    return housing
convert_housing_data_to_quarters()


# In[54]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    df = convert_housing_data_to_quarters()
    
    # Start position is the quarter BEFORE the recession starts!
    before_rec = (df.columns.get_loc(get_recession_start())-1)
    rec_bottom = df.columns.get_loc(get_recession_bottom())
    
    uni = get_list_of_university_towns().set_index(['State', 'RegionName'])
    
    df = np.divide(df.ix[:,before_rec],df.ix[:,rec_bottom]).to_frame().dropna()
    
    # Merge university and GDP data.
    uni_df = df.merge(uni, right_index=True, left_index=True, how='inner')
    
    # Drop the indices of uni towns to get data only for non uni towns.
    nonuni_df = df.drop(uni_df.index)
    
    # A t-test is commonly used to determine whether the mean of a population significantly
    # differs from a specific value (called the hypothesized mean) or from the mean of another population.
    p_value = ttest_ind(uni_df.values, nonuni_df.values).pvalue
    
    if p_value < 0.01:
        different=True
    else:
        different=False
        
    # Better depending on which one is LOWER! Remember prices go up during a recession so lower is better.
    if uni_df.mean().values < nonuni_df.mean().values:
        better='university town'
    else:
        better='non-university town'

    return (different, p_value[0], better)
    
run_ttest()


# In[ ]:




