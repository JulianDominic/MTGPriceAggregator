import { TextField, Typography } from '@mui/material';
import { Container } from '@mui/system';

function SearchBar({ cardName, setCardName, error }) {
  return (
    <Container sx={{ width: "100%" }} disableGutters>
      <TextField
        label="Card Name"
        value={cardName}
        onChange={(e) => setCardName(e.target.value.replace(/[’‘]/g, "'"))}
        fullWidth
        variant="outlined"
      />
      {error[0] ? <Typography variant="subtitle2" color="error">{error[1]}</Typography> : <Typography>{"\n"}</Typography>}
    </Container>
  );
}

export default SearchBar;
