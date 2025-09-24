import { RGSClient } from './rgs-client.js';
import { GameStateManager } from './game-state.js';
import type { RGSClientConfig, AuthenticateResponse, PlayResponse, EndRoundResponse } from '../types/rgs.js';

export interface GameControllerOptions extends RGSClientConfig {
  apiMultiplier?: number; // Default multiplier for converting API amounts (e.g., 1000000)
}

export class GameController {
  private rgsClient: RGSClient;
  private stateManager: GameStateManager;
  private apiMultiplier: number;

  constructor(options: GameControllerOptions) {
    this.rgsClient = new RGSClient(options);
    this.stateManager = new GameStateManager();
    this.apiMultiplier = options.apiMultiplier || 1000000; // Default from simple example
  }

  public getStateManager(): GameStateManager {
    return this.stateManager;
  }

  public getRGSClient(): RGSClient {
    return this.rgsClient;
  }

  /**
   * Initialize the game session by authenticating with the RGS
   */
  public async initialize(): Promise<boolean> {
    try {
      this.stateManager.clearError();
      
      const response = await this.rgsClient.authenticate();
      
      if (this.rgsClient.isErrorResponse(response)) {
        this.stateManager.setError(`Authentication failed: ${response.error.message}`);
        this.stateManager.setState('error');
        return false;
      }

      const authResponse = response as AuthenticateResponse;
      
      // Update state with authentication response
      this.stateManager.setBalance(authResponse.balance);
      this.stateManager.setConfig(authResponse.config);
      
      if (authResponse.round) {
        this.stateManager.setCurrentRound(authResponse.round);
        // If there's an active round with a payout, set appropriate state
        if (authResponse.round.payoutMultiplier && authResponse.round.payoutMultiplier > 0) {
          this.stateManager.setState('playing');
          this.stateManager.setLastWin(authResponse.round.payoutMultiplier);
        } else {
          this.stateManager.setState('idle');
        }
      } else {
        this.stateManager.setState('idle');
      }

      return true;
    } catch (error) {
      console.error('Initialization error:', error);
      this.stateManager.setError('Failed to initialize game session');
      this.stateManager.setState('error');
      return false;
    }
  }

  /**
   * Place a bet and start a game round
   */
  public async placeBet(betAmount: number, mode: string = 'BASE'): Promise<boolean> {
    try {
      if (!this.stateManager.canPlay()) {
        this.stateManager.setError('Cannot place bet in current state');
        return false;
      }

      this.stateManager.clearError();
      this.stateManager.setState('playing');

      // Convert bet amount to API format
      const apiAmount = Math.round(betAmount * this.apiMultiplier);
      
      const response = await this.rgsClient.play(apiAmount, mode);
      
      if (this.rgsClient.isErrorResponse(response)) {
        this.stateManager.setError(`Bet failed: ${response.error.message}`);
        this.stateManager.setState('error');
        return false;
      }

      const playResponse = response as PlayResponse;
      
      // Update state with play response
      this.stateManager.setBalance(playResponse.balance);
      this.stateManager.setCurrentRound(playResponse.round);
      
      if (playResponse.round.payoutMultiplier !== undefined) {
        this.stateManager.setLastWin(playResponse.round.payoutMultiplier);
        
        // If no win, automatically end the round
        if (playResponse.round.payoutMultiplier === 0) {
          this.stateManager.setState('idle');
          this.stateManager.setCurrentRound(null);
        }
        // If there's a win, stay in playing state until endRound is called
      }

      return true;
    } catch (error) {
      console.error('Place bet error:', error);
      this.stateManager.setError('Failed to place bet');
      this.stateManager.setState('error');
      return false;
    }
  }

  /**
   * End the current round and collect winnings
   */
  public async endRound(): Promise<boolean> {
    try {
      if (!this.stateManager.needsEndRound()) {
        this.stateManager.setError('No active round to end');
        return false;
      }

      this.stateManager.clearError();
      
      const response = await this.rgsClient.endRound();
      
      if (this.rgsClient.isErrorResponse(response)) {
        this.stateManager.setError(`End round failed: ${response.error.message}`);
        this.stateManager.setState('error');
        return false;
      }

      const endResponse = response as EndRoundResponse;
      
      // Update state after ending round
      this.stateManager.setBalance(endResponse.balance);
      this.stateManager.setState('idle');
      this.stateManager.setCurrentRound(null);

      return true;
    } catch (error) {
      console.error('End round error:', error);
      this.stateManager.setError('Failed to end round');
      this.stateManager.setState('error');
      return false;
    }
  }

  /**
   * Refresh the current balance
   */
  public async refreshBalance(): Promise<boolean> {
    try {
      this.stateManager.clearError();
      
      const response = await this.rgsClient.getBalance();
      
      if (this.rgsClient.isErrorResponse(response)) {
        this.stateManager.setError(`Balance refresh failed: ${response.error.message}`);
        return false;
      }

      this.stateManager.setBalance(response.balance);
      return true;
    } catch (error) {
      console.error('Refresh balance error:', error);
      this.stateManager.setError('Failed to refresh balance');
      return false;
    }
  }

  /**
   * Convert API amount to display amount
   */
  public apiToDisplay(apiAmount: number): number {
    return apiAmount / this.apiMultiplier;
  }

  /**
   * Convert display amount to API amount
   */
  public displayToApi(displayAmount: number): number {
    return Math.round(displayAmount * this.apiMultiplier);
  }

  /**
   * Get current balance in display format
   */
  public getDisplayBalance(): number {
    const balance = this.stateManager.getState().balance;
    return balance ? this.apiToDisplay(balance.amount) : 0;
  }
}