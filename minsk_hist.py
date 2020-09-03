import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd

from mcp.CovidParsers import MinskPSSEParser
from mcp.StatsPlotter import BasePlotter

MINISK_CSV = 'data/minsk.csv'
IMAGES_FOLDER = 'images'


download_new_data = False
if os.path.exists(MINISK_CSV):
    stats = pd.read_csv(MINISK_CSV)
    stats.loc[:, 'data'] = pd.to_datetime(stats['data'], format='%Y-%m-%d')
    stats = stats.set_index('data')
    if stats.index[0] < datetime.date.today():
        download_new_data = True

else:
    download_new_data = True

if download_new_data:
    print("FETCHING NEW DATA")
    parser = MinskPSSEParser()
    stats = parser.fetch_data()
    stats['aktywni'] = stats['potwierdzeni'] - stats['ozdrowieńcy']
    stats.to_csv(MINISK_CSV)

plotter = BasePlotter(stats)

plotter.plot_active()

plt.savefig(os.path.join(IMAGES_FOLDER, 'active.png'))
plt.savefig(os.path.join(IMAGES_FOLDER, 'active.svg'))
plt.show()
