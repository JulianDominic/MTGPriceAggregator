import React, { useState } from 'react';
import {
  Container,
  TextField,
  Button,
  Typography,
  Grid,
  CircularProgress,
  FormControlLabel,
  Checkbox,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import axios from 'axios';
import CardInfo from './CardInfo.jsx';

const stores = [
  { label: 'GamesHaven', value: 'GamesHaven' },
  { label: 'OneMTG', value: 'OneMTG' },
  { label: 'AgoraHobby', value: 'AgoraHobby' },
  { label: 'FlagshipGames', value: 'FlagshipGames' },
  { label: 'CardsCitadel', value: 'CardsCitadel' },
  { label: 'GreyOgreGames', value: 'GreyOgreGames' },
  { label: 'Hideout', value: 'Hideout' }
];

function App() {
  const [cardName, setCardName] = useState('');
  const [selectedStores, setSelectedStores] = useState({});
  const [loading, setLoading] = useState(false);
  const [cards, setCards] = useState([]);
  const [error, setError] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');

  const handleStoreChange = (store) => {
    setSelectedStores({ ...selectedStores, [store.value]: !selectedStores[store.value] });
  };

  const handleSearch = async () => {
    // Validation Checks
    if (!cardName) {
      setError('Card name is required');
      return;
    }

    const selectedStoreKeys = Object.keys(selectedStores).filter(store => selectedStores[store]);
    if (selectedStoreKeys.length === 0) {
      setError('At least one store must be selected');
      return;
    }

    // Start the search
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://YOUR_IP:10016/search', {
        cardName,
        stores: selectedStoreKeys
      });
      // Start sorting here because I have an initial state of putting them in an ascending order.
      const sortedCards = response.data.sort((a, b) => {
        const priceA = parseFloat(a.price.replace(/[^0-9.-]+/g, ""));
        const priceB = parseFloat(b.price.replace(/[^0-9.-]+/g, ""));
        return priceA - priceB;
      });
      setCards(sortedCards);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch card data.');
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (e) => {
    const order = e.target.value;
    setSortOrder(order);
    const sortedCards = [...cards].sort((a, b) => {
      const priceA = parseFloat(a.price.replace(/[^0-9.-]+/g, ""));
      const priceB = parseFloat(b.price.replace(/[^0-9.-]+/g, ""));
      return order === 'asc' ? priceA - priceB : priceB - priceA;
    });
    setCards(sortedCards);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        MTG Price Aggregator
      </Typography>
      <TextField
        label="Card Name"
        value={cardName}
        onChange={(e) => setCardName(e.target.value)}
        fullWidth
        margin="normal"
        error={!cardName && error === 'Card name is required'}
        helperText={!cardName && error === 'Card name is required' ? 'Please enter a card name' : ''}
      />
      <Grid container spacing={2} marginTop={2}>
        {stores.map((store, index) => (
          <Grid item key={index}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={selectedStores[store.value] || false}
                  onChange={() => handleStoreChange(store)}
                />
              }
              label={store.label}
            />
          </Grid>
        ))}
      </Grid>
      {error && error !== 'Card name is required' && (
        <Typography color="error" gutterBottom>{error}</Typography>
      )}
      <Button variant="contained" color="primary" onClick={handleSearch} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : 'Search'}
      </Button>
      {cards.length > 0 && (
        // Load the sort button only if there are cards available. Otherwise, it is meaningless.
        <Grid container spacing={2} marginTop={2}>
          <Grid item>
            <FormControl variant="outlined" style={{ minWidth: 200 }}>
              <InputLabel>Sort by Price</InputLabel>
              <Select
                value={sortOrder}
                onChange={handleSort}
                label="Sort by Price"
              >
                <MenuItem value="asc">Low to High</MenuItem>
                <MenuItem value="desc">High to Low</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      )}
      {/* Put the cards in a grid */}
      <Grid container spacing={2} marginTop={2}>
        {cards.map((card, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <CardInfo card={card} />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default App;
