import { useState } from "react";
import ProductCard from "./components/ProductCard";
import * as stores from "@/assets/stores.json"
import Header from "./components/Header";

function App() {
  const [selectedStores, setSelectedStores] = useState(stores.stores);
  const [cards, setCards] = useState([
    {name: "name1", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
    {name: "name2", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
    {name: "name3", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
    {name: "name4", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
  ]);

  return (
    <>
      <Header />
      <div className="grid sm:grid-cols-1 md:grid-cols-3 xl:grid-cols-4 gap-4 p-4">
        {cards && cards.map((card, index) => <ProductCard key={index} card={card}/>)}
      </div>
    </>
  )
}

export default App
