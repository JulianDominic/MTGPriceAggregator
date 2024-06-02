import React from 'react';
import { Card, CardContent, Typography, Button } from '@mui/material';

function CardInfo({ card }) {
  return (
    <Card sx={{ borderRadius: "1em" }}>
      <CardContent>
        <Typography variant="h6">
          {card.name}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Set: {card.set_name}
        </Typography>
        <Typography variant="body1">
          Price: ${card.price}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Store: {card.store}
        </Typography>
        <Button 
          onClick={() => window.open(card.url)}
          variant="contained"
        >
          Shop
        </Button>
      </CardContent>
    </Card>
  );
}

export default CardInfo;
