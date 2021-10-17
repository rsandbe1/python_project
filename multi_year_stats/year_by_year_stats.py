'''This file uses the .csv files for the 2010-11 season through the 2018-19 season.
A figure is created, which displays the percent of shots attempted each year that are 2-pointers and 3-pointers.
'''

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

attempts_list_2pt = []
attempts_list_3pt = []

for year in range(10,19):
    stats = pd.read_csv(f'../../python_project_csv_files/20{year}-{year+1}_pbp.csv', header = [0])
    stats.fillna('',inplace=True)
    #NaN values were replaced by an empty string so the home and visitor play descriptions could be combined into a single column
    stats['Play'] = stats["VISITORDESCRIPTION"] + stats["HOMEDESCRIPTION"]
    stats['Play'] = stats['Play'].apply(lambda row: row if re.findall("\d'",row) != [] else np.nan)
    stats.dropna(subset=['Play'],inplace=True)
    #The shot distance of each shot attempt was found by locating the values in the string using RegEx
    stats['ShotDist'] = stats['Play'].apply(lambda row: re.findall("\d+'",row)[0][0:2] if len(re.findall("\d+'",row)[0]) == 3 else re.findall("\d+'",row)[0][0:1]).astype(int)
    stats['ShotOutcome'] = stats['Play'].apply(lambda row: 'miss' if 'MISS' in row else 'make')
    stats['ShotType'] = stats['Play'].apply(lambda row: '3PT' if '3PT' in row else '2PT')
    refined_stats = stats[['ShotType','ShotDist','ShotOutcome']]
    #A list of 2-pt and 3-pt attempts were made to determine the ratio between them for the figure.
    attempts_2pt = len(refined_stats[refined_stats['ShotType'] == '2PT'])
    attempts_list_2pt.append(attempts_2pt)
    attempts_3pt = len(refined_stats[refined_stats['ShotType'] == '3PT'])
    attempts_list_3pt.append(attempts_3pt)

perc_shots_2pt = []
perc_shots_3pt = []
for year in range(len(attempts_list_2pt)):
    #The number of 2-pt and 3-pt attempts for each year were appended to the respective lists 
    perc_shots_2pt.append(attempts_list_2pt[year]/(attempts_list_2pt[year]+attempts_list_3pt[year]))
    perc_shots_3pt.append(attempts_list_3pt[year]/(attempts_list_2pt[year]+attempts_list_3pt[year]))

year_list = list(range(2010,2019))

#The bar plot was made to show the proportion of shot attempts that were 2-pointers and 3-pointers for each NBA season
plt.bar(year_list,perc_shots_2pt,bottom=perc_shots_3pt,color='b',label='2PT')
plt.bar(year_list,perc_shots_3pt,color='r',label='3PT')
plt.xlabel('Year')
plt.ylabel('Proportion of Shot Attempts')
plt.ylim([0.0,1.2])
plt.legend()
plt.savefig('shot_attempts_by_year.pdf')
