import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import matplotlib.dates as mdates
import pandas as pd


class BasePlotter:
    def __init__(self, stats):
        self.stats = stats

    def generate_plot(self):
        sns.set(rc={'figure.figsize': (10, 6)})
        sns.set_style("whitegrid")
        fig, axs = plt.subplots(1, 2)
        plt.title('\n')
        plt.suptitle(f'Covid-19 w powiecie mińskim [{self.stats.index.max().date().strftime("%d.%m.%Y")}]\n'
                     f'Źródło danych: http://minsk.psse.waw.pl/', fontsize=14)

        self._plot_active(axs[1])
        self._plot_day_changes(axs[0])

    def _plot_active(self, ax):
        ax.plot(self.stats.index, self.stats["aktywni"], 'bo-', label='Aktywni')
        ax.set_ylabel('Aktywni')
        ax.legend(loc='upper left')
        self._format_asies(ax, self.stats['aktywni'])
        self._add_last_day_dot(ax, self.stats['aktywni'])

    def _plot_day_changes(self, ax):
        new_cases = self.stats['potwierdzeni'].diff()
        ax.plot(self.stats.index, new_cases, 'ro-', label='Potwierdzeni')
        self._add_last_day_dot(ax, new_cases)

        healed = self.stats['ozdrowieńcy'].diff()
        ax.plot(self.stats.index, healed, 'bo-', label='Ozdrowieńcy')
        self._add_last_day_dot(ax, healed)

        ax.legend(loc='upper left')
        y_max = max(healed.max(), new_cases.max())
        ax.set_ylabel('Dzienna zmiana')
        self._format_asies(ax, new_cases, y_max=y_max)

    def _add_last_day_dot(self, ax, series):
        last_X = self.stats.index.max()
        last_y = series[last_X]
        # ax.plot([last_X], [last_y], 'bo')
        label = "{:.0f}".format(last_y)
        ax.annotate(label,
                    (last_X, last_y),
                    textcoords="offset points",
                    xytext=(5, 10),
                    ha='center')

    def _format_asies(self, ax, series, y_max=None):
        ax.set_xlabel('Data')
        locator = mdates.AutoDateLocator(minticks=5, maxticks=5)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.set_xlim(self.stats.index.min(), self.stats.index.max() + pd.DateOffset(days=4))
        if not y_max:
            y_max = series.max()
        ax.set_ylim(0, 1.1 * y_max)
