import { useState } from "react";
import { Button } from "./ui/button";
import { LoaderCircle } from "lucide-react";
import { BACKEND_URL } from "@/api/constants";
import { toast } from "sonner"

const UpdateCards = () => {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async () => {
    setIsLoading(true);
    try {
      await fetch(`${BACKEND_URL}/all-cards`, {
        method: "POST",
        body: JSON.stringify({ force: true }),
      });
    } catch (err) {
      toast.error("Failed to update card list");
      console.error(err);
    }
    setIsLoading(false);
  };

  return (
    <Button onClick={handleClick}>
      {isLoading ? <LoaderCircle className="animate-spin w-12 h-12" /> : "Update Card List"}
    </Button>
  );
};

export default UpdateCards;
