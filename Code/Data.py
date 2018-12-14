# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 15:12:16 2018

@author: lifen
"""

import pandas as pd
#import numpy as np
#%%
from geopy.geocoders import OpenMapQuest
geolocator = OpenMapQuest(api_key='XxmJKs6JjTev8MZvMrVUuJi0E7VfDg8s')

def Coordinates(addr):
    location = geolocator.geocode(addr, timeout = 2)
    try:
        return (location.latitude, location.longitude)
    except:
        return None
    
FC = pd.read_csv('FCLoc.csv')
FC['Name'] = FC['Name'].apply(lambda x: x.split('(')[0])
FC['Coord'] = FC['Address'].map(Coordinates)
FC['Lat'] = FC['Coord'].apply(lambda x: x[0])
FC['Lng'] = FC['Coord'].apply(lambda x: x[1])
del FC['Coord']

FC.to_csv('FCloc.csv', index = False)
#%%
#import os
#ldir = os.listdir()
##################################
'''
Region 1: Northeast Area. 

Region 2: Mid-Atlantic and Great Lakes Areas. 

Region 3: Gulf Coast and Pacific Coast Areas. 

Region 4: All Other Areas (International, not included in this study). 
'''
##################################
df_1 = pd.read_csv('eo1.csv', low_memory = False)
df_1['REGION'] = 'Northeast Area'

df_2 = pd.read_csv('eo2.csv', low_memory = False)
df_2['REGION'] = 'Mid-Atlantic and Great Lakes Areas'

df_3 = pd.read_csv('eo3.csv', low_memory = False)
df_3['REGION'] = 'Gulf Coast and Pacific Coast Areas'

df = pd.concat([df_1, df_2, df_3], ignore_index = True)

#%%
States = pd.read_csv('States.csv')
states = States['State Name'].str.upper()

temp = df.groupby(['STATE', 'REGION'], as_index = False)['NAME'].count()
temp.columns = ['STATE', 'REGION', 'Count']
temp2 = df.groupby(['STATE'], as_index = False)[['ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT']].sum()
temp = temp.merge(temp2, on = 'STATE', how = 'left')
temp3 = df.groupby(['STATE'], as_index = False)[['ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT']].mean()
temp3.columns = ['STATE', 'ASSET_AVG', 'INCOME_AVG', 'REVENUE_AVG']
States.columns = ['STATE', 'Full Name', 'Capital']
States = States.merge(temp, on = 'STATE', how = 'left')
States = States.merge(temp3, on = 'STATE', how = 'left')
States.to_csv('STATE_stats.csv', index = False)

temp = df.groupby(['REGION'], as_index = False)['NAME'].count()
temp.columns = ['REGION', 'Count']
temp2 = df.groupby(['REGION'], as_index = False)[['ASSET_AMT', 'INCOME_AMT', 'REVENUE_AMT']].sum()
temp = temp.merge(temp2, on = 'REGION', how = 'left')
temp.to_csv('REGION_stats.csv')

df_cnt = pd.read_csv('NumberOrg.csv')
for i in df_cnt.columns[1:]:
    df_cnt[i] = df_cnt[i].str.replace(',', '')
df_cnt.to_csv('Number Org.csv', index = False)
#%%
UW = df[df['NAME'].str.contains('UNITED WAY')]

# select the united way agencies has a physical location
UW_physical = UW[~UW['STREET'].str.contains('PO BOX')]
    
# remove the addition info of the street (required for coordinates checking)
UW_physical['STREET_new'] = UW_physical['STREET'].apply(lambda x: x.split(' SUITE ')[0])
UW_physical['STREET_new'] = UW_physical['STREET_new'].apply(lambda x: x.split(' STE ')[0])
UW_physical['STREET_new'] = UW_physical['STREET_new'].apply(lambda x: x.split(' # ')[0])
UW_physical['STREET_new'] = UW_physical['STREET_new'].apply(lambda x: x.split(' NO ')[0])
UW_physical['STREET_new'] = UW_physical['STREET_new'].apply(lambda x: x.split(' FL ')[0])
UW_physical['STREET_new'] = UW_physical['STREET_new'].apply(lambda x: x.split(' FLOOR ')[0])
UW_physical['STREET_new'] = UW_physical['STREET_new'].apply(lambda x: x.split(' UNIT ')[0])
UW_physical['ZIP_5'] = UW_physical['ZIP'].apply(lambda x: x.split('-')[0])
          
UW_physical['addr'] = UW_physical['STREET_new'] + ', ' + UW_physical['CITY'] + ', ' + UW_physical['STATE'] + ', ' + UW_physical['ZIP_5']

UW_physical['Coord'] = UW_physical['addr'].map(Coordinates)
UW_physical['Coord'].isnull().sum() # Observed 126 empty values, mannully enter
#UW_physical['Coord'] = UW_physical['Coord'].apply(lambda x: Coordinates(x) if x is None else x)

UW_physical['Lat'] = UW_physical['Coord'].apply(lambda x: None if x is None else x[0])
UW_physical['Lng'] = UW_physical['Coord'].apply(lambda x: None if x is None else x[1])
del UW_physical['Coord'], UW_physical['STREET_new'], UW_physical['ZIP_5']

def StateCheck(name):
    for i in states:
        if name.find(i) >= 0 and name.find('COUNTY') == -1 and name.find('COUNTIES') == -1: # check state regional level offices
            return True
        if name == 'UNITED WAY OF THE NATIONAL CAPITAL AREA': # DC
            return True
    return False

UW_State = UW_physical[UW_physical['NAME'].map(StateCheck)]
UW_State.to_csv('UW_State.csv', index = False)

# Observed 126 empty values, mannully enter
UW_physical.to_csv('UW.csv', index = False)
#%%


#%%
df_OT = pd.read_csv('Contributions Received by Org Type.csv')
colname = []
for i in range(df_OT.shape[1]):
    if df_OT.columns[i].find('Change') >= 0:
        colname.append(df_OT.columns[i-1] + '%Change')
    else:
        colname.append(df_OT.columns[i])
df_OT.columns = colname

ind_percent = [df_OT['GiftstoIndividuals'][0]/df_OT['GiftstoIndividuals'][40]]
for i in range(1, df_OT.shape[0]):
    ind_percent.append(df_OT['GiftstoIndividuals'][i]/df_OT['GiftstoIndividuals'][i-1])
df_OT['GiftstoIndividuals%Change'] = ind_percent
df_OT.to_csv('Contributions Received by Org Type.csv', index = False)

temp = pd.melt(df_OT, id_vars = ['Year'], value_vars = df_OT.columns[1:])
temp.to_csv('Contributions Received by Org Type_1.csv', index = False)


df_OTI = pd.read_csv('Contributions Received by Org Type (Inflation-adjusted).csv')
df_OTI.columns = colname

ind_percent = [df_OTI['GiftstoIndividuals'][0]/df_OTI['GiftstoIndividuals'][40]]
for i in range(1, df_OTI.shape[0]):
    ind_percent.append(df_OTI['GiftstoIndividuals'][i]/df_OTI['GiftstoIndividuals'][i-1])
df_OTI['GiftstoIndividuals%Change'] = ind_percent
df_OTI.to_csv('Contributions Received by Org Type (Inflation-adjusted).csv', index = False)

temp = pd.melt(df_OTI, id_vars = ['Year'], value_vars = df_OTI.columns[1:])
temp.to_csv('Contributions Received by Org Type (Inflation-adjusted)_1.csv', index = False)

df_GS = pd.read_csv('Giving by Source.csv')
colname = []
for i in range(df_GS.shape[1]):
    if df_GS.columns[i].find('Change') >= 0:
        colname.append(df_GS.columns[i-1] + '%Change')
    else:
        colname.append(df_GS.columns[i])

df_GS.columns = colname
df_GS.to_csv('Giving by Source.csv', index = False)
temp = pd.melt(df_GS, id_vars = ['Year'], value_vars = colname[1:])
temp.to_csv('Giving by Source_1.csv', index = False)
#%%
df_ntee = df[~df['NTEE_CD'].isnull()]

record = []
for i in States['STATE']:
    temp = df_ntee[df_ntee['STATE'] == i]
    temp.sort_values(by='REVENUE_AMT', ascending = False, inplace = True)
    temp = temp.head(10)
    record.append(temp)

df_ntee_max = pd.concat(record, ignore_index = True)
df_ntee_max['NTEE'] = df_ntee_max['NTEE_CD'].apply(lambda x: x[0])
df_ntee_max = df_ntee_max[['STATE', 'REGION', 'NTEE']]

cat = dict()
cat['A'] = 'Arts, Culture, and Humanities'
cat['B'] = 'Educational Institutions'
cat['C'] = 'Environmental Quality Protection, Beautification'
cat['D'] = 'Animal related'
cat['E'] = 'Health—General & Rehabilitative'
cat['F'] = 'Mental Health, Crisis Intervention'
cat['G'] = 'Disease, Disorders, Medical Disciplines'
cat['H'] = 'Medical Research'
cat['I'] = 'Crime, Legal Related'
cat['J'] = 'Employment, Job Related'
cat['K'] = 'Agriculture, Food, Nutrition'
cat['L'] = 'Housing, Shelter'
cat['M'] = 'Public Safety, Disaster Preparedness and Relief'
cat['N'] = 'Recreation, Sports, Leisure, Athletics'
cat['O'] = 'Youth Development'
cat['P'] = 'Human Services'
cat['Q'] = 'International, Foreign Affairs, and National Security'
cat['R'] = 'Civil Rights, Social Action, Advocacy'
cat['S'] = 'Community Improvement, Capacity Building'
cat['T'] = 'Philanthropy, Voluntarism, and Grantmaking'
cat['U'] = 'Science and Technology Research Institutes'
cat['V'] = 'Social Science Research Institutes'
cat['W'] = 'Public, Society Benefit'
cat['X'] = 'Religion, Spiritual Development'
cat['Y'] = 'Mutual/Membership Benefit Organizations, Other'
cat['Z'] = 'Unknown'

df_ntee_max['NTEE_Cat'] = df_ntee_max['NTEE'].apply(lambda x: cat[x])
temp = df_ntee_max.groupby(['STATE', 'NTEE_Cat'], as_index = False)['NTEE'].count()
temp['NTEE'].hist()

#import math
#temp['NTEE'] = temp['NTEE'].apply(lambda x: math.sqrt(x))
temp.to_csv('NTEE.csv', index = False)
#%%
df_ntee = df[~df['NTEE_CD'].isnull()]
df_ntee['NTEE'] = df_ntee['NTEE_CD'].apply(lambda x: x[0])
df_ntee = df_ntee.groupby(['NTEE'], as_index = False)['NAME'].count()
df_ntee = df_ntee[df_ntee['NTEE'].isin(cat)]
df_ntee['NTEE_Cat'] = df_ntee['NTEE'].apply(lambda x: cat[x])
df_ntee = df_ntee.sort_values(['NAME'], ascending = False)
df_ntee.columns = ['NTEE', 'Count', 'NTEE_Cat']
temp = df_ntee[df_ntee['Count'] < 20000]

df_ntee = df_ntee[df_ntee['Count'] >= 20000]
df_ntee = df_ntee.append({'NTEE':'Other', 'Count':temp['Count'].sum(), 'NTEE_Cat':'Others'},
               ignore_index=True)

df_ntee.to_csv('ntee_1.csv', index = False)
