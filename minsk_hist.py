import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd

from mcp.CovidParsers import MinskPSSEParser
from mcp.StatsPlotter import BasePlotter
from mcp.CovidDb import CovidDb

MINISK_CSV = 'data/minsk.csv'
DB_PATH = 'data/covid.db'
IMAGES_FOLDER = 'images'


download_new_data = False
db_ctx = CovidDb(DB_PATH)
if db_ctx.table_exists():
    stats = db_ctx.getStats()
    if stats.index.max() < datetime.date.today():
        download_new_data = True

else:
    download_new_data = True

if download_new_data:
    print("FETCHING NEW DATA")
    parser = MinskPSSEParser()
    stats = parser.fetch_data()
    stats['aktywni'] = stats['potwierdzeni'] - stats['ozdrowieńcy'] - stats['zmarli']
    db_ctx.insertStats(stats)

db_ctx.close()
plotter = BasePlotter(stats.last('3M'))

plotter.plot_active()

plt.savefig(os.path.join(IMAGES_FOLDER, 'active.png'))
plt.savefig(os.path.join(IMAGES_FOLDER, 'active.svg'))
plt.show()
