import React, { useState } from 'react';
import { Button, CircularProgress } from '@mui/material';
import axios from 'axios';

function SearchButton({ cardName, stores, setError, setCards, endpoint }) {
  const [loading, setLoading] = useState(false);
  const checkStores = () => {
    for (const key in stores) {
      if (stores[key] === true) {
        return true;
      }
    }
    return false;
  }

  const validInput = () => {
    if (!cardName) {
      setError([true, "Please enter a card name."])
      return false;
    }
    // 2. None of the stores have been selected
    if (!checkStores()) {
      setError([true, "Please select a store."])
      return false;
    }
    setError([false, ""])
    return true;
  }

  const handleSearch = async () => {
    if (!validInput()) {
      return;
    }
    const selectedStores = Object.keys(stores).filter((store) => stores[store]);
    // Start the search
    setLoading(true);
    try {
      const response = await axios.post(endpoint, {
        cardName,
        stores: selectedStores
      });
      // Start sorting here because I have an initial state of putting them in an ascending order.
      const sortedCards = response.data.sort((a, b) => {
        const priceA = parseFloat(a.price.replace(/[^0-9.-]+/g, ""));
        const priceB = parseFloat(b.price.replace(/[^0-9.-]+/g, ""));
        return priceA - priceB;
      });
      setCards(sortedCards);
    } catch (err) {
      setError([true, "Failed to fetch cards from the server."]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      variant="contained"
      onClick={handleSearch}
      disabled={loading}
      sx={{ height: "56px" }}
    >
      {loading ? <CircularProgress size={24} /> : 'Search'}
    </Button>
  );
}

export default SearchButton;
