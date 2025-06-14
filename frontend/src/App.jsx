import React, { useEffect, useState } from 'react';
import axios from 'axios';
import * as data from './stores.json'
import { Button, Container, CircularProgress, Typography } from "@mui/material";
import SearchBar from "./Components/SearchBar";
import SearchButton from "./Components/SearchButton";
import StoreSelection from './Components/StoreSelection';
import SortMenu from './Components/SortMenu';
import ProductDisplay from './Components/ProductDisplay';

// Pre-select all of the stores
const stores = data.stores;
const intialSelection = stores.reduce((acc, store) => {
  acc[store] = true;
  return acc;
}, {});
// FastAPI Backend Endpoint
const HOST_IP = import.meta.env.VITE_HOST_IP || "localhost";
const searchEndpoint   = "http://" + HOST_IP + ":10016/search"
const cardListEndpoint = "http://" + HOST_IP + ":10016/all-cards"

function App() {
  const [cardName, setCardName] = useState('');
  const [selectedStores, setSelectedStores] = useState(intialSelection);
  const [error, setError] = useState([false, ""]);
  const [cards, setCards] = useState([]);
  const [masterCardList, setMasterCardList] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    handlePullingCards(false);
  }, []);

  const handleUpdateClick = async () => {
    handlePullingCards(true)
  }

  const handlePullingCards = async (force) => {
    console.log(force);
    try {
      setLoading(true)
      const response = await axios.post(
        cardListEndpoint,
        {
          force
        }
      )
      // console.log(response)
      if (response.data.card_names) {
        setMasterCardList(response.data.card_names);
        console.log("Successfully pulled card names from Scryfall/Backend")
      }
    } catch (err) {
      console.log(err)
    } finally {
      setLoading(false)
    }
  } 

  return (
    <Container
      sx={{
        display: "flex",
        flexDirection: "column",
        alignContent: "center",
        gap: "1em",
      }}
    >
      <Container
        sx={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
          width: "100%",
        }}
      >
        <Typography variant="h4" gutterBottom>
          MTG Price Aggregator
        </Typography>
        <Button
          variant="contained"
          onClick={handleUpdateClick}
          disabled={loading}
          color="success"
        >
          {loading ? <CircularProgress size={24} /> : "Update Master Card List"}
        </Button>
      </Container>
      <Container
        sx={{
          display: "flex",
          flexDirection: "row",
          gap: "1em",
        }}
      >
        <SearchBar cardName={cardName} setCardName={setCardName} error={error} masterCardList={masterCardList} />
        <SearchButton cardName={cardName} stores={selectedStores} setError={setError} setCards={setCards} endpoint={searchEndpoint} />
      </Container>
      <Container>
        <StoreSelection stores={stores} selectedStores={selectedStores} setSelectedStores={setSelectedStores} />
      </Container>
      <Container>
        {cards.length > 0 && <SortMenu cards={cards} setCards={setCards} />}
        <ProductDisplay cards={cards} />
      </Container>
    </Container>
  );
}

export default App;
