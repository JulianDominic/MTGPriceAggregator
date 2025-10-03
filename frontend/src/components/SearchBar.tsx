import React, { useState, useMemo } from 'react';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
import { MasterCardList, MTGCard } from '@/types';
import { Button } from './ui/button';
import { LoaderCircle } from 'lucide-react';
import { toast } from 'sonner';
import { searchStores } from '@/api/client';

const SearchBar = ({ masterCardList, selectedStores, setCards } : { masterCardList : MasterCardList, selectedStores : string[], setCards : React.Dispatch<React.SetStateAction<MTGCard[]>> }) => {
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
      const cards = await searchStores(inputValue, selectedStores);
      setCards(cards);
    } catch (err) {
      toast.error("Failed to get cards");
      console.error(err);
    }
    setIsLoading(false);
  };

  return (
    <div className="w-full p-4 flex items-center space-x-6">
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
      <Button className="top-full" onClick={handleSearch}>
        {isLoading ? <LoaderCircle className="animate-spin w-12 h-12" /> : "Search"}
      </Button>
    </div>
  );
}

export default SearchBar;
