import datetime as dt

class TextInfoWriter:
    def __init__(self, stats, district_info, thresholds):
        self.stats = stats
        self.info = district_info
        self.thresholds = thresholds

    def get_last_7D_diff(self, col_name):
        last_8D = self.stats[col_name].last('8D')
        return last_8D[-1] - last_8D[0]

    def get_facebook_msg(self):
        ill = self.get_last_7D_diff('potwierdzeni')
        healed = self.get_last_7D_diff('ozdrowieńcy')
        mean_confirmed = round(ill / (self.info.POPULATION / 100_000) / 7, 2)
        threshold, col = self.thresholds.get_level(mean_confirmed)

        msg = f'''[{dt.date.today().strftime("%d.%m.%Y")}]
Statystyki za ostatnie 7 dni:
- zachorowało: {ill:.0f}
- wyzdrowiało: {healed:.0f}

Lokalny estymator progu bezpieczeństwa: {mean_confirmed} ==> kolor {col} 

===============================

,,Lokalny estymator progu bezpieczeństwa'' to średnia liczba zachorowań na 100 tys. osób / 7 dni dla powiatu. 
(Na podstawie progów krajowych https://twitter.com/PremierRP/status/1323980694033489923)

aktywni = potwierdzeni - ozdrowieńcy - zgony

===============================
Źródło danych: http://minsk.psse.waw.pl/4786 
Dane zbierane ze strony metodą web scraping'u.'''
        return msg