import aiohttp, asyncio
from lgs import GamesHaven, OneMTG, AgoraHobby, FlagshipGames, CardsCitadel, GreyOgreGames, Hideout, MTGAsia, ScrapeMTG

async def main():
    card_name = input("Name of card: ")
    # Remove AgoraHobby to speed things up. It has the longest loading time.
    sites = [
        GamesHaven,
        OneMTG,
        AgoraHobby,
        FlagshipGames,
        CardsCitadel,
        GreyOgreGames,
        Hideout,
        MTGAsia
        ]
    instances = [site(card_name) for site in sites]

    async def get_cards(client, site_instance:ScrapeMTG):
        print("Fetching for", site_instance.__class__.__name__)
        success = await site_instance.fetch(client)
        print("Finished fetching for", site_instance.__class__.__name__)
        if not(success):
            return None
        return await site_instance.get_card_info()

    async with aiohttp.ClientSession() as client:
        all_store_cards = [get_cards(client, site_instance) for site_instance in instances]
        results = await asyncio.gather(*all_store_cards)
        results = {sites[i]:results[i] for i in range(len(sites))}
        for store,store_cards in results.items():
            if store_cards is not None:
                cheapest_idx = ScrapeMTG.get_cheapest_card(store_cards)
                print(store_cards[cheapest_idx])
            else:
                print(f"{store.__name__} does not have \"{card_name}\".")


if __name__ == "__main__":
    asyncio.run(main())
