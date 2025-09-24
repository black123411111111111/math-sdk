# Stake Engine Web SDK

The Stake Engine Web SDK provides a TypeScript/JavaScript library for integrating web frontends with the Stake Engine RGS (Remote Game Server).

## Features

- **TypeScript Support**: Full type definitions for all RGS API endpoints
- **State Management**: Built-in game state management with reactive updates
- **Error Handling**: Comprehensive error handling and timeout management
- **Utilities**: Helper functions for common gaming operations
- **Framework Agnostic**: Works with any JavaScript framework (React, Vue, Svelte, etc.)

## Installation

```bash
npm install @stake-engine/web-sdk
```

## Quick Start

### Basic Usage

```typescript
import { GameController } from '@stake-engine/web-sdk';

// Initialize the game controller
const gameController = new GameController({
  baseUrl: 'https://your-rgs-server.com',
  sessionId: 'player-session-id',
  language: 'en',
  currency: 'USD'
});

// Initialize the session
await gameController.initialize();

// Place a bet
await gameController.placeBet(100, 'BASE'); // 100 credits

// End the round (if there's a win)
await gameController.endRound();
```

### State Management

```typescript
// Subscribe to game state changes
const unsubscribe = gameController.getStateManager().subscribe((state) => {
  console.log('Game state:', state.state);
  console.log('Balance:', state.balance);
  console.log('Current round:', state.currentRound);
  console.log('Last win:', state.lastWin);
});

// Check game state
const stateManager = gameController.getStateManager();
if (stateManager.canPlay()) {
  // Player can place a bet
}
if (stateManager.needsEndRound()) {
  // Player needs to end the current round
}
```

### Direct RGS Client Usage

```typescript
import { RGSClient } from '@stake-engine/web-sdk';

const client = new RGSClient({
  baseUrl: 'https://your-rgs-server.com',
  sessionId: 'player-session-id'
});

// Authenticate
const authResponse = await client.authenticate();
if (!client.isErrorResponse(authResponse)) {
  console.log('Player balance:', authResponse.balance);
  console.log('Game config:', authResponse.config);
}

// Place a bet
const playResponse = await client.play(1000000, 'BASE'); // 1 credit with 1M multiplier
if (!client.isErrorResponse(playResponse)) {
  console.log('Round result:', playResponse.round);
}
```

## API Reference

### GameController

The main class for managing game sessions and state.

#### Constructor Options

```typescript
interface GameControllerOptions {
  baseUrl: string;        // RGS server URL
  sessionId: string;      // Player session ID
  language?: string;      // Player language (default: 'en')
  currency?: string;      // Game currency
  timeout?: number;       // Request timeout in ms (default: 30000)
  apiMultiplier?: number; // API amount multiplier (default: 1000000)
}
```

#### Methods

- `initialize()`: Authenticate and initialize the game session
- `placeBet(amount, mode?)`: Place a bet and start a round
- `endRound()`: End the current round and collect winnings
- `refreshBalance()`: Refresh the player's balance
- `getStateManager()`: Get the game state manager
- `getRGSClient()`: Get the underlying RGS client

### RGSClient

Low-level client for direct RGS API communication.

#### Methods

- `authenticate(language?)`: Authenticate with the RGS
- `play(amount, mode?)`: Start a game round
- `getBalance()`: Get current balance
- `endRound()`: End the current round
- `sendEvent(event)`: Send a game event

### GameStateManager

Manages game state with reactive updates.

#### State Properties

```typescript
interface GameStateData {
  state: 'idle' | 'playing' | 'ended' | 'error';
  balance: Balance | null;
  config: GameConfig | null;
  currentRound: GameRound | null;
  lastWin: number;
  error: string | null;
}
```

#### Methods

- `subscribe(listener)`: Subscribe to state changes
- `getState()`: Get current state
- `canPlay()`: Check if player can place a bet
- `needsEndRound()`: Check if round needs to be ended

## Examples

See the `examples/` directory for complete working examples:

- `simple-game/`: Basic Svelte implementation matching the original simple example

## RGS API Endpoints

The SDK supports all standard RGS endpoints:

- `POST /wallet/authenticate`: Authenticate player session
- `POST /wallet/play`: Place a bet and start a round
- `POST /wallet/balance`: Get current balance
- `POST /wallet/end-round`: End the current round
- `POST /bet/event`: Send game events

## Error Handling

All API calls return either the expected response or an error response:

```typescript
const response = await client.play(1000000, 'BASE');
if (client.isErrorResponse(response)) {
  console.error('Error:', response.error.code, response.error.message);
} else {
  // Handle successful response
  console.log('Round result:', response.round);
}
```

## Development

### Building the SDK

```bash
npm run build
```

### Running Examples

```bash
cd examples/simple-game
npm install
npm run dev
```

## License

MIT License - see LICENSE file for details.