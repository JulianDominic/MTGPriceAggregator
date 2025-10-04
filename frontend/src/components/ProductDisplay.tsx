import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import ProductCard from "@/components/ProductCard";
import { MTGCard } from "@/types";
import { useMemo, useState } from "react";

const ProductDisplay = ({ cards }: { cards: MTGCard[] }) => {
  const [selectedOption, setSelectedOption] = useState("asc");

  const sortedCards = useMemo(() => {
    return [...cards].sort((a, b) => {
      return selectedOption === "asc" 
        ? a.price - b.price 
        : b.price - a.price;
    });
  }, [cards, selectedOption]);

  return (
    sortedCards.length > 0 && <div className="p-4">
      <Select
        value={selectedOption}
        onValueChange={(value) => {
          setSelectedOption(value);
        }}
      >
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Sort by Price" />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectItem value="asc">Ascending ($ to $$$)</SelectItem>
            <SelectItem value="desc">Descending ($$$ to $)</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
      <div className="grid sm:grid-cols-1 md:grid-cols-3 xl:grid-cols-4 gap-4 py-4">
        {sortedCards.map((card, index) => <ProductCard key={index} card={card} />)}
      </div>
    </div>
  );
};

export default ProductDisplay;
