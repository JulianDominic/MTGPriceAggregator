import { Grid } from '@mui/material';
import CardInfo from './CardInfo';

function ProductDisplay({ cards }) {
  return (
    <Grid container spacing={2} marginTop={2}>
      {cards.map((card, index) => (
        <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
          <CardInfo card={card} />
        </Grid>
      ))}
    </Grid>
  );
}

export default ProductDisplay;
