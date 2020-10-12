import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import matplotlib.dates as mdates
import pandas as pd


class BasePlotter:
    def __init__(self, stats):
        self.stats = stats

    def plot_active(self):
        sns.set(rc={'figure.figsize': (10, 6)})
        sns.set_style("whitegrid")
        fig, ax = plt.subplots()
        ax = sns.lineplot(x=self.stats.index, y=self.stats["aktywni"], ax=ax)

        last_X = self.stats.index.max()
        last_y = self.stats['aktywni'][last_X]
        plt.plot([last_X], [last_y], 'bo')

        ax.set_title(f'Aktywne przypadki covid-19 w powiecie mińskim\n Dane z dnia {last_X.date().strftime("%d.%m.%Y")}')
        ax.text(1, 0, 'Źródło danych: http://minsk.psse.waw.pl/ ', fontsize=12, color='black',
                horizontalalignment='right',
                verticalalignment='bottom',
                transform=ax.transAxes)

        plt.ylabel('Aktywni')
        plt.xlabel('Data')
        locator = mdates.AutoDateLocator(minticks=9, maxticks=15)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        ax.set_xlim(self.stats.index.min(), self.stats.index.max() + pd.DateOffset(days=4))
        ax.set_ylim(0, 1.1 * self.stats['aktywni'].max())
        plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)

        label = "{:.0f}".format(last_y)
        plt.annotate(label,
                     (last_X, last_y),
                     textcoords="offset points",
                     xytext=(5, 10),
                     ha='center')

        ax.grid(True)
