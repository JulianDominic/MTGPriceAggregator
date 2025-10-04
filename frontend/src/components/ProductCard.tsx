import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import type { MTGCard } from "@/types";

const ProductCard = ({ card } : { card : MTGCard }) => {
  return (
    <Card className="w-full max-w-sm min-w-xxs">
      <CardHeader>
        <CardTitle>{card.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <CardDescription>Set: {card.set_name}</CardDescription>
        <CardDescription>Store: {card.store}</CardDescription>
        <p>Price: ${card.price}</p>
      </CardContent>
      <CardFooter>
        <Button className="w-full" onClick={() => {window.open(card.url, "_blank")}}>
          Buy Now
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;
