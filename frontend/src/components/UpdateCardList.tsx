import { useEffect, useState } from "react";
import { Button } from "./ui/button";
import { LoaderCircle } from "lucide-react";
import { toast } from "sonner"
import { MasterCardList } from "@/types";
import { getMasterCardList } from "@/api/client";

const UpdateCards = ({ setMasterCardList } : { setMasterCardList : React.Dispatch<React.SetStateAction<MasterCardList>> }) => {
  const [isLoading, setIsLoading] = useState(false);

  const updateCardList = async (force : Boolean) => {
    setIsLoading(true);
    try {
      const masterCardList = await getMasterCardList(force);
      setMasterCardList(masterCardList);
    } catch (err) {
      toast.error("Failed to update card list");
      console.error(err);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    updateCardList(false);
  }, []);

  const handleClick = async () => {
    await updateCardList(true);
  };

  return (
    <Button onClick={handleClick} className="min-w-35">
      {isLoading ? <LoaderCircle className="animate-spin w-12 h-12" /> : "Update Card List"}
    </Button>
  );
};

export default UpdateCards;
