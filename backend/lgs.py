import aiohttp
import asyncio
from bs4 import BeautifulSoup, element
from abc import ABC, abstractmethod
from enum import Enum

class LGS(Enum):
    GamesHaven = "GamesHaven"
    OneMTG = "OneMTG"
    AgoraHobby = "AgoraHobby"
    FlagshipGames = "FlagshipGames"
    CardsCitadel = "CardsCitadel"
    GreyOgreGames = "GreyOgreGames"
    Hideout = "Hideout"
    MTGAsia = "MTGAsia"

class ScrapeMTG(ABC):
    @abstractmethod
    async def get_card_info(self):
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
    
    async def fetch(self, client:aiohttp.ClientSession) -> bool:
        async with client.get(self.url) as response:
            self.status_code = response.status
            if self.status_code == 200:
                self.html_data = await response.text()
                return True
            print(f"Failed to retrieve the page. Status code: {self.status_code}")
            return False
        
    def valid_card_name(self, possible_name:str) -> bool:
        # Validate the card name by checking if it's a subset
        # I tried zip(...) but it wouldn't work for a Room card (xx // yy)
        #   it would have worked if you searched xx but not yy
        # Subsets seem to be the only one that supports both right now.
        original_card = set(self.card_name.lower().split())
        possible_name = set(possible_name.lower().split())
        if len(original_card) > len(possible_name):
            return False
        return original_card.issubset(possible_name)
    
    def get_card_name(self, lgs_card:element.Tag=None, name_div:str=None) -> str:
        name = lgs_card.select_one(name_div)
        if name is None:
            return ""
        name = name.text
        # Remove leading and trailing whitespace
        name = name.strip()

        lgs = self.__class__.__name__
        if lgs in [LGS.OneMTG.value, LGS.FlagshipGames.value, LGS.MTGAsia.value, LGS.CardsCitadel.value]:
            # Card Name (AA/Showcase/etc) [SET NAME]
            name = name.split('[')[0]
        elif lgs in [LGS.AgoraHobby.value]:
            # Skip non-English cards
            if name.split()[0].startswith(('[', '【')):
                return ""
        name = name.strip()
        # Check if the name is correct
        if not self.valid_card_name(name):
            return ""

        return name
    
    def get_set_name(self, lgs_card:element.Tag=None, set_name_div:str=None) -> str:
        set_name = lgs_card.select_one(set_name_div)
        if set_name is None:
            return ""
        set_name = set_name.text
        # Remove leading and trailing whitespace
        set_name = set_name.strip()

        lgs = self.__class__.__name__
        if lgs in [LGS.OneMTG.value, LGS.FlagshipGames.value, LGS.MTGAsia.value, LGS.CardsCitadel.value]:
            # Card Name (AA/Showcase/etc) [SET NAME]
            set_name = set_name.split('[')
            # I'm hoping that the "card" isn't a card, otherwise, it shouldn't encounter this block.
            if (len(set_name) < 2):
                print("!!!ERROR: Failed to parse: ")
                print(set_name)
                return ""
            set_name = set_name[1][:-1]
        elif lgs in [LGS.AgoraHobby.value]:
            # [SET NAME] RARITY - CONDITION
            set_name = set_name.split()[0].strip()[1:-1]
        return set_name.strip()
    
    def get_price(self, lgs_card:element.Tag=None, price_div:str=None) -> str:
        price = lgs_card.select_one(price_div)
        if price is None:
            return ""
        price = price.text
        # Remove leading and trailing whitespace
        price.strip()

        lgs = self.__class__.__name__
        if lgs in [LGS.OneMTG.value, LGS.FlagshipGames.value, LGS.MTGAsia.value, LGS.CardsCitadel.value]:
            # $xx.yy -> xx.yy
            price = price[1:]
        elif lgs in [LGS.AgoraHobby.value]:
            # $$xx.yy
            price = price.strip()[2:]
        else:
            # $xx.yy CURRENCY
            price = price.split()[0][1:]
        if lgs in [LGS.CardsCitadel.value]:
            price = price.strip()
            if price == "Varies":
                price = lgs_card.select_one('div.addNow').text.strip().split('$')[1]
            elif price == "Sold Out":
                return ""
            else:
                price = price[1:]
        return price.strip()
    
    def get_availability(self, lgs_card:element.Tag=None, avail_div:str=None) -> bool:
        is_avail = lgs_card.select_one(avail_div)

        lgs = self.__class__.__name__
        if lgs in [LGS.AgoraHobby.value]:
            is_avail = is_avail.get("value")
            # print(is_avail == "Add to Cart")
            return is_avail == "Add to Cart"
        return is_avail != None


class GamesHaven(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        self.url = f"https://www.gameshaventcg.com/search?q=*{self.card_name}*"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')

        card_divs = soup.select("div.productCard__card")
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "button.button--primary")
            if not is_avail:
                continue
            name = self.get_card_name(card, "p.productCard__title")
            set_name = self.get_set_name(card, "p.productCard__setName")
            price = self.get_price(card, "p.productCard__price")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards


class OneMTG(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        self.url = f"https://onemtg.com.sg/search?q=*{self.card_name}*"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')
        
        card_divs = soup.select("div.product-description")
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "a.nm-addToCart")
            if not is_avail:
                continue
            name = self.get_card_name(card, "div.product-detail div.grid-view-item__title")
            set_name = self.get_set_name(card, "div.product-detail div.grid-view-item__title")
            price = self.get_price(card, "span.product-price__price")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards


class AgoraHobby(ScrapeMTG):
    def __init__(self, card_name):
        self.card_name = card_name
        self.url = f"https://agorahobby.com/store/search?category=mtg&searchfield={self.card_name}&search=GO"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')

        card_divs = soup.select('div#store_listingcontainer div.store-item')
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "input.addtocart")
            if not is_avail:
                continue
            name = self.get_card_name(card, "div.store-item-title")
            set_name = self.get_set_name(card, "div.store-item-cat")
            price = self.get_price(card, "div.store-item-price")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards
    

class FlagshipGames(ScrapeMTG):
    def __init__(self, card_name):
        self.card_name = card_name
        self.url = f"https://www.flagshipgames.sg/search?q={self.card_name}"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')

        card_divs = soup.select('div.list-view-items.products-display div.product-card-list2')
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "a.nm-addToCart")
            if not is_avail:
                continue
            name = self.get_card_name(card, "div.product-detail")
            set_name = self.get_set_name(card, "div.product-detail")
            price = self.get_price(card, "span.product-price__price.is-bold.qv-regularprice")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards


class CardsCitadel(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        self.url = f"https://cardscitadel.com/search?q=*{card_name}*"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')

        card_divs = soup.select('div.col-lg-9 div.product.Norm')
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "span.addBtn")
            if not is_avail:
                continue
            name = self.get_card_name(card, "p.productTitle")
            set_name = self.get_set_name(card, "p.productTitle")
            price = self.get_price(card, "p.productPrice")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards
    

class GreyOgreGames(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        self.url = f"https://www.greyogregames.com/search?q=*{self.card_name}*"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')

        card_divs = soup.select('div.collectionGrid div.productCard__card')
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "button.button--primary")
            if not is_avail:
                continue
            name = self.get_card_name(card, "p.productCard__title")
            set_name = self.get_set_name(card, "p.productCard__setName")
            price = self.get_price(card, "p.productCard__price")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards


class Hideout(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        self.url = f"https://hideoutcg.com/search?q=*{card_name}*"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')

        card_divs = soup.select('div.productCard__card')
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "button.button--primary")
            if not is_avail:
                continue
            name = self.get_card_name(card, "p.productCard__title")
            set_name = self.get_set_name(card, "p.productCard__setName")
            price = self.get_price(card, "p.productCard__price")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards

class MTGAsia(ScrapeMTG):
    def __init__(self, card_name:str):
        self.card_name = card_name
        self.url = f"https://www.mtg-asia.com/search?q=*{self.card_name}*"

    async def get_card_info(self):
        soup = BeautifulSoup(self.html_data, 'html.parser')
        
        card_divs = soup.select("div.products-display div.product-card-list2")
        cards = []
        for card in card_divs:
            is_avail = self.get_availability(card, "a.nm-addToCart")
            if not is_avail:
                continue
            name = self.get_card_name(card, "div.grid-view-item__title")
            set_name = self.get_set_name(card, "div.grid-view-item__title")
            price = self.get_price(card, "span.product-price__price")
            if name and price and set_name:
                cards.append({
                    "name": name,
                    "set_name": set_name,
                    "price": price,
                    "store": self.__class__.__name__,
                    "url": self.url,
                })
        if not cards:
            return None
        return cards
