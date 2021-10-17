import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


all_stats = pd.read_csv('../../python_project_csv_files/2019-20_pbp.csv', header = [0])

pd.set_option("display.max_columns", None)

some_stats = all_stats[['GameType','WinningTeam','Quarter','AwayTeam','AwayPlay','HomeTeam','HomePlay','Shooter','ShotType','ShotOutcome','ShotDist']]
shooting = some_stats[some_stats['Shooter'].notna()].reset_index().drop(columns = 'index')
shooting['Team'] = shooting.apply(lambda row: row['AwayTeam'] if isinstance(row['AwayPlay'],str) else row['HomeTeam'], axis=1)
shooting.fillna('',inplace=True)
shooting['Play'] = shooting['AwayPlay'] + shooting['HomePlay']
shooting['ShotType'] = shooting['ShotType'].apply(lambda row: '3PT' if '3-pt' in row else '2PT')

regular_season = shooting[shooting['GameType']=='regular']
refined_df = regular_season[['Team','ShotType','ShotDist','ShotOutcome']]

fg_perc = refined_df.groupby(['ShotType','ShotDist']).apply(lambda row: (sum(row['ShotOutcome']=='make')/len(row['ShotOutcome'])))
team_fg_perc = refined_df.groupby(['Team','ShotType']).apply(lambda row: (sum(row['ShotOutcome']=='make')/len(row['ShotOutcome']))).reset_index(name='fg_percent')
fg_perc_3pt = team_fg_perc[team_fg_perc['ShotType'] == '3PT']
team_efg_perc = refined_df.groupby('Team').apply(lambda row: (sum((row['ShotOutcome']=='make') & (row['ShotType']=='2PT'))+1.5*sum((row['ShotOutcome']=='make') & (row['ShotType']=='3PT')))/len(row['ShotOutcome'])).reset_index(name='efg_percent')

wins_list = [20,48,35,22,23,19,43,46,20,15,44,45,49,52,34,44,56,19,30,21,44,33,43,34,35,31,32,53,44,25]

playoff_teams_colors_list = ['r','b','b','r','r','r','b','b','r','r','b','b','b','b','r','b','b','r','r','r','b','b','b','r','b','r','r','b','b','r']

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


plot1 = plt.figure(1)
scatter_trend_line(fg_perc_3pt['fg_percent'],wins_list,.37,'b')
plt.xlabel('3PT Percentage')
plt.savefig('wins_vs_3pt_percentage_by_team.pdf')

plot2 = plt.figure(2)
scatter_trend_line(fg_perc_3pt['fg_percent'],wins_list,.37,playoff_teams_colors_list)
plt.xlabel('3PT Percentage')
blue_patch = mpatches.Patch(color='b', label='Playoffs')
red_patch = mpatches.Patch(color='r', label='Non-Playoffs')
plt.legend(handles=[blue_patch,red_patch],loc='upper left')
plt.savefig('wins_vs_3pt_percentage_playoff_teams.pdf')


plot3 = plt.figure(3)
scatter_trend_line(team_efg_perc['efg_percent'],wins_list,.537,'b')
plt.xlabel('Effective Field Goal Percentage')
plt.savefig('wins_vs_effective_field_goal_percentage_by_team.pdf')

plot4 = plt.figure(4)
scatter_trend_line(team_efg_perc['efg_percent'],wins_list,.537,playoff_teams_colors_list)
plt.xlabel('Effective Field Goal Percentage')
blue_patch = mpatches.Patch(color='b', label='Playoffs')
red_patch = mpatches.Patch(color='r', label='Non-Playoffs')
plt.legend(handles=[blue_patch,red_patch],loc='upper left')
plt.savefig('wins_vs_effective_field_goal_percentage_playoff_teams.pdf')
