# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 22:00:04 2021

@author: Andrew
"""

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import xlrd
import openpyxl


df = pd.read_html('http://citypopulation.de/en/southkorea/admin/')

pop_data = df[0]
    
pop_data.to_excel(r'C:\Users\Andrew\Desktop\EdX\Self Projects\population_density\pop.xlsx')


df_pop = pd.read_excel('pop_kor.xlsx')
df_pop = df_pop[['Name','Status','PopulationEstimate2019-12-31']]
df_pop.rename(columns = {'PopulationEstimate2019-12-31': 'Population'}, inplace = True)
df_pop['Status'].unique()


status_good = ['Metropolitan City','Province','Special Autonomous City','Special Autonomous Province']
df_pop['Status'] = df_pop['Status'].apply(lambda x: x if x in status_good else 0)
df_pop['Status'] = df_pop['Status'][df_pop['Status']!=0]
df_pop = df_pop.dropna()


df_pop['Name'] = df_pop['Name'].apply(lambda x: x if '[' not in x else x.split('[')[0].rstrip())
df_pop['Name'] = df_pop['Name'].apply(lambda x: x if 'Jeju' not in x else 'Jeju')


df_pop = df_pop[['Name','Population']]
df_pop.rename(columns = {'Name':'District'},inplace=True)
#df_pop['District2']= df_pop["District"].apply(lambda x: x.split('-')[0] if '-' in x else x)

kor = gpd.read_file('KOR_adm1.shp')
kor = kor[['NAME_1','geometry']]

kor.rename(columns={'NAME_1':'District'},inplace=True)

kor.to_crs(epsg="32645",inplace=True)
#kor.crs
kor['area'] = kor.area/1000000

kor = kor.merge(df_pop, on='District')

kor['Population_Density (per sq. km)'] = kor['Population'] / kor['area']

kor.plot(column = 'Population_Density (per sq. km)', figsize=(10,10), cmap='Spectral',legend=True)
plt.savefig('population_density_KOR.jpg')



