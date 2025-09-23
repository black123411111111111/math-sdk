/**
 * Dragon's Hoard - Reel Definitions
 * Defines the reel strips for the base game and free game modes.
 */

import { Symbol } from './symbols';

export interface ReelStrip {
  id: string;
  name: string;
  symbols: string[];
  mode: 'base' | 'free';
}

// Base game reel strips - 5 reels with varying symbol distributions
export const baseGameReels: ReelStrip[] = [
  {
    id: 'BR1',
    name: 'Base Reel 1',
    mode: 'base',
    symbols: [
      'H1', 'L1', 'L2', 'L3', 'L4', 'H2', 'L1', 'L2', 'L3', 'L4',
      'H3', 'L1', 'L2', 'W', 'L4', 'H4', 'L1', 'L2', 'L3', 'S',
      'H1', 'L1', 'L2', 'L3', 'L4', 'H2', 'L1', 'L2', 'L3', 'L4',
      'H3', 'L1', 'L2', 'L3', 'L4', 'H4', 'L1', 'L2', 'L3', 'L4'
    ]
  },
  {
    id: 'BR2', 
    name: 'Base Reel 2',
    mode: 'base',
    symbols: [
      'H2', 'L1', 'L2', 'L3', 'L4', 'H1', 'L1', 'L2', 'W', 'L4',
      'H4', 'L1', 'L2', 'L3', 'L4', 'H3', 'L1', 'L2', 'L3', 'L4',
      'H2', 'L1', 'S', 'L3', 'L4', 'H1', 'L1', 'L2', 'L3', 'L4',
      'H4', 'L1', 'L2', 'L3', 'L4', 'H3', 'L1', 'L2', 'L3', 'L4'
    ]
  },
  {
    id: 'BR3',
    name: 'Base Reel 3', 
    mode: 'base',
    symbols: [
      'H3', 'L1', 'L2', 'L3', 'L4', 'H2', 'L1', 'L2', 'L3', 'L4',
      'H1', 'L1', 'W', 'L3', 'L4', 'H4', 'L1', 'L2', 'L3', 'L4',
      'H3', 'L1', 'L2', 'L3', 'S', 'H2', 'L1', 'L2', 'L3', 'L4',
      'H1', 'L1', 'L2', 'L3', 'L4', 'H4', 'L1', 'L2', 'L3', 'L4'
    ]
  },
  {
    id: 'BR4',
    name: 'Base Reel 4',
    mode: 'base', 
    symbols: [
      'H4', 'L1', 'L2', 'L3', 'L4', 'H3', 'L1', 'L2', 'L3', 'L4',
      'H2', 'L1', 'L2', 'L3', 'W', 'H1', 'L1', 'L2', 'L3', 'L4',
      'H4', 'L1', 'L2', 'S', 'L4', 'H3', 'L1', 'L2', 'L3', 'L4',
      'H2', 'L1', 'L2', 'L3', 'L4', 'H1', 'L1', 'L2', 'L3', 'L4'
    ]
  },
  {
    id: 'BR5',
    name: 'Base Reel 5',
    mode: 'base',
    symbols: [
      'H1', 'L1', 'L2', 'L3', 'L4', 'H4', 'L1', 'L2', 'L3', 'L4',
      'H3', 'L1', 'L2', 'L3', 'L4', 'H2', 'W', 'L2', 'L3', 'L4',
      'H1', 'L1', 'L2', 'L3', 'L4', 'H4', 'L1', 'S', 'L3', 'L4',
      'H3', 'L1', 'L2', 'L3', 'L4', 'H2', 'L1', 'L2', 'L3', 'L4'
    ]
  }
];

// Free game reel strips - More favorable symbol distributions with increased wilds and high-value symbols
export const freeGameReels: ReelStrip[] = [
  {
    id: 'FR1',
    name: 'Free Reel 1',
    mode: 'free',
    symbols: [
      'H1', 'H2', 'L1', 'L2', 'W', 'H3', 'H4', 'L3', 'L4', 'W',
      'H1', 'H2', 'L1', 'L2', 'L3', 'H3', 'H4', 'L4', 'W', 'S',
      'H1', 'H2', 'L1', 'L2', 'L3', 'H3', 'H4', 'L4', 'W', 'L1',
      'H1', 'H2', 'L1', 'L2', 'L3', 'H3', 'H4', 'L4', 'W', 'L2'
    ]
  },
  {
    id: 'FR2',
    name: 'Free Reel 2', 
    mode: 'free',
    symbols: [
      'H2', 'H1', 'L2', 'L1', 'W', 'H4', 'H3', 'L4', 'L3', 'W',
      'H2', 'H1', 'L2', 'L1', 'L4', 'H4', 'H3', 'L3', 'W', 'L1',
      'H2', 'H1', 'S', 'L1', 'L4', 'H4', 'H3', 'L3', 'W', 'L2',
      'H2', 'H1', 'L2', 'L1', 'L4', 'H4', 'H3', 'L3', 'W', 'L3'
    ]
  },
  {
    id: 'FR3',
    name: 'Free Reel 3',
    mode: 'free',
    symbols: [
      'H3', 'H1', 'L3', 'L1', 'W', 'H2', 'H4', 'L2', 'L4', 'W',
      'H3', 'H1', 'L3', 'L1', 'L2', 'H2', 'H4', 'L4', 'W', 'L1',
      'H3', 'H1', 'L3', 'L1', 'S', 'H2', 'H4', 'L4', 'W', 'L2',
      'H3', 'H1', 'L3', 'L1', 'L2', 'H2', 'H4', 'L4', 'W', 'L4'
    ]
  },
  {
    id: 'FR4',
    name: 'Free Reel 4',
    mode: 'free',
    symbols: [
      'H4', 'H2', 'L4', 'L2', 'W', 'H3', 'H1', 'L3', 'L1', 'W',
      'H4', 'H2', 'L4', 'L2', 'L1', 'H3', 'H1', 'L3', 'W', 'L2',
      'H4', 'H2', 'L4', 'S', 'L1', 'H3', 'H1', 'L3', 'W', 'L3',
      'H4', 'H2', 'L4', 'L2', 'L1', 'H3', 'H1', 'L3', 'W', 'L4'
    ]
  },
  {
    id: 'FR5',
    name: 'Free Reel 5',
    mode: 'free',
    symbols: [
      'H1', 'H3', 'L1', 'L3', 'W', 'H4', 'H2', 'L4', 'L2', 'W',
      'H1', 'H3', 'L1', 'L3', 'L4', 'H4', 'H2', 'L2', 'W', 'L1',
      'H1', 'H3', 'L1', 'L3', 'L4', 'H4', 'H2', 'S', 'W', 'L2',
      'H1', 'H3', 'L1', 'L3', 'L4', 'H4', 'H2', 'L2', 'W', 'L3'
    ]
  }
];

// All reels collection
export const allReels: ReelStrip[] = [
  ...baseGameReels,
  ...freeGameReels
];

// Reel configuration for easy access
export const reelConfig = {
  baseGame: {
    reels: baseGameReels,
    reelCount: 5,
    rowCount: 3
  },
  freeGame: {
    reels: freeGameReels,
    reelCount: 5,
    rowCount: 3
  }
};

// Utility functions
export function getReelById(id: string): ReelStrip | undefined {
  return allReels.find((reel: ReelStrip) => reel.id === id);
}

export function getReelsByMode(mode: 'base' | 'free'): ReelStrip[] {
  return allReels.filter((reel: ReelStrip) => reel.mode === mode);
}

export function getRandomSymbolFromReel(reel: ReelStrip): string {
  const randomIndex = Math.floor(Math.random() * reel.symbols.length);
  return reel.symbols[randomIndex];
}