const BACKEND_IP = import.meta.env.VITE_HOST_IP || "localhost";
export const BACKEND_URL = `http://${BACKEND_IP}:10016`;

export const getMasterCardList = async (force : boolean) => {
  const response = await fetch(`${BACKEND_URL}/cards/all?force=${force}`);
  if (!response.ok) {
    throw new Error(`Update failed: ${response.statusText}`);
  }
  const cardList = await response.json();
  return cardList.card_names;
};

export const searchStores = async (cardName : string, stores : string[]) => {
  const searchParams = new URLSearchParams({
    card_name: cardName
  });
  
  stores.forEach(store => searchParams.append("stores", store));
  
  const response = await fetch(`${BACKEND_URL}/search?${searchParams}`);
  if (!response.ok) {
    throw new Error(`Search failed: ${response.statusText}`);
  }
  const cardList = await response.json();
  return cardList.cards;
};
