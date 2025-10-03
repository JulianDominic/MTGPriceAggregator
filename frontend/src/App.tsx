import { useState } from "react";
import ProductCard from "@/components/ProductCard";
import * as stores from "@/assets/stores.json"
import Header from "@/components/Header";
import SearchBar from "@/components/SearchBar";
import { MasterCardList, MTGCard, StoreSelection } from "@/types";
import StoreSelect from "./components/StoreSelect";

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
      <div className="grid sm:grid-cols-1 md:grid-cols-3 xl:grid-cols-4 gap-4 p-4">
        {cards && cards.map((card, index) => <ProductCard key={index} card={card} />)}
      </div>
    </>
  )
}

export default App
