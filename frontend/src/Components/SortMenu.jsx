import React, { useState } from 'react';
import { Grid, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

function SortMenu({ cards, setCards }) {
  const [sortOrder, setSortOrder] = useState('asc');

  const handleSort = (event) => {
    const order = event.target.value;
    setSortOrder(order);
    const sortedCards = [...cards].sort((a, b) => {
      const priceA = parseFloat(a.price.replace(/[^0-9.-]+/g, ""));
      const priceB = parseFloat(b.price.replace(/[^0-9.-]+/g, ""));
      return order === 'asc' ? priceA - priceB : priceB - priceA;
    });
    setCards(sortedCards);
  };

  return (
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
  );
}

export default SortMenu;
