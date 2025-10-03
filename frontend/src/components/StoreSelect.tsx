import { StoreSelection } from "@/types";
import { Checkbox } from "./ui/checkbox";
import { Label } from "./ui/label";
import { CheckedState } from "@radix-ui/react-checkbox";

const StoreSelect = ({ selectedStores, setSelectedStores } : { selectedStores : StoreSelection, setSelectedStores : React.Dispatch<React.SetStateAction<StoreSelection>> }) => {
  const handleSelect = (event: React.ChangeEvent<any>) => {
    setSelectedStores(
      {
        ...selectedStores,
        [event.target.id]: !selectedStores[event.target.id],
      }
    );
  };
  
  return (
    <div className="grid grid-cols-2 gap-4 md:flex md:flex-row md:items-center md:space-x-4 p-4">
      {Object.keys(selectedStores).map((store) => {
        return (
          <div key={store} className="flex items-center gap-3">
            <Checkbox id={store} onClick={handleSelect} checked={selectedStores[store] as CheckedState}/>
            <Label htmlFor="terms">{store}</Label>
          </div>
        );
      })
      }
    </div>
  );

};

export default StoreSelect;
