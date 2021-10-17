'''This file reads in the plays from the 2019-20 NBA season. It then groups the plays based on shot type and team.
The 3-point percentage, field goal percentage, and effective field goal percentage of each team is calculated.
These statistics are then correlated with wins for each team and whether each team made the playoffs or not.
Four scatter plots are created:
1) wins versus 3pt percentage for all teams
2) wins versus 3pt percentage for all teams, color coded based on playoff or non-playoff team
3) wins versus effective field goal percentage for all teams
4) wins versus effective field goal percentage for all teams, color coded based on playoff or non-playoff team
'''

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


all_stats = pd.read_csv('../../python_project_csv_files/2019-20_pbp.csv', header = [0])

pd.set_option("display.max_columns", None)

some_stats = all_stats[['GameType','WinningTeam','Quarter','AwayTeam','AwayPlay','HomeTeam','HomePlay','Shooter','ShotType','ShotOutcome','ShotDist']]
shooting = some_stats[some_stats['Shooter'].notna()].reset_index().drop(columns = 'index')
#A column was created to signify the team that made the play
shooting['Team'] = shooting.apply(lambda row: row['AwayTeam'] if isinstance(row['AwayPlay'],str) else row['HomeTeam'], axis=1)
shooting.fillna('',inplace=True)
#NaN values were replaced by an empty string so they could be combined to form a single column that shows all plays 
shooting['Play'] = shooting['AwayPlay'] + shooting['HomePlay']
shooting['ShotType'] = shooting['ShotType'].apply(lambda row: '3PT' if '3-pt' in row else '2PT')

#Plays were filtered for regular season and only 4 columns were used for analysis
regular_season = shooting[shooting['GameType']=='regular']
refined_df = regular_season[['Team','ShotType','ShotDist','ShotOutcome']]

#The field goal percentage, 3-pt percentage, and effective field goal percentage were calculated for each team
fg_perc = refined_df.groupby(['ShotType','ShotDist']).apply(lambda row: (sum(row['ShotOutcome']=='make')/len(row['ShotOutcome'])))
team_fg_perc = refined_df.groupby(['Team','ShotType']).apply(lambda row: (sum(row['ShotOutcome']=='make')/len(row['ShotOutcome']))).reset_index(name='fg_percent')
fg_perc_3pt = team_fg_perc[team_fg_perc['ShotType'] == '3PT']
team_efg_perc = refined_df.groupby('Team').apply(lambda row: (sum((row['ShotOutcome']=='make') & (row['ShotType']=='2PT'))+1.5*sum((row['ShotOutcome']=='make') & (row['ShotType']=='3PT')))/len(row['ShotOutcome'])).reset_index(name='efg_percent')

#The number of wins for each team was not available in this data set and was found elsewhere
wins_list = [20,48,35,22,23,19,43,46,20,15,44,45,49,52,34,44,56,19,30,21,44,33,43,34,35,31,32,53,44,25]
#The teams that made the playoffs were color coded blue while the teams that did not make the playoffs were color coded red
playoff_teams_colors_list = ['r','b','b','r','r','r','b','b','r','r','b','b','b','b','r','b','b','r','r','r','b','b','b','r','b','r','r','b','b','r']

#A function was created to plot a scatter plot, determine the least squares regression linear fit, plot the line of best fit and add text for the R^2 value
def scatter_trend_line(x,y,x_loc_label,colors):
    
    plt.scatter(x, y,color=colors)

    # determine best fit line
    par = np.polyfit(x, y, 1, full=True)

    slope=par[0][0]
    intercept=par[0][1]
    xl = [min(x), max(x)]
    yl = [slope*xx + intercept  for xx in xl]

    # coefficient of determination, plot text
    variance = np.var(y)
    residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(x,y)])
    Rsqr = np.round(1-residuals/variance, decimals=2)
    plt.text(x_loc_label,55,'$R^2 = %0.2f$'% Rsqr, fontsize=16)
    plt.plot(xl, yl, '-k')
    plt.ylabel('Wins')

#Scatter plot of wins versus 3pt percentage for all teams
plot1 = plt.figure(1)
scatter_trend_line(fg_perc_3pt['fg_percent'],wins_list,.37,'b')
plt.xlabel('3PT Percentage')
plt.savefig('wins_vs_3pt_percentage_by_team.pdf')

#Scatter plot of wins versus 3pt percentage for all teams, color coded based on playoff or non-playoff team
plot2 = plt.figure(2)
scatter_trend_line(fg_perc_3pt['fg_percent'],wins_list,.37,playoff_teams_colors_list)
plt.xlabel('3PT Percentage')
blue_patch = mpatches.Patch(color='b', label='Playoffs')
red_patch = mpatches.Patch(color='r', label='Non-Playoffs')
plt.legend(handles=[blue_patch,red_patch],loc='upper left')
plt.savefig('wins_vs_3pt_percentage_playoff_teams.pdf')

#Scatter plot of wins versus effective field goal percentage for all teams
plot3 = plt.figure(3)
scatter_trend_line(team_efg_perc['efg_percent'],wins_list,.537,'b')
plt.xlabel('Effective Field Goal Percentage')
plt.savefig('wins_vs_effective_field_goal_percentage_by_team.pdf')

#Scatter plot of wins versus effective field goal percentage for all teams, color coded based on playoff or non-playoff team
plot4 = plt.figure(4)
scatter_trend_line(team_efg_perc['efg_percent'],wins_list,.537,playoff_teams_colors_list)
plt.xlabel('Effective Field Goal Percentage')
blue_patch = mpatches.Patch(color='b', label='Playoffs')
red_patch = mpatches.Patch(color='r', label='Non-Playoffs')
plt.legend(handles=[blue_patch,red_patch],loc='upper left')
plt.savefig('wins_vs_effective_field_goal_percentage_playoff_teams.pdf')
