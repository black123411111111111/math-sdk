# Web SDK Integration Guide

This guide demonstrates how to integrate the Stake Engine Math SDK with web frontends using the included Web SDK.

## Overview

The Stake Engine provides two main components for game development:

1. **Math SDK (Python)**: Generates game logic, simulations, and mathematical models
2. **Web SDK (TypeScript/JavaScript)**: Provides frontend integration with the RGS API

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Math SDK      │    │   RGS Server    │    │   Web SDK       │
│   (Python)      │───▶│   (Backend)     │◀───│ (Frontend)      │
│                 │    │                 │    │                 │
│ • Game Logic    │    │ • API Endpoints │    │ • RGS Client    │
│ • Simulations   │    │ • Session Mgmt  │    │ • State Mgmt    │
│ • Optimization  │    │ • Balance Mgmt  │    │ • UI Components │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Math SDK to RGS

The Math SDK generates the following outputs that are consumed by the RGS:

1. **Game Logic Files**: JSON/JSONL files containing simulation results
2. **Lookup Tables**: CSV files mapping probabilities to simulation IDs
3. **Configuration Files**: Game parameters and settings

### Example Workflow

1. Run your game's `run.py` script:
   ```bash
   cd games/fifty_fifty
   python run.py
   ```

2. This generates files in `library/publish_files/`:
   - `books_base.jsonl.zst` (or `.jsonl` if compression is disabled)
   - `lookUpTableIdToCriteria_base.csv`
   - `index.json`

3. Upload these files to the RGS server

## RGS to Web SDK

The Web SDK communicates with the RGS through standard HTTP endpoints:

### Authentication Flow

```typescript
import { GameController } from '@stake-engine/web-sdk';

const gameController = new GameController({
  baseUrl: 'https://your-rgs-server.com',
  sessionId: getUrlParam('sessionID'),
  language: getUrlParam('language') || 'en',
  currency: getUrlParam('currency') || 'USD'
});

// Initialize session
await gameController.initialize();
```

### Game Flow

```typescript
// 1. Place a bet
await gameController.placeBet(betAmount, 'BASE');

// 2. End round (if there's a win)
if (gameController.getStateManager().needsEndRound()) {
  await gameController.endRound();
}
```

## Complete Example: Fifty-Fifty Game

Here's how to create a complete integration using the fifty-fifty game:

### 1. Generate Math Files

```bash
cd games/fifty_fifty
python run.py
```

### 2. Deploy RGS (conceptual)

Upload the generated files to your RGS server:
- `library/publish_files/books_base.jsonl.zst`
- `library/publish_files/lookUpTableIdToCriteria_base.csv`
- `library/publish_files/index.json`

### 3. Create Web Frontend

```typescript
// main.ts
import { GameController, getUrlParam } from '@stake-engine/web-sdk';

const gameController = new GameController({
  baseUrl: `https://${getUrlParam('rgs_url')}`,
  sessionId: getUrlParam('sessionID')!,
  language: getUrlParam('language') || 'en'
});

// Initialize and start game loop
await gameController.initialize();

// Game logic
async function playRound() {
  await gameController.placeBet(1, 'BASE');
  
  const state = gameController.getStateManager().getState();
  if (state.lastWin > 0) {
    await gameController.endRound();
  }
}
```

### 4. URL Parameters

The frontend expects these URL parameters:
- `rgs_url`: RGS server URL
- `sessionID`: Player session ID
- `language`: Player language (optional)
- `currency`: Game currency (optional)
- `mode`: Game mode (optional, default: 'BASE')

Example URL:
```
https://your-frontend.com/?rgs_url=rgs.example.com&sessionID=abc123&language=en&currency=USD
```

## API Endpoints Used

The Web SDK communicates with these RGS endpoints:

| Endpoint | Purpose | When Called |
|----------|---------|-------------|
| `POST /wallet/authenticate` | Validate session, get config | On initialization |
| `POST /wallet/play` | Place bet, start round | When player bets |
| `POST /wallet/balance` | Get current balance | For balance updates |
| `POST /wallet/end-round` | End round, collect winnings | When round has winnings |
| `POST /bet/event` | Send game events | For game state tracking |

## State Management

The Web SDK provides reactive state management:

```typescript
gameController.getStateManager().subscribe((state) => {
  // React to state changes
  console.log('Game state:', state.state);
  console.log('Balance:', state.balance);
  console.log('Last win:', state.lastWin);
  
  // Update UI based on state
  updateUI(state);
});
```

## Error Handling

All API calls include comprehensive error handling:

```typescript
const response = await gameController.placeBet(100, 'BASE');
const state = gameController.getStateManager().getState();

if (state.error) {
  console.error('Game error:', state.error);
  // Handle error in UI
}
```

## Framework Integration

### Svelte (Recommended)

```svelte
<script lang="ts">
  import { GameController } from '@stake-engine/web-sdk';
  
  let gameState = $state(null);
  
  onMount(async () => {
    const controller = new GameController(config);
    controller.getStateManager().subscribe(state => {
      gameState = state;
    });
    await controller.initialize();
  });
</script>

<button disabled={!gameState?.canPlay()} onclick={placeBet}>
  Place Bet
</button>
```

### React

```tsx
import { useEffect, useState } from 'react';
import { GameController } from '@stake-engine/web-sdk';

function GameComponent() {
  const [gameState, setGameState] = useState(null);
  const [controller, setController] = useState(null);
  
  useEffect(() => {
    const gameController = new GameController(config);
    gameController.getStateManager().subscribe(setGameState);
    gameController.initialize();
    setController(gameController);
  }, []);
  
  return (
    <button 
      disabled={!gameState?.canPlay()} 
      onClick={() => controller?.placeBet(100, 'BASE')}
    >
      Place Bet
    </button>
  );
}
```

### Vue

```vue
<template>
  <button :disabled="!canPlay" @click="placeBet">
    Place Bet
  </button>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { GameController } from '@stake-engine/web-sdk';

const gameState = ref(null);
const controller = ref(null);

const canPlay = computed(() => gameState.value?.canPlay());

onMounted(async () => {
  controller.value = new GameController(config);
  controller.value.getStateManager().subscribe(state => {
    gameState.value = state;
  });
  await controller.value.initialize();
});
</script>
```

## Development Workflow

1. **Math Development**: Create and test game logic in Python
2. **Simulation**: Generate game files using `run.py`
3. **RGS Deployment**: Upload files to RGS server
4. **Frontend Development**: Build UI using Web SDK
5. **Integration Testing**: Test complete flow
6. **Production Deployment**: Deploy both RGS and frontend

## Best Practices

1. **Error Handling**: Always check for errors in API responses
2. **State Management**: Use the built-in state manager for reactive updates
3. **Type Safety**: Leverage TypeScript types for better development experience
4. **Testing**: Test with actual RGS server or mock responses
5. **Performance**: Cache responses where appropriate
6. **Security**: Validate all user inputs and session tokens

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure RGS server allows cross-origin requests
2. **Session Timeout**: Handle session expiration and re-authentication
3. **Network Errors**: Implement retry logic for failed requests
4. **State Sync**: Ensure frontend state matches server state

### Debug Mode

Enable debug logging:

```typescript
// Enable verbose logging
console.log('Game state:', gameController.getStateManager().getState());
console.log('Last response:', await gameController.getRGSClient().getBalance());
```

## Migration from Simple Example

If you're migrating from the text-based simple example:

1. Replace manual fetch calls with Web SDK:
   ```typescript
   // Old
   const response = await fetch(url, { method: 'POST', body: JSON.stringify(data) });
   
   // New
   const response = await gameController.placeBet(amount, mode);
   ```

2. Use state manager instead of manual state:
   ```typescript
   // Old
   let balance = $state(1000);
   let gamestate = $state('rest');
   
   // New
   gameController.getStateManager().subscribe(state => {
     // Auto-updates when state changes
   });
   ```

3. Replace manual error handling with built-in error management