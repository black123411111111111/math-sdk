/**
 * Dragon's Hoard - Demo Usage Example
 * Demonstrates how to use the Dragon's Hoard game configuration
 */

import dragonHoardConfig, { 
  allSymbols, 
  baseGameReels, 
  freeGameReels, 
  calculateWin, 
  countScatters,
  GameResult,
  GameMode,
  gameModes
} from './index';

// Example: Display game information
console.log(`Game: ${dragonHoardConfig.gameName}`);
console.log(`Game ID: ${dragonHoardConfig.gameId}`);
console.log(`RTP: ${dragonHoardConfig.rtp * 100}%`);
console.log(`Volatility: ${dragonHoardConfig.volatility}`);
console.log(`Max Win: ${dragonHoardConfig.maxWin}x`);

// Example: Show available symbols
console.log('\nAvailable Symbols:');
allSymbols.forEach(symbol => {
  console.log(`${symbol.id}: ${symbol.name} (${symbol.type})`);
});

// Example: Show reel configuration
console.log('\nBase Game Reels:');
baseGameReels.forEach(reel => {
  console.log(`${reel.id}: ${reel.symbols.length} symbols`);
});

console.log('\nFree Game Reels:');
freeGameReels.forEach(reel => {
  console.log(`${reel.id}: ${reel.symbols.length} symbols`);
});

// Example: Simulate a simple game board
function simulateBoard(mode: GameMode): string[][] {
  const reels = mode === gameModes.BASE ? baseGameReels : freeGameReels;
  const board: string[][] = [];
  
  for (let i = 0; i < 5; i++) {
    const reel = reels[i];
    const reelColumn: string[] = [];
    
    // Pick 3 consecutive symbols from a random position
    const startPos = Math.floor(Math.random() * reel.symbols.length);
    for (let j = 0; j < 3; j++) {
      const symbolIndex = (startPos + j) % reel.symbols.length;
      reelColumn.push(reel.symbols[symbolIndex]);
    }
    
    board.push(reelColumn);
  }
  
  return board;
}

// Example: Display a simulated board
console.log('\nSimulated Base Game Board:');
const baseBoard = simulateBoard(gameModes.BASE);
for (let row = 0; row < 3; row++) {
  const rowSymbols = baseBoard.map(reel => reel[row]).join(' | ');
  console.log(`Row ${row + 1}: ${rowSymbols}`);
}

// Example: Check for scatters
const scatterCount = countScatters(baseBoard);
console.log(`\nScatter symbols found: ${scatterCount}`);

if (scatterCount >= 3) {
  const freeSpinsAwarded = dragonHoardConfig.features.scatters.triggers.freeSpins.awards[scatterCount];
  console.log(`Free spins awarded: ${freeSpinsAwarded}`);
}

// Example: Show paytable for high-value symbols
console.log('\nPaytable (High Value Symbols):');
console.log('Symbol | 3 of a kind | 4 of a kind | 5 of a kind');
console.log('-------|-------------|-------------|------------');
['H1', 'H2', 'H3', 'H4'].forEach(symbolId => {
  const symbol = allSymbols.find(s => s.id === symbolId);
  const pays = dragonHoardConfig.paytable[symbolId];
  if (symbol && pays) {
    console.log(`${symbol.name.padEnd(6)} | ${pays[3].toString().padStart(11)} | ${pays[4].toString().padStart(11)} | ${pays[5].toString().padStart(11)}`);
  }
});

// Example: Feature configuration
console.log('\nFeature Configuration:');
console.log(`Wild Symbol: ${dragonHoardConfig.features.wilds.symbol} (multiplier: ${dragonHoardConfig.features.wilds.multiplier}x)`);
console.log(`Scatter Symbol: ${dragonHoardConfig.features.scatters.symbol}`);
console.log(`Free Spins: ${dragonHoardConfig.features.freeSpins.enabled ? 'Enabled' : 'Disabled'}`);

export { dragonHoardConfig };