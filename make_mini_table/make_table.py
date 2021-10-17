'''This file creates a small table, which shows the first 10 rows of one of the Pandas DataFrames used.
It is for the presentation only, just to display the csv file structures that were used.
'''

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

all_stats = pd.read_csv('../../python_project_csv_files/2018-19_pbp.csv', header = [0])
pd.set_option("display.max_columns", None)
some_stats = all_stats[['PERIOD','HOMEDESCRIPTION','VISITORDESCRIPTION','PLAYER1_NAME','PLAYER1_TEAM_ABBREVIATION']]
some_stats = some_stats.head(10)
some_stats

fig, ax =plt.subplots(figsize=(12,8))
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=some_stats.values,colLabels=some_stats.columns,loc='center')

pp = PdfPages("mini_df_example.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()
