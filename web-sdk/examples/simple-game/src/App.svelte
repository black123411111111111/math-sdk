<script lang="ts">
  import { onMount } from 'svelte';
  import { GameController, getUrlParam, formatCurrency } from '@stake-engine/web-sdk';
  import type { GameStateData, PlayResponse, EndRoundResponse } from '@stake-engine/web-sdk';

  // Game state
  let gameController: GameController | null = null;
  let gameState: GameStateData | null = null;
  let isInitialized = false;
  let lastPlayResponse: PlayResponse | null = null;
  let lastEndRoundResponse: EndRoundResponse | null = null;

  // Configuration from URL parameters
  const rgsUrl = getUrlParam('rgs_url') || 'localhost:8080';
  const sessionID = getUrlParam('sessionID') || 'test-session';
  const language = getUrlParam('language') || 'en';
  const currency = getUrlParam('currency') || 'USD';
  const mode = getUrlParam('mode') || 'BASE';

  onMount(async () => {
    try {
      // Initialize the game controller
      gameController = new GameController({
        baseUrl: `https://${rgsUrl}`,
        sessionId: sessionID,
        language,
        currency,
        apiMultiplier: 1000000 // Same as original example
      });

      // Subscribe to game state changes
      const unsubscribe = gameController.getStateManager().subscribe((state) => {
        gameState = state;
      });

      // Initialize the session
      const success = await gameController.initialize();
      if (success) {
        isInitialized = true;
      }

      // Cleanup subscription on component destroy
      return unsubscribe;
    } catch (error) {
      console.error('Failed to initialize game:', error);
    }
  });

  async function placeBet() {
    if (!gameController || !gameState) return;

    try {
      const success = await gameController.placeBet(1, mode); // 1 credit bet
      if (success) {
        // Get the last play response for display
        const rgsClient = gameController.getRGSClient();
        // Note: In a real app, you'd store this from the controller's response
        lastPlayResponse = {
          balance: gameState.balance!,
          round: gameState.currentRound!
        };
        lastEndRoundResponse = null;
      }
    } catch (error) {
      console.error('Failed to place bet:', error);
    }
  }

  async function endRound() {
    if (!gameController || !gameState) return;

    try {
      const success = await gameController.endRound();
      if (success) {
        // Get the last end round response for display
        lastEndRoundResponse = {
          balance: gameState.balance!
        };
      }
    } catch (error) {
      console.error('Failed to end round:', error);
    }
  }

  // Computed values
  $: displayBalance = gameState?.balance ? gameController?.apiToDisplay(gameState.balance.amount) ?? 0 : 0;
  $: displayWin = gameState?.lastWin ?? 0;
  $: canPlay = gameState?.state === 'idle' && displayBalance > 0;
  $: canEndRound = gameState?.state === 'playing' && displayWin > 0;
  $: gameStateText = gameState?.state ?? 'loading';
</script>

<div class="game-wrapper">
  <div class="game-content">
    {#if !isInitialized}
      <h2>Initializing game...</h2>
    {:else}
      <h2>Balance: {formatCurrency(displayBalance, currency)}</h2>
      <h2>Round Win: {displayWin}x</h2>
      <h3>State: {gameStateText}</h3>
      
      {#if gameState?.error}
        <div class="error">
          Error: {gameState.error}
        </div>
      {/if}

      <button 
        onclick={placeBet}
        disabled={!canPlay}
      >
        Place Bet
      </button>
      
      <button 
        onclick={endRound}
        disabled={!canEndRound}
      >
        End Round
      </button>
    {/if}
  </div>

  <div class="json-stack">
    <h3>play/ response</h3>
    <div class="bet-display">
      <pre>{JSON.stringify(lastPlayResponse, null, 2)}</pre>
    </div>

    <h3>end-round/ response</h3>
    <div class="end-display">
      <pre>{JSON.stringify(lastEndRoundResponse, null, 2)}</pre>
    </div>
  </div>
</div>

<style>
  h3 {
    color: white;
    margin-bottom: 0.5rem;
  }
</style>