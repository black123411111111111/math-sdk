// Main exports for the Stake Engine Web SDK

// Core classes
export { RGSClient } from './lib/rgs-client.js';
export { GameStateManager } from './lib/game-state.js';
export { GameController } from './lib/game-controller.js';

// Types
export type * from './types/rgs.js';

// Utilities
export * from './lib/utils.js';

// Version
export const VERSION = '1.0.0';

// Default API multiplier constant
export const DEFAULT_API_MULTIPLIER = 1000000;