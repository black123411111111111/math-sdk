/**
 * Dragon's Hoard - Symbol Definitions
 * Defines the high-value, low-value, wild, and scatter symbols for the game.
 */

export interface Symbol {
  id: string;
  name: string;
  value: number;
  type: 'high' | 'low' | 'wild' | 'scatter';
  multiplier?: number;
}

// High-value symbols - Dragon themed
export const highValueSymbols: Symbol[] = [
  {
    id: 'H1',
    name: 'Dragon',
    value: 500,
    type: 'high'
  },
  {
    id: 'H2', 
    name: 'Golden Crown',
    value: 250,
    type: 'high'
  },
  {
    id: 'H3',
    name: 'Treasure Chest',
    value: 150,
    type: 'high'
  },
  {
    id: 'H4',
    name: 'Ruby Gem',
    value: 100,
    type: 'high'
  }
];

// Low-value symbols - Playing card values
export const lowValueSymbols: Symbol[] = [
  {
    id: 'L1',
    name: 'Ace',
    value: 50,
    type: 'low'
  },
  {
    id: 'L2',
    name: 'King',
    value: 40,
    type: 'low'
  },
  {
    id: 'L3',
    name: 'Queen', 
    value: 30,
    type: 'low'
  },
  {
    id: 'L4',
    name: 'Jack',
    value: 20,
    type: 'low'
  }
];

// Special symbols
export const wildSymbol: Symbol = {
  id: 'W',
  name: 'Dragon Wild',
  value: 0,
  type: 'wild',
  multiplier: 2
};

export const scatterSymbol: Symbol = {
  id: 'S',
  name: 'Dragon Orb',
  value: 0,
  type: 'scatter'
};

// All symbols collection
export const allSymbols: Symbol[] = [
  ...highValueSymbols,
  ...lowValueSymbols,
  wildSymbol,
  scatterSymbol
];

// Symbol mapping for easy lookup
export const symbolMap: Record<string, Symbol> = allSymbols.reduce((map, symbol) => {
  map[symbol.id] = symbol;
  return map;
}, {} as Record<string, Symbol>);

// Paytable - defines win amounts for symbol combinations
export const paytable: Record<string, Record<number, number>> = {
  // High-value symbols (5, 4, 3 of a kind)
  'H1': { 5: 1000, 4: 250, 3: 50 },
  'H2': { 5: 500, 4: 125, 3: 25 },
  'H3': { 5: 300, 4: 75, 3: 15 },
  'H4': { 5: 200, 4: 50, 3: 10 },
  
  // Low-value symbols (5, 4, 3 of a kind)
  'L1': { 5: 100, 4: 25, 3: 5 },
  'L2': { 5: 80, 4: 20, 3: 4 },
  'L3': { 5: 60, 4: 15, 3: 3 },
  'L4': { 5: 40, 4: 10, 3: 2 },
  
  // Wild symbol (acts as any symbol)
  'W': { 5: 2000, 4: 500, 3: 100 },
  
  // Scatter symbol (pay anywhere)
  'S': { 5: 500, 4: 100, 3: 20 }
};