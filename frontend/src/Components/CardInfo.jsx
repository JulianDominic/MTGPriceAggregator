import React from 'react';
import { Container, Card, CardContent, Typography, Button, CardHeader, CardActions } from '@mui/material';

function CardInfo({ card }) {
  return (
    <Card sx={{
      borderRadius: "0.5em",
      height: "240px",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between"
    }}>
      <CardHeader
        title={card.name}
        sx={{
          height: "97px"
        }}
      />
      <CardContent sx={{
        paddingTop: 0,
      }}>
        <Typography variant="body1" color="textSecondary">
          Set: {card.set_name}
        </Typography>
        <Typography variant="body1">
          Price: ${card.price}
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Store: {card.store}
        </Typography>
      </CardContent>
      <CardActions>
        <Container>
          <Button
            onClick={() => window.open(card.url)}
            variant="contained"
            sx={{ width: "100%" }}
          >
            Shop
          </Button>
        </Container>
      </CardActions>
    </Card>
  );
}

export default CardInfo;
