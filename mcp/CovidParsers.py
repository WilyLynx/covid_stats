import re

import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame
from requests import request


class MinskPSSEParser:
    def __init__(self, url='http://minsk.psse.waw.pl/4786'):
        self._fetch_url = url

    def fetch_data(self) -> DataFrame:
        messages = self._get_messages()
        covid_stats = self._extract_stats(messages)
        covid_stats = self._build_data_frame(covid_stats)
        return covid_stats

    @staticmethod
    def _build_data_frame(covid_stats):
        covid_stats = pd.DataFrame(covid_stats,
                                   columns=['data', 'kwarantanna', 'hospitalizowani', 'potwierdzeni', 'ozdrowieńcy', 'zmarli'])
        covid_stats.loc[:, 'data'] = pd.to_datetime(covid_stats['data'], format='%d.%m.%Y')
        covid_stats: DataFrame = covid_stats.set_index('data').sort_index(ascending=True)
        return covid_stats

    def _get_messages(self):
        site = request('GET', self._fetch_url).content
        soup = BeautifulSoup(site, 'html.parser')
        articles = soup \
            .find_all('div', {'class': 'article_inside'})[0] \
            .find_all('div', {'class': 'ce_text'})
        filer_text = 'powiatu mińskiego związaną z koronawirusem'
        messages = [msg for msg in articles if filer_text in str(msg)]
        return messages

    @staticmethod
    def _extract_stats(messages):
        data = []
        for msg in messages:
            try:
                msg_data = []
                # date
                if len(msg.find_all('h3')) > 0:
                    header = msg.find_all('h3')[0]
                else:
                    header = msg.find_all('em')[0]
                match = re.search('\d{2}\.\d{2}\.\d{4}', str(header))
                date = match.group(0)
                msg_data.append(date)

                # features
                rows = msg.find('ul').find_all('li')
                try:
                    msg_data.append(int([r for r in rows if 'kwarantanną' in str(r)][0].contents[3].contents[0]))
                except Exception:
                    msg_data.append(None)

                try:
                    msg_data.append(int([r for r in rows if 'hospitalizowanych ' in str(r)][0].contents[3].contents[0]))
                except Exception:
                    msg_data.append(None)

                try:
                    msg_data.append(int([r for r in rows if 'potwierdzonych' in str(r)][0].contents[3].contents[0]))
                except Exception:
                    msg_data.append(None)

                try:
                    row = str([r for r in rows if 'ozdrowieńców' in str(r)][0])
                    num = re.search('[0-9]+', row)[0]
                    msg_data.append(int(num))
                except Exception:
                    msg_data.append(None)

                try:
                    msg_data.append(int([r for r in rows if 'zgonów' in str(r)][0].contents[3].contents[0]))
                except Exception:
                    msg_data.append(None)

                data.append(msg_data)
            except Exception:
                pass
        return data
