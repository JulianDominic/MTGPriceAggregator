import { TextField } from '@mui/material';

function SearchBar({ cardName, setCardName, error }) {
  return (
      <TextField
        label="Card Name"
        value={cardName}
        onChange={(e) => setCardName(e.target.value.replace(/[’‘]/g, "'"))}
        fullWidth
        variant="outlined"
        error={error[0]}
        helperText={error[1]}
      />
  );
}

export default SearchBar;
