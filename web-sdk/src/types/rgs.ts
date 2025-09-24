// RGS API Types based on the documentation

export interface Balance {
  amount: number;
  currency: string;
}

export interface BetLevel {
  level: number;
  amount: number;
}

export interface Jurisdiction {
  socialCasino: boolean;
  disabledFullscreen: boolean;
  disabledTurbo: boolean;
}

export interface GameConfig {
  minBet: number;
  maxBet: number;
  stepBet: number;
  defaultBetLevel: number;
  betLevels: BetLevel[];
  jurisdiction: Jurisdiction;
}

export interface GameEvent {
  index: number;
  type: string;
  [key: string]: any;
}

export interface GameRound {
  id?: string;
  state?: string;
  payoutMultiplier?: number;
  events?: GameEvent[];
  totalWin?: number;
  wins?: any[];
}

// Request Types
export interface AuthenticateRequest {
  sessionID: string;
  language?: string;
}

export interface PlayRequest {
  sessionID: string;
  amount: number;
  mode: string;
  currency?: string;
}

export interface BalanceRequest {
  sessionID: string;
}

export interface EndRoundRequest {
  sessionID: string;
}

export interface EventRequest {
  sessionID: string;
  event: string;
}

// Response Types
export interface AuthenticateResponse {
  balance: Balance;
  config: GameConfig;
  round?: GameRound;
}

export interface PlayResponse {
  balance: Balance;
  round: GameRound;
}

export interface BalanceResponse {
  balance: Balance;
}

export interface EndRoundResponse {
  balance: Balance;
}

export interface EventResponse {
  event: string;
}

// Error Response
export interface ErrorResponse {
  error: {
    code: string;
    message: string;
  };
}

export type RGSResponse<T> = T | ErrorResponse;

// Game State
export type GameState = 'idle' | 'playing' | 'ended' | 'error';

// RGS Client Configuration
export interface RGSClientConfig {
  baseUrl: string;
  sessionId: string;
  language?: string;
  currency?: string;
  timeout?: number;
}