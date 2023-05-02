"""Classes for the weather app"""
import time
from bs4 import BeautifulSoup
import requests



class Scraper:
    """
    En scraper som hämtar väderdata från yr.no och klart.se
    ...
    Attributes
    ----------
    url : str
        Url:en som ska skrapas
    response : requests.models.Response
        Svaret från url:en
    soup : bs4.BeautifulSoup
        Svaret från url:en i html-format
    Methods
    -------
    fix_url(string)
        Fixar url:en så att den kan skrapas
    fetch_url(url)
        Hämtar url:en och returnerar svaret

    """

    def __init__(self):

        self.url = ""
        self.response = None
        self.soup = None

    def fix_url(self, string):
        string = string.replace("å", "%C3%A5")
        string = string.replace("ä", "%C3%A4")
        string = string.replace("ö", "%C3%B6")
        string = string.replace("æ", "%C3%A6")
        return string

    def fetch_url(self, url):
        while True:
            try:
                self.response = requests.get(url)
                self.response.raise_for_status()
                break
            except requests.exceptions.HTTPError as error:
                print(f"Det uppstod ett fel: {error}")
                print("Försök igen")
                print("")
            except requests.exceptions.ConnectionError as error:
                print(f"Det uppstodp ett fel: {error}")
                print("Försök igen")
                print("")


class Yr(Scraper):
    """
    Tar väderdata från yr.no
    ...
    Attributes
    ----------
    yr_temperature : str
        Temperaturen från yr.no
    yr_condition : str
        Vädret från yr.no
    yr_wind : str
        Vinden från yr.no
    yr_rain : str
        Nederbörden från yr.no
    yr_export : dict
        En dictionary med väderdata från yr.no
    Methods
    -------
    get_yr_weather()
        Hämtar väderdata från yr.no "temp, condition, wind, rain" och returnerar en dictionary med väderdata

    """

    def __init__(self):
        super().__init__()
        self.yr_temperaure = ""
        self.yr_condition = ""
        self.yr_wind = ""
        self.yr_rain = ""
        self.yr_export = {}

    def get_yr_weather(self):
        """
        Hämtar väderdata från yr.no "temp, condition, wind, rain" och returnerar en dictionary med väderdata
        ...
        :param:
        ----------
        self : Yr
            En instans av klassen Yr

        :return:
            En dictionary med väderdata från yr.no
        """
        while True:
            try:
                self.url = self.fix_url(
                    f"https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/2-2701680/Sverige/V%C3%A4rmland/Karlstads%20Kommun/Karlstad")

                self.response = requests.get(self.url)
                self.response.raise_for_status()
                break
            except requests.exceptions.HTTPError as error:
                print(f"Det uppstod ett fel: {error}")
                print("Försök igen")
                print("")
            except requests.exceptions.ConnectionError as error:
                print(f"Det uppstod ett fel: {error}")
                print("Försök igen")
                print("")
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        try:
            self.temp = self.soup.find(class_='temperature temperature--cold').get_text()
        except AttributeError:
            self.temp = self.soup.find(class_='temperature temperature--warm').get_text()
        self.temp = self.soup.find(class_='temperature temperature--warm').get_text()
        self.condition = self.soup.find('img', {'class': 'weather-symbol__img'})['alt']
        self.wind = self.soup.find(class_='wind__value now-hero__next-hour-wind-value').get_text()
        self.rain = self.soup.find(class_='now-hero__next-hour-precipitation-value').get_text()
        self.temp = self.temp[10:]

        self.yr_export = {"Temperatur": self.temp, "Väder": self.condition, "Vind": self.wind,
                          "Nederbörd": self.rain}
        return self.yr_export


class Klart(Scraper):
    """
    Tar väder från klart.se
    ...
    Attributes
    ----------
    klart_temperaure : str
        Temperatur från klart.se
    klart_condition : str
        Väder från klart.se
    klart_wind : str
        Vind från klart.se
    klart_rain : str
        Nederbörd från klart.se
    klart_export : dict
        Dictonary med alla väder som ska skrivas ut


    Methods
    -------
    get_klart_weather()
        Går in på klart.se och hämtar temperatur, väder, vind och nederbörd
            och sen lägger in det i en dictonary

    """

    def __init__(self):
        super().__init__()
        self.klart_temperaure = ""
        self.klart_condition = ""
        self.klart_wind = ""
        self.klart_rain = ""
        self.klart_export = {}

    def get_klart_weather(self):
        """
        Hämtar väderdata från klart.se och lägger in det i en dictonary
        ...
        :param:
        ----------
        None
        -------
        :return:
            klart_export : dict

        """
        while True:
            try:
                self.url = self.fix_url(
                    f"https://klart.se/se/v%C3%A4rmlands-l%C3%A4n/v%C3%A4der-karlstad/")
                self.response = requests.get(self.url)
                self.response.raise_for_status()
                break
            except requests.exceptions.HTTPError as error:
                print(f"Det uppstod ett fel: {error}")
            except requests.exceptions.ConnectionError as error:
                print(f"Det uppstod ett fel: {error}")
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.klart_temperaure = self.soup.find(class_='temp-high').get_text()
        self.klart_condition = self.soup.find('svg', {'aria-label': True})
        self.klart_wind = self.soup.find(class_='item-child wind-value').get_text()
        try:
            self.klart_rain = self.soup.find(class_='item-child rain-value -disabled').get_text()
        except Exception:
            self.klart_rain = self.soup.find(class_='item-child rain-value').get_text()

        # filterar ut prognos
        self.klart_condition = self.klart_condition['aria-label'][8:]
        self.klart_wind = self.klart_wind.strip()
        self.klart_rain = self.klart_rain.strip()

        self.klart_export = {"Temperatur": self.klart_temperaure, "Väder": self.klart_condition,
                             "Vind": self.klart_wind,
                             "Nederbörd": self.klart_rain}
        return self.klart_export


class Gp(Scraper):
    """
    Tar nyhteer från gp.se
    ...
    Attributes
    ----------
    articles : list
        Lista med alla artiklar
    gp_export : list
        Lista med alla artiklar som ska skrivas ut
    gp_news : dict
        Dictonary med alla artiklar som ska skrivas ut
    Methods
    -------
    get_gp_articles()
        Hämtar alla artiklar från gp.se och tar ruktik och ingress från varje artikel
    """

    def __init__(self):
        super().__init__()
        self.articles = ""
        self.gp_export = []
        self.gp_news = {}
        self.number = 1

    def get_gp_articles(self):
        """
        Hämtar alla artiklar från gp.se och tar ruktik och ingress från varje artikel
        ...
        :param:
        ----------
        None
        -------
        :return:
            gp_news : dict

        """
        self.url = "https://www.gp.se"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.articles = self.soup.find_all(class_='c-teaser')

        num_articles = len(self.articles)  # Antal artiklar att hämta
        print(f"Hämtar {num_articles} artiklar från {self.url}\n")

        for article in self.articles:
            try:
                article_link = article.find('a', {"class": "c-teaser__link"})['href']
                article_link = self.url + article_link
            except TypeError:
                continue

            try:
                self.response = requests.get(article_link, allow_redirects=False)
                self.response.raise_for_status()

                soup = BeautifulSoup(self.response.content, 'html.parser')
                article_title = soup.find("h1", class_="c-article__heading").text.strip()
                article_text = soup.find("element").text.strip()
                self.gp_news = {article_title: article_text}
                self.gp_export.append(self.gp_news)
                print(f"Artikel {self.number} av {num_articles}")
                self.number += 1

            except Exception:
                print("fel")
                print(article_link)
                continue

            time.sleep(1)

        print("Done!")
        return self.gp_export


class Aftonbladet(Scraper):
    """
    Tar nyhteer från aftonbladet.se
    ...
    Attributes
    ----------
    articles : list
        Lista med alla artiklar
    aftonbladet_export : list
        Lista med alla artiklar som ska skrivas ut
    aftonbladet_news : dict
        Dictonary med alla artiklar som ska skrivas ut
    Methods
    -------
    get_aftonbladet_articles()
        Hämtar alla artiklar från aftonbladet.se och tar ruktik och ingress från varje artikel


    """

    def __init__(self):
        super().__init__()
        self.articles = ""
        self.aftonbladet_export = []
        self.aftonbladet_news = {}
        self.aftonbladet_ingress = []
        self.number = 1

    def get_aftonbladet_articles(self):
        """
        Hämtar alla artiklar från aftonbladet.se och tar ruktik och ingress från varje artikel
        ...
        :param:
        ----------
        None
        -------
        :return:
            aftonbladet_export : list
        """
        self.url = "https://www.aftonbladet.se/nyheter"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.articles = self.soup.find_all("div", {"class": "hyperion-css-rakwf4"})

        num_articles = len(self.articles)
        print(f"Hämtar {num_articles} artiklar från {self.url}\n")

        for article in self.articles:
            try:
                article_link = article.find('a')['href']
                article_link = self.url + article_link
            except TypeError:
                continue
            response = requests.get(article_link)
            soup = BeautifulSoup(response.content, 'html.parser')

            try:
                article_title = soup.find("h1", {"class": "h1 hyperion-css-5tht1q"}).text.strip()
                paragraphs = soup.find_all("p", {"class": "hyperion-css-n38mho"})
                paragraphs_text = [paragraph.text for paragraph in paragraphs]
                self.aftonbladet_news[article_title] = ''.join(paragraphs_text)
                self.aftonbladet_export.append(self.aftonbladet_news)
                self.aftonbladet_news = {}
                print(f"Artikel {self.number} av {num_articles}")
                self.number += 1

            except Exception:
                print(f"fel i artikel {self.number}")
                continue
            time.sleep(1)

        print("Done!")
        return self.aftonbladet_export
