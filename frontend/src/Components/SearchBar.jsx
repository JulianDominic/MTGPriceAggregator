import { Autocomplete, TextField, Typography } from '@mui/material';
import { Container } from '@mui/system';

function SearchBar({ cardName, setCardName, error, masterCardList }) {
  return (
    <Container sx={{ width: "100%" }} disableGutters>
      <Autocomplete
        freeSolo
        options={masterCardList}
        inputValue={cardName}
        // Typing change
        onInputChange={(e, newValue) => setCardName(newValue.replace(/[’‘]/g, "'"))}
        // Select from menu change
        onChange={(e, newValue) => { if (newValue) {setCardName(newValue)} }}
        // Don't show master list if the user hasn't typed anything
        filterOptions={(options, { inputValue }) => {
          if (inputValue.trim() === "") return [];
          const filtered = options
            .filter((option) =>
              option.toLowerCase().includes(inputValue.toLowerCase())
            )
            .sort((a, b) => {
              const aIndex = a.toLowerCase().indexOf(inputValue.toLowerCase());
              const bIndex = b.toLowerCase().indexOf(inputValue.toLowerCase());
              return aIndex - bIndex;
            });
          return filtered.splice(0, 20);
        }}
        // Limit how many are shown
        ListboxProps={{
          style: { maxHeight: 100, overflowY: "auto" }
        }}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Card Name"
            value={cardName}
            fullWidth
            variant="outlined"
            error={error[0]}
            helperText={error[0] ? error[1] : ""}
          />
        )}
      />
      {/* {error[0] ? <Typography variant="subtitle2" color="error">{error[1]}</Typography> : <Typography>{"\n"}</Typography>} */}
    </Container>
  );
}

export default SearchBar;
