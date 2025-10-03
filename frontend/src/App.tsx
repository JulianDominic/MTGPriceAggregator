import { useState } from "react";
import ProductCard from "./components/ProductCard";

function App() {
  const [cards, setCards] = useState([
    {name: "name1", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
    {name: "name2", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
    {name: "name3", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
    {name: "name4", price: 1.30, set_name: "set name", store: "store", url: new URL("https://youtube.com")},
  ]);

  return (
    <>
      <div className="grid sm: grid-cols-1 md:grid-cols-3 gap-4 p-4">
        {cards.map((card) => <ProductCard card={card}/>)}
      </div>
    </>
  )
}

export default App
