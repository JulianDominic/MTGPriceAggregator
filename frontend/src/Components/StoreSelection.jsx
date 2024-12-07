import {
  Grid,
  Checkbox,
  FormControlLabel,
  useMediaQuery,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
} from '@mui/material';

function StoreSelection({ stores, selectedStores, setSelectedStores }) {
  const isMobile = !useMediaQuery("(min-width:400px)")

  const handleSelect = (event) => {
    const storeName = isMobile ? event.target.value : event.target.name;
    setSelectedStores({
      ...selectedStores,
      [storeName]: !selectedStores[storeName],
    });
  }

  return isMobile ? (
    <FormControl fullWidth>
      <InputLabel>Select Store</InputLabel>
      <Select
        multiple
        value={[]}
        onChange={handleSelect}
        displayEmpty
      >
        {stores.map((store, index) => (
          <MenuItem value={store} key={index}>
            <Checkbox checked={selectedStores[store]} />
            {store}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  ) :(
    <Grid container>
      {stores.map((store, index) => (
        <Grid item
          key={index}
          sx={{
            width: "165px",
          }}
        >
          <FormControlLabel
            control={
              <Checkbox
                name={store}
                checked={selectedStores[store]}
                onChange={handleSelect}
              />
            }
            label={store}
          />
        </Grid>
      ))}
    </Grid>
  );
}

export default StoreSelection;
