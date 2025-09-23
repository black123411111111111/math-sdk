# Dragon's Hoard - Slot Game Math Model

This directory contains the mathematical foundation for the "Dragon's Hoard" slot game, implemented in TypeScript.

## Overview

Dragon's Hoard is a 5-reel, 3-row slot game with a dragon fantasy theme featuring:
- High-value symbols: Dragon, Golden Crown, Treasure Chest, Ruby Gem
- Low-value symbols: Ace, King, Queen, Jack
- Wild symbol: Dragon Wild (substitutes for all symbols except scatter, 2x multiplier)
- Scatter symbol: Dragon Orb (triggers free spins)

## Files

### `symbols.ts`
Defines all game symbols, their values, types, and the paytable:
- Symbol interfaces and types
- High-value and low-value symbol definitions
- Wild and scatter symbol configurations
- Complete paytable with win amounts for 3, 4, and 5 of a kind

### `reels.ts`
Contains the reel strip definitions for both game modes:
- Base game reels (5 reels with standard symbol distribution)
- Free game reels (5 reels with enhanced symbol distribution)
- Utility functions for reel manipulation
- Reel configuration objects

### `index.ts`
Main configuration file that exports the complete game setup:
- Game configuration interface
- Feature definitions (wilds, scatters, free spins)
- Utility functions for win calculations
- Complete game configuration object

### `demo.ts`
Example implementation showing how to use the game configuration:
- Game information display
- Board simulation
- Scatter detection
- Paytable presentation

## Game Features

### Wild Symbol (W - Dragon Wild)
- Substitutes for all paying symbols
- Applies 2x multiplier to wins
- Does not substitute for scatter symbols

### Scatter Symbol (S - Dragon Orb)
- Triggers free spins when 3 or more appear anywhere on the reels
- Awards:
  - 3 scatters = 10 free spins
  - 4 scatters = 15 free spins
  - 5 scatters = 25 free spins

### Free Spins Feature
- Uses enhanced reel sets with more favorable symbol distribution
- Can be retriggered during free spins
- Maintains same paytable as base game

## Game Statistics

- **RTP (Return to Player)**: 96%
- **Volatility**: Medium
- **Maximum Win**: 10,000x bet
- **Minimum Bet**: $0.10
- **Maximum Bet**: $100.00
- **Reel Layout**: 5 reels × 3 rows

## Usage

```typescript
import dragonHoardConfig, { 
  allSymbols, 
  baseGameReels, 
  paytable 
} from './index';

// Access game configuration
console.log(dragonHoardConfig.gameName); // "Dragon's Hoard"
console.log(dragonHoardConfig.rtp); // 0.96

// Access symbols
console.log(allSymbols.length); // Total number of symbols

// Access reels
console.log(baseGameReels[0].symbols); // First reel symbol array
```

## TypeScript Configuration

The module includes a `tsconfig.json` file configured for ES2017+ features. To compile:

```bash
tsc --project .
```

To validate without compilation:

```bash
tsc --noEmit --project .
```

## Symbol IDs Reference

### High-Value Symbols
- `H1`: Dragon (highest paying)
- `H2`: Golden Crown
- `H3`: Treasure Chest
- `H4`: Ruby Gem

### Low-Value Symbols
- `L1`: Ace
- `L2`: King
- `L3`: Queen
- `L4`: Jack

### Special Symbols
- `W`: Wild (Dragon Wild)
- `S`: Scatter (Dragon Orb)

## Reel Set IDs

### Base Game
- `BR1` to `BR5`: Base game reels 1-5

### Free Game
- `FR1` to `FR5`: Free game reels 1-5

This mathematical model provides the foundation for implementing the Dragon's Hoard slot game in any gaming platform that supports TypeScript/JavaScript.