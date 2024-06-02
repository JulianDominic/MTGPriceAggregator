import requests, os
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class ScrapeMTG(ABC):
    @abstractmethod
    def get_card_info(self, status_code:int):
        pass

    @staticmethod
    def get_cheapest_card(cards:list[dict]) -> int:
        if cards is None:
            return None
        prices = dict()
        for idx,card in enumerate(cards):
            price = card["price"]
            if ',' in price:
                price = price.split(',')
                price = float(price[0]) * 1000 + float(price[1])
            prices[float(price)] = idx
        lowest_idx = prices[min([i for i in prices.keys()])]
        return lowest_idx


class GamesHaven(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        print(f"Processing for {self.__class__.__name__}")
        self.url = f"https://www.gameshaventcg.com/search?page=1&q=*{self.card_name}*"
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code
    

    def get_card_info(self, status_code:int):
        if status_code == 200:
            html_data = self.response.content
            soup = BeautifulSoup(html_data, 'html.parser')

            card_divs = soup.select('div.collectionGrid div.productCard__card')
            cards = []
            for card in card_divs:
                try:
                    name = card.select_one('p.productCard__title').text.strip()
                    if name.split('(')[0].lower().strip() != self.card_name.lower().strip():
                        continue
                    set_name = card.select_one('p.productCard__setName').text.strip()
                    price = card.select_one('p.productCard__price').text.strip()[1:].split()[0]
                    try:
                        availability_button = card.select_one('button.product-item__action-button.productCard__button.button--primary')
                        if availability_button is None:
                            break
                    except AttributeError:
                        break
                    card_info = {
                        "name": name,
                        "set_name": set_name,
                        "price": price,
                        "store": "GamesHaven",
                        "url": self.url,
                    }
                    cards.append(card_info)
                except:
                    continue
            if not cards:
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {self.response.status_code}")
            return None
        return cards


class OneMTG(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        print(f"Processing for {self.__class__.__name__}")
        self.url = f"https://onemtg.com.sg/search?q=*{self.card_name}*"
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code


    def get_card_info(self, status_code: int):
        if status_code == 200:
            html_data = self.response.content
            soup = BeautifulSoup(html_data, 'html.parser')

            card_divs = soup.select('div.col-lg-9 div.product.Norm')
            cards = []
            for card in card_divs:
                try:
                    name = card.select_one('p.productTitle').text.strip()
                    name, set_name = [i.strip() for i in name.split('[')]
                    if name.split('(')[0].lower().strip() != self.card_name.lower().strip():
                        continue
                    set_name = set_name[:-1].strip()
                    price = card.select_one('p.productPrice').text.strip()[1:].split()[0]
                    if price == "old":
                        continue
                    if price == "aries":  # would be "varies" but there's the [1:]
                        price = card.select_one('div.addNow').text.strip().split('$')[1]
                    try:
                        availability_button = card.select_one('span.addBtn')
                        if availability_button is None:
                            break
                    except AttributeError:
                        break
                    card_info = {
                        "name": name,
                        "set_name": set_name,
                        "price": price,
                        "store": "OneMTG",
                        "url": self.url,
                    }
                    cards.append(card_info)
                except:
                    continue
            if not cards:
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {status_code}")
            return None
        return cards


class AgoraHobby(ScrapeMTG):
    def __init__(self, card_name):
        self.card_name = card_name
        print(f"Processing for {self.__class__.__name__}")
        self.url = f"https://agorahobby.com/store/search?category=mtg&searchfield={self.card_name}&search=GO"
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code


    def get_card_info(self, status_code: int):
        if status_code == 200:
            html_data = self.response.content
            soup = BeautifulSoup(html_data, 'html.parser')

            card_divs = soup.select('div#store_listingcontainer div.store-item')
            cards = []
            for card in card_divs:
                try:
                    name = card.select_one('div.store-item-title').text.strip()
                    if name.split()[0].startswith(('[', '【')):  # Skips non-english cards
                        continue
                    elif not(set([i.lower() for i in self.card_name.split()]).issubset(set([i.lower() for i in name.split()]))):
                        continue
                    set_name = card.select_one('div.store-item-cat').text.split()[0].strip()[1:-1]
                    price = card.select_one('div.store-item-price').text.strip()[1:].split()[0][1:]
                    availability_button = card.select_one('input.button.button-item-buy.addtocart').get('value')
                    if availability_button is None:
                        break
                    if availability_button != "Add to Cart":
                        continue
                    card_info = {
                        "name": name,
                        "set_name": set_name,
                        "price": price,
                        "store": "Agora",
                        "url": self.url,
                    }
                    cards.append(card_info)
                except:
                    continue
            if not cards:
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {status_code}")
            return None
        return cards
    

class FlagshipGames(ScrapeMTG):
    def __init__(self, card_name):
        self.card_name = card_name
        print(f"Processing for {self.__class__.__name__}")
        self.url = f"https://www.flagshipgames.sg/search?type=product&options%5Bprefix%5D=last&q={self.card_name}"
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code


    def get_card_info(self, status_code: int):
        if status_code == 200:
            html_data = self.response.content
            soup = BeautifulSoup(html_data, 'html.parser')

            card_divs = soup.select('div.list-view-items.products-display div.product-card-list2')
            cards = []
            for card in card_divs:
                try:
                    name = card.select_one('div.product-detail').text.strip()
                    name, set_name = [i.strip() for i in name.split('[')]
                    if name.split('(')[0].lower().strip() != self.card_name.lower().strip():
                        continue
                    set_name = set_name[:-1].strip()
                    price = card.select_one('span.product-price__price.is-bold.qv-regularprice').text.strip()[1:]
                    try:
                        availability_button = card.select_one('a.nm-addToCart.addToCart.enable.btn')
                        if availability_button is None:
                            break
                    except AttributeError:
                        break
                    card_info = {
                        "name": name,
                        "set_name": set_name,
                        "price": price,
                        "store": "FlagshipGames",
                        "url": self.url,
                    }
                    cards.append(card_info)
                except:
                    continue
            if not cards:
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {self.response.status_code}")
            return None
        return cards

class CardsCitadel(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        print(f"Processing for {self.__class__.__name__}")
        self.url = f"https://cardscitadel.com/search?q=*{card_name}*"
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code


    def get_card_info(self, status_code: int):
        if status_code == 200:
            html_data = self.response.content
            soup = BeautifulSoup(html_data, 'html.parser')

            card_divs = soup.select('div.col-lg-9 div.product.Norm')
            cards = []
            for card in card_divs:
                try:
                    name = card.select_one('p.productTitle').text.strip()
                    name, set_name = [i.strip() for i in name.split('[')]
                    if name.split('(')[0].lower().strip() != self.card_name.lower().strip():
                        continue
                    set_name = set_name[:-1].strip()
                    price = card.select_one('p.productPrice').text.strip()[1:].split()[0]
                    if price == "old":
                        continue
                    if price == "aries":  # would be "varies" but there's the [1:]
                        price = card.select_one('div.addNow').text.strip().split('$')[1]
                    try:
                        availability_button = card.select_one('span.addBtn')
                        if availability_button is None:
                            break
                    except AttributeError:
                        break
                    card_info = {
                        "name": name,
                        "set_name": set_name,
                        "price": price,
                        "store": "CardsCitadel",
                        "url": self.url,
                    }
                    cards.append(card_info)
                except:
                    continue
            if not cards:
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {status_code}")
            return None
        return cards
    

class GreyOgreGames(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        print(f"Processing for {self.__class__.__name__}")
        self.url = f"https://www.greyogregames.com/search?page=1&q=*{self.card_name}*"
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code
    

    def get_card_info(self, status_code:int):
        if status_code == 200:
            html_data = self.response.content
            soup = BeautifulSoup(html_data, 'html.parser')

            card_divs = soup.select('div.collectionGrid div.productCard__card')
            cards = []
            for card in card_divs:
                try:
                    name = card.select_one('p.productCard__title').text.strip()
                    if name.split('(')[0].lower().strip() != self.card_name.lower().strip():
                        continue
                    set_name = card.select_one('p.productCard__setName').text.strip()
                    price = card.select_one('p.productCard__price').text.strip()[1:].split()[0]
                    try:
                        availability_button = card.select_one('button.product-item__action-button.productCard__button.button--primary')
                        if availability_button is None:
                            break
                    except AttributeError:
                        break
                    card_info = {
                        "name": name,
                        "set_name": set_name,
                        "price": price,
                        "store": "GreyOgreGames",
                        "url": self.url,
                    }
                    cards.append(card_info)
                except:
                    continue
            if not cards:
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {self.response.status_code}")
            return None
        return cards


class Hideout(ScrapeMTG):
    def __init__(self, card_name):
        self.card_name = card_name
        print(f"Processing for {self.__class__.__name__}")
        self.url = f"https://www.hideout-online.com/search?type=product&options%5Bprefix%5D=last&q={self.card_name}"
        self.response = requests.get(self.url)
        self.status_code = self.response.status_code


    def get_card_info(self, status_code: int):
        if status_code == 200:
            html_data = self.response.content
            soup = BeautifulSoup(html_data, 'html.parser')

            card_divs = soup.select('div.list-view-items.products-display div.product-card-list2')
            cards = []
            for card in card_divs:
                try:
                    name = card.select_one('div.product-detail').text.strip()
                    name, set_name = [i.strip() for i in name.split('[')]
                    if name.split('(')[0].lower().strip() != self.card_name.lower().strip():
                        continue
                    set_name = set_name[:-1].strip()
                    price = card.select_one('span.product-price__price.is-bold.qv-regularprice').text.strip()[1:]
                    try:
                        availability_button = card.select_one('a.nm-addToCart.addToCart.enable.btn')
                        if availability_button is None:
                            break
                    except AttributeError:
                        break
                    card_info = {
                        "name": name,
                        "set_name": set_name,
                        "price": price,
                        "store": "Hideout",
                        "url": self.url,
                    }
                    cards.append(card_info)
                except:
                    continue
            if not cards:
                return None
        else:
            print(f"Failed to retrieve the page. Status code: {self.response.status_code}")
            return None
        return cards


def main():
    main_flag = True
    while main_flag:
        card_name = input("Name of card: ")
        # Remove AgoraHobby to speed things up. It has the longest loading time.
        sites = [GamesHaven, OneMTG, AgoraHobby, FlagshipGames, CardsCitadel, GreyOgreGames, Hideout]
        instances = [site(card_name) for site in sites]

        for site_instance in instances:
            site_instance:ScrapeMTG
            cards = site_instance.get_card_info(site_instance.status_code)
            if cards is not None:
                cheapest_idx = site_instance.get_cheapest_card(cards)
                if cheapest_idx is None:
                    print(f"\"{card_name}\" is unavailable on {site_instance.__class__.__name__}.")
                else:
                    print(cards[cheapest_idx])
        
        # Check with the user if they want to search for another card
        end_flag = True
        while end_flag:
            end = input("\n\nIs there another card you would like to check? (Y/n) ")
            if end.lower() in ["y", ""]:
                # Clear the screen/terminal
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            elif end.lower() == "n":
                end_flag = False
                main_flag = False
            else:
                print("Invalid option.")


if __name__ == "__main__":
    main()
