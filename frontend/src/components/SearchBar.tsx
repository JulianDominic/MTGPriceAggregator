import React, { useState, useMemo } from 'react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
import { MasterCardList, MTGCard, StoreSelection } from '@/types';
import { Button } from './ui/button';
import { LoaderCircle } from 'lucide-react';
import { toast } from 'sonner';
import { searchStores } from '@/api/client';
import { getErrorMessage } from '@/lib/utils';

const SearchBar = ({ masterCardList, selectedStores, setCards } : { masterCardList : MasterCardList, selectedStores : StoreSelection, setCards : React.Dispatch<React.SetStateAction<MTGCard[]>> }) => {
  const [open, setOpen] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const filteredOptions = useMemo(() => {
    if (inputValue.trim() === "") return [];

    const filtered = masterCardList
      .filter((option) =>
        option.name.toLowerCase().includes(inputValue.toLowerCase())
      )
      .sort((a, b) => {
        const aIndex = a.name.toLowerCase().indexOf(inputValue.toLowerCase());
        const bIndex = b.name.toLowerCase().indexOf(inputValue.toLowerCase());
        return aIndex - bIndex;
      });

    return filtered.slice(0, 20);
  }, [inputValue, masterCardList]);

  const handleInputChange = (value : string) => {
    const normalizedValue = value.replace(/[""]/g, "'");
    setInputValue(normalizedValue);
    setOpen(value.trim() !== "");
  };

  const handleSelect = (value : string) => {
    setInputValue(value);
    setOpen(false);
  };

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      if (!inputValue) {
        throw new Error("Card name field cannot be empty.");
      }
      let count = 0;
      for (const store in selectedStores) {
        if (!selectedStores[store]) {
          count++;
        }
      }
      if (count === Object.keys(selectedStores).length) {
        throw new Error("At least one store must be selected");
      }

      const cards = await searchStores(inputValue, Object.keys(selectedStores));
      setCards(cards);
    } catch (err) {
      const errorMsg = getErrorMessage(err);
      toast.error(errorMsg);
      console.error(errorMsg);
    }
    setIsLoading(false);
  };

  return (
    <div className="w-full p-4 flex items-start space-x-6">
      <Command className="rounded-lg border max-h-50">
        <CommandInput
          id="card-name"
          placeholder="Enter a card..."
          value={inputValue}
          onValueChange={handleInputChange}
          onFocus={() => {
            if (inputValue.trim() !== "") setOpen(true);
          }}
        />
        {open && filteredOptions.length > 0 && (
          <CommandList>
            <CommandGroup>
              {filteredOptions.map((option) => (
                <CommandItem
                  key={option.id}
                  value={option.name}
                  onSelect={() => handleSelect(option.name)}
                  className="cursor-pointer"
                >
                  {option.name}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        )}
        {open && inputValue.trim() !== "" && filteredOptions.length === 0 && (
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
          </CommandList>
        )}
      </Command>
      <div>
        <Button className="top-full" onClick={handleSearch}>
          {isLoading ? <LoaderCircle className="animate-spin w-12 h-12" /> : "Search"}
        </Button>
      </div>
    </div>
  );
}

export default SearchBar;
