import { MasterCardList } from "@/types";
import { ModeToggle } from "./mode-toggle";
import UpdateCards from "./UpdateCardList";

const Header = ({ setMasterCardList } : { setMasterCardList : React.Dispatch<React.SetStateAction<MasterCardList>> }) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center justify-between px-4">
        <span className="font-bold">MTG Price Aggregator</span>
        <div className="flex items-center space-x-6">
          <UpdateCards setMasterCardList={setMasterCardList}/>
          <ModeToggle />
        </div>
      </div>
    </header>
  );
};

export default Header;
