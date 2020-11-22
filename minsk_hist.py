import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mcp import CovidParsers as cp
from mcp import StatsPlotter as sp
from mcp import CovidDb as cdb
from mcp import TextInfoWriter as tiw
from mcp import MinskDistrictInfo as minfo
from mcp import SafetyThresholds as st
import locale

MINISK_CSV = 'data/minsk.csv'
DB_PATH = 'data/covid.db'
FB_PATH = 'fb'
IMAGES_FOLDER = 'images'

locale.setlocale(locale.LC_ALL, 'pl_PL')

download_new_data = False
db_ctx = cdb.CovidDb(DB_PATH)
if db_ctx.table_exists():
    stats = db_ctx.getStats()
    if stats.index.max() < datetime.date.today():
        download_new_data = True

else:
    download_new_data = True

if download_new_data:
    print("FETCHING NEW DATA")
    parser = cp.MinskPSSEParser()
    stats = parser.fetch_data()
    stats['aktywni'] = stats['potwierdzeni'] - stats['ozdrowieńcy'] - stats['zmarli']
    db_ctx.insertStats(stats)

db_ctx.close()

stats = stats[~stats.index.duplicated()]
idx = pd.date_range(min(stats.index), max(stats.index))
stats = stats.reindex(idx, fill_value=-1)


last_index_with_value = None
for index, row in stats.iterrows():
    if last_index_with_value is not None:
        day_diff = (index - last_index_with_value).days
        if day_diff > 1:
            for i, p in enumerate(['kwarantanna', 'hospitalizowani', 'potwierdzeni', 'ozdrowieńcy', 'zmarli', 'aktywni']):
                last_v = stats.loc[last_index_with_value, p]
                current_v = stats.loc[index, p]
                stats.loc[last_index_with_value:index, p] = np.linspace(last_v, current_v, day_diff+1)
    if row[0] != -1:
        last_index_with_value = index
    else:
        continue

plotter = sp.BasePlotter(stats.last('31D'))
plotter.generate_plot()

msg = tiw.TextInfoWriter(stats, minfo.MinskDistrictInfo(), st.PolishThresholds()).get_facebook_msg()
with open(os.path.join(FB_PATH, 'info.txt'), 'w') as f:
    f.write(msg)

plt.savefig(os.path.join(IMAGES_FOLDER, 'active.png'))
plt.savefig(os.path.join(IMAGES_FOLDER, 'active.svg'))
plt.show()
