import datetime as dt


class TextInfoWriter:
    def __init__(self, stats, district_info):
        self.stats = stats
        self.info = district_info

    def get_facebook_msg(self):
        last_4D = self.stats['potwierdzeni'].last('4D')
        last_15D = self.stats['potwierdzeni'].last('15D')
        last_3D_diff = last_4D[-1] - last_4D[0]
        last_14D_diff = last_15D[-1] - last_15D[0]

        msg = f'''[{dt.date.today().strftime("%d.%m.%Y")}]
Potwierdzone zachorowania w ostatnich dniach:
  3 dni: {last_3D_diff:.0f}
14 dni: {last_14D_diff:.0f}

aktywni = potwierdzeni - ozdrowieńcy - zgony

===============================
Źródło danych: http://minsk.psse.waw.pl/4786 
Dane zbierane ze strony metodą web scraping'u.'''
        return msg