# Python Project

This project analyzes trends of 3-point shooting in the NBA and correlates these trends with team success.

There are four directories for this project:

## make_mini_table

This directory is for the purpose of the presentation and makes a small table of 10 rows to show the structure of the .csv files that were used and read in as a Pandas DataFrame

## multi_year_stats

This directory contains year_by_year_stats.py, which uses the .csv files for the 2010-11 season through the 2018-19 season. A figure is created, which displays the percent of shots attempted each year that are 2-pointers and 3-pointers.

## 2018-19_stats

This directory contains 2018-19_wins_correlations.py.
This file reads in the plays from the 2018-19 NBA season. It then groups the plays based on shot type and team.
The 3-point percentage, field goal percentage, and effective field goal percentage of each team is calculated.
These statistics are then correlated with wins for each team and whether each team made the playoffs or not.
Four scatter plots are created:
1) wins versus 3pt percentage for all teams
2) wins versus 3pt percentage for all teams, color coded based on playoff or non-playoff team
3) wins versus effective field goal percentage for all teams
4) wins versus effective field goal percentage for all teams, color coded based on playoff or non-playoff team

## 2019-20_stats

This directory contains two python scripts, the first of which is league_shooting_stats_2019-20.py.
This file reads in the plays from the 2019-20 NBA season and extracts the shot type (2-pt or 3-pt), shot distance, shot outome (make or miss).
It then calculates the field goal percentage and effective field goal percentages for 2-pt and 3-pt shots as a function of shot distance.
Three figures are plotted:
1) the distribution of shot attempts from distances of 0 to 35 feet
2) the distribution of field goal percentages at shot distances from 0 to 40 feet
3) the distribution of effective field goal percentages at shot distances from 0 to 40 feet

The second python script is 2019-20_wins_correlations.py, which does the same analysis and creates the same figures as 2018-19_wins_correlations.py.
However, a single function/script was not created to handle both datasets because the formats of the data files were completely different. They contained different information and the column headings were not the same, so the data needed to be handled and parsed differently.
