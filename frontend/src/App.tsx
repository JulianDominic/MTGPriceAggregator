import { useState } from "react";
import ProductCard from "@/components/ProductCard";
import * as stores from "@/assets/stores.json"
import Header from "@/components/Header";
import SearchBar from "@/components/SearchBar";
import { MasterCardList, MTGCard } from "@/types";

function App() {
  const [masterCardList, setMasterCardList] = useState<MasterCardList>([]);
  const [selectedStores, setSelectedStores] = useState<string[]>(stores.stores);
  const [cards, setCards] = useState<MTGCard[]>([]);

  return (
    <>
      <Header setMasterCardList={setMasterCardList}/>
      <SearchBar masterCardList={masterCardList} selectedStores={selectedStores} setCards={setCards}/>
      <div className="grid sm:grid-cols-1 md:grid-cols-3 xl:grid-cols-4 gap-4 p-4">
        {cards && cards.map((card, index) => <ProductCard key={index} card={card} />)}
      </div>
    </>
  )
}

export default App
