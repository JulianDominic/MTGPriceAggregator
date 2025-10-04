import { useState } from "react";
import * as stores from "@/assets/stores.json"
import Header from "@/components/Header";
import SearchBar from "@/components/SearchBar";
import { MasterCardList, MTGCard, StoreSelection } from "@/types";
import StoreSelect from "@/components/StoreSelect";
import ProductDisplay from "@/components/ProductDisplay";

const intialSelection = stores.stores.reduce((acc, store) => {
  acc[store] = true;
  return acc;
}, {} as StoreSelection);

function App() {
  const [masterCardList, setMasterCardList] = useState<MasterCardList>([]);
  const [selectedStores, setSelectedStores] = useState<StoreSelection>(intialSelection);
  const [cards, setCards] = useState<MTGCard[]>([]);

  return (
    <>
      <Header setMasterCardList={setMasterCardList}/>
      <SearchBar masterCardList={masterCardList} selectedStores={selectedStores} setCards={setCards}/>
      <StoreSelect selectedStores={selectedStores} setSelectedStores={setSelectedStores}/>
      <ProductDisplay cards={cards} />
    </>
  )
}

export default App
