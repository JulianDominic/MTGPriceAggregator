export interface MTGCard {
  name: string,
  set_name: string,
  price: number,
  store: string,
  url: URL
};

interface CardName { id: number, name: string };

export type MasterCardList = CardName[];

export type StoreSelection = {
  [key: string]: boolean
};
