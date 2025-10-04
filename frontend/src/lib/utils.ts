import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const getErrorMessage = (err:unknown) => {
  if (err instanceof Error) {
    return err.message;
  }
  return String(err);
};
