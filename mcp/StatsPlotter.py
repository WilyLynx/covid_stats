import matplotlib.pyplot as plt
import seaborn as sns
import datetime


class BasePlotter:
    def __init__(self, stats):
        self.stats = stats

    def plot_active(self):
        sns.set(rc={'figure.figsize': (11, 6)})
        sns.set_style("whitegrid")
        ax = sns.lineplot(x=self.stats.index, y=self.stats["aktywni"])
        ax.set_title(f'Aktywne przypadki covid-19 w powiecie mińskim\n Dane z dnia {datetime.date.today()}')
        ax.text(1, 0, 'Źródło danych: http://minsk.psse.waw.pl/ ', fontsize=12, color='black',
                horizontalalignment='right',
                verticalalignment='bottom',
                transform=ax.transAxes)
        plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)
