/**
 * Dragon's Hoard - Main Game Configuration
 * Exports the complete game configuration for the Dragon's Hoard slot game.
 */

import { allSymbols, symbolMap, paytable, highValueSymbols, lowValueSymbols, wildSymbol, scatterSymbol } from './symbols';
import { allReels, baseGameReels, freeGameReels, reelConfig } from './reels';

export interface GameConfig {
  gameId: string;
  gameName: string;
  provider: string;
  version: string;
  rtp: number;
  volatility: 'low' | 'medium' | 'high';
  maxWin: number;
  minBet: number;
  maxBet: number;
  reelLayout: {
    reels: number;
    rows: number;
  };
  symbols: typeof allSymbols;
  reels: typeof allReels;
  paytable: typeof paytable;
  features: GameFeatures;
}

export interface GameFeatures {
  wilds: {
    enabled: boolean;
    symbol: string;
    multiplier: number;
    substitutes: string[];
  };
  scatters: {
    enabled: boolean;
    symbol: string;
    triggers: {
      freeSpins: {
        minSymbols: number;
        awards: Record<number, number>; // number of scatters -> free spins
      };
    };
  };
  freeSpins: {
    enabled: boolean;
    reelSet: string;
    multiplier: number;
    retrigger: boolean;
  };
}

// Main game configuration
export const dragonHoardConfig: GameConfig = {
  gameId: 'dragon-hoard',
  gameName: "Dragon's Hoard",
  provider: 'Stake Engine',
  version: '1.0.0',
  rtp: 0.96,
  volatility: 'medium',
  maxWin: 10000,
  minBet: 0.10,
  maxBet: 100.00,
  reelLayout: {
    reels: 5,
    rows: 3
  },
  symbols: allSymbols,
  reels: allReels,
  paytable: paytable,
  features: {
    wilds: {
      enabled: true,
      symbol: 'W',
      multiplier: 2,
      substitutes: ['H1', 'H2', 'H3', 'H4', 'L1', 'L2', 'L3', 'L4']
    },
    scatters: {
      enabled: true,
      symbol: 'S',
      triggers: {
        freeSpins: {
          minSymbols: 3,
          awards: {
            3: 10,  // 3 scatters = 10 free spins
            4: 15,  // 4 scatters = 15 free spins 
            5: 25   // 5 scatters = 25 free spins
          }
        }
      }
    },
    freeSpins: {
      enabled: true,
      reelSet: 'free',
      multiplier: 1,
      retrigger: true
    }
  }
};

// Game modes
export const gameModes = {
  BASE: 'base',
  FREE: 'free'
} as const;

export type GameMode = typeof gameModes[keyof typeof gameModes];

// Win calculation helpers
export interface WinLine {
  symbols: string[];
  positions: Array<{ reel: number; row: number }>;
  payout: number;
  multiplier: number;
}

export interface GameResult {
  board: string[][];
  wins: WinLine[];
  totalWin: number;
  scatterCount: number;
  freeSpinsAwarded: number;
  mode: GameMode;
}

// Utility functions for game logic
export function calculateWin(symbols: string[], count: number): number {
  const symbol = symbols[0];
  return paytable[symbol]?.[count] || 0;
}

export function countScatters(board: string[][]): number {
  let count = 0;
  for (const reel of board) {
    for (const symbol of reel) {
      if (symbol === scatterSymbol.id) {
        count++;
      }
    }
  }
  return count;
}

export function isWildSymbol(symbol: string): boolean {
  return symbol === wildSymbol.id;
}

export function getSymbolMultiplier(symbol: string): number {
  const symbolObj = symbolMap[symbol];
  return symbolObj?.multiplier || 1;
}

// Export all components
export {
  // Symbols
  allSymbols,
  symbolMap,
  paytable,
  highValueSymbols,
  lowValueSymbols,
  wildSymbol,
  scatterSymbol,
  
  // Reels
  allReels,
  baseGameReels,
  freeGameReels,
  reelConfig
};

// Default export
export default dragonHoardConfig;