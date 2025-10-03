import { ModeToggle } from "./mode-toggle";

const Header = () => {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center justify-between px-4">
        <span className="font-bold">MTG Price Aggregator</span>
        <ModeToggle />
      </div>
    </header>
  );
};

export default Header;
