const BACKEND_IP = import.meta.env.VITE_HOST_IP || "localhost";
export const BACKEND_URL = `http://${BACKEND_IP}:10016`;

export const getMasterCardList = async (force : boolean) => {
  const response = await fetch(`${BACKEND_URL}/cards/all?force=${force}`);
  const cardList = await response.json();
  return cardList.card_names;
};

export const searchStores = async (cardName : string, stores : string[]) => {
  const response = await fetch(`${BACKEND_URL}/search`, {
    headers: {
      "Content-Type": "application/json"
    },
    method: "POST",
    body: JSON.stringify({
      cardName,
      stores
    }),
  });
  const cardList = await response.json();
  return cardList.cards;
};
