import React, { useState } from 'react';
import * as data from './stores.json'
import { Container, Typography } from "@mui/material";
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

function Test() {
  const [cardName, setCardName] = useState('');
  const [selectedStores, setSelectedStores] = useState(intialSelection);
  const [error, setError] = useState([false, ""]);
  const [cards, setCards] = useState([]);

  return (
    <Container
      sx={{
        display: "flex",
        flexDirection: "column",
        alignContent: "center",
        gap: "1em",
      }}
    >
      <Container>
        <Typography variant="h4" gutterBottom>
          MTG Price Aggregator
        </Typography>
      </Container>
      <Container
        sx={{
          display: "flex",
          flexDirection: "row",
          gap: "1em",
        }}
      >
        <SearchBar cardName={cardName} setCardName={setCardName} error={error} />
        <SearchButton cardName={cardName} stores={selectedStores} setError={setError} setCards={setCards} />
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

export default Test;
