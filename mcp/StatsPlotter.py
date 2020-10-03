import matplotlib.pyplot as plt
import seaborn as sns
import datetime
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
        ax.set_title(f'Aktywne przypadki covid-19 w powiecie mińskim\n Dane z dnia {datetime.date.today()}')
        ax.text(1, 0, 'Źródło danych: http://minsk.psse.waw.pl/ ', fontsize=12, color='black',
                horizontalalignment='right',
                verticalalignment='bottom',
                transform=ax.transAxes)


        ax.set_xlim(self.stats.index.min(), self.stats.index.max() + pd.DateOffset(days=4))
        ax.set_ylim(0, 1.1 * self.stats['aktywni'].max())
        plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)

        label = "{:.2f}".format(last_y)
        plt.annotate(label,
                     (last_X, last_y),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

        ax.grid(True)
        fig.autofmt_xdate()
