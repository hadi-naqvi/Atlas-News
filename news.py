from newsapi import NewsApiClient
import csv

api = NewsApiClient(api_key = "7f5f126f9cd847afb855a8989b87e4a4")

####################################################################################################################################################################
list_of_countries = {
    "United Arab Emirates": "ae", "Argentina": "ar", "Austria": "at", "Australia": "au", "Belgium": "be",
    "Bulgaria": "bg", "Brazil": "br", "Canada": "ca", "Switzerland": "ch", "China": "cn",
    "Colombia": "co", "Cuba": "cu", "Czech Republic": "cz", "Germany": "de", "Egypt": "eg",
    "France": "fr", "Gabon": "gb", "Greece": "gr", "Hong Kong": "hk", "Hungary": "hu", "Indonesia": "id",
    "Ireland": "ie", "Israel": "il", "India": "in", "Italy": "it", "Japan": "jp", "Korea": "kr",
    "Lithuania": "lt", "Latvia": "lv", "Morocco": "ma", "Mexico": "mx", "Malaysia": "my", "Nigeria": "ng",
    "Netherlands": "nl", "Norway": "no", "New Zealand": "nz", "Philippines": "ph", "Poland": "pl",
    "Portugal": "pt", "Romania": "ro", "Serbia": "rs", "Russia": "ru", "Saudi Arabia": "sa", "Sweden": "se",
    "Singapore": "sg", "Slovenia": "si", "Slovakia": "sk", "Thailand": "th", "Turkey": "tr", "Taiwan": "tw",
    "Ukraine": "ua", "United States": "us", "Venezuela": "ve", "South Africa": "za"
}

def search(query: str, country =None, sources=None, lang= "en"):
    """

    :param query:
    :return: The articles that are related to the query
    """

    # Returns the articles sorted by popularity
    articles = api.get_everything(q= query, sources= sources, language = lang, sort_by="relevancy", page_size = 25)
    return articles

def upload(articles_list):

    # Opens the file test.csv to begin writing the csv file
    with open('test.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        articles = articles_list["articles"]

        # Makes the header
        writer.writerow(["Title", "Url", "Num of Likes", "Num of Dislikes", "Image URL", "Date Published", "Source"])

        # Iterates through the articles and writes them into the csv file
        for article in articles:
            writer.writerow([article["title"],article['url'], 0, 0, article['urlToImage'], article['publishedAt'], article['source']["name"]])


def uploadHome(articles_list):
    # Opens the file test.csv to begin writing the csv file
    with open('test.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        articles = articles_list

        # Makes the header
        writer.writerow(["Title", "Url", "Num of Likes", "Num of Dislikes", "Image URL", "Date Published", "Source"])

        # Iterates through the articles and writes them into the csv file
        for article in articles:
            writer.writerow([article["title"], article['url'], 0, 0, article['urlToImage'], article['publishedAt'],
                             article['source']["name"]])

def homepage():
    # Iterates through the list of countries and finds the top news from the country
    for country in list_of_countries:
        list_of_countries[country] = api.get_top_headlines(q=country,country=list_of_countries[country], page_size=1)
        list_of_countries[country]["articles"]["country"] = country
    return list_of_countries

def getCountryNews(country):
    """

    :param country:
    :return: Returns the top news for the given country
    """
    articles = api.get_top_headlines(q=country, country= list_of_countries[country], page_size=25)
    for article in articles["articles"]:
        article["country"] = country
    return articles
