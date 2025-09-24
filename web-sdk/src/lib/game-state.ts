import type { GameState, GameRound, Balance, GameConfig } from '../types/rgs.js';

export interface GameStateData {
  state: GameState;
  balance: Balance | null;
  config: GameConfig | null;
  currentRound: GameRound | null;
  lastWin: number;
  error: string | null;
}

export class GameStateManager {
  private listeners: Set<(state: GameStateData) => void> = new Set();
  private state: GameStateData;

  constructor() {
    this.state = {
      state: 'idle',
      balance: null,
      config: null,
      currentRound: null,
      lastWin: 0,
      error: null
    };
  }

  public getState(): GameStateData {
    return { ...this.state };
  }

  public subscribe(listener: (state: GameStateData) => void): () => void {
    this.listeners.add(listener);
    // Immediately call with current state
    listener(this.getState());
    
    // Return unsubscribe function
    return () => {
      this.listeners.delete(listener);
    };
  }

  public updateState(updates: Partial<GameStateData>): void {
    this.state = { ...this.state, ...updates };
    this.notifyListeners();
  }

  public setState(newState: GameState): void {
    this.updateState({ state: newState });
  }

  public setBalance(balance: Balance): void {
    this.updateState({ balance });
  }

  public setConfig(config: GameConfig): void {
    this.updateState({ config });
  }

  public setCurrentRound(round: GameRound | null): void {
    this.updateState({ currentRound: round });
  }

  public setLastWin(amount: number): void {
    this.updateState({ lastWin: amount });
  }

  public setError(error: string | null): void {
    this.updateState({ error });
  }

  public clearError(): void {
    this.setError(null);
  }

  public reset(): void {
    this.state = {
      state: 'idle',
      balance: null,
      config: null,
      currentRound: null,
      lastWin: 0,
      error: null
    };
    this.notifyListeners();
  }

  private notifyListeners(): void {
    const currentState = this.getState();
    this.listeners.forEach(listener => {
      try {
        listener(currentState);
      } catch (error) {
        console.error('Error in game state listener:', error);
      }
    });
  }

  // Convenience methods for common state checks
  public isIdle(): boolean {
    return this.state.state === 'idle';
  }

  public isPlaying(): boolean {
    return this.state.state === 'playing';
  }

  public isEnded(): boolean {
    return this.state.state === 'ended';
  }

  public hasError(): boolean {
    return this.state.state === 'error' || this.state.error !== null;
  }

  public canPlay(): boolean {
    return this.isIdle() && this.state.balance !== null && this.state.balance.amount > 0;
  }

  public needsEndRound(): boolean {
    return this.isPlaying() && this.state.currentRound?.payoutMultiplier !== undefined && this.state.currentRound.payoutMultiplier > 0;
  }
}