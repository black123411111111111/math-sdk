import type {
  RGSClientConfig,
  AuthenticateRequest,
  AuthenticateResponse,
  PlayRequest,
  PlayResponse,
  BalanceRequest,
  BalanceResponse,
  EndRoundRequest,
  EndRoundResponse,
  EventRequest,
  EventResponse,
  ErrorResponse,
  RGSResponse
} from '../types/rgs.js';

export class RGSClient {
  private baseUrl: string;
  private sessionId: string;
  private language: string;
  private currency?: string;
  private timeout: number;

  constructor(config: RGSClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, ''); // Remove trailing slash
    this.sessionId = config.sessionId;
    this.language = config.language || 'en';
    this.currency = config.currency;
    this.timeout = config.timeout || 30000; // 30 seconds default
  }

  private async makeRequest<T>(endpoint: string, body: any): Promise<RGSResponse<T>> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Check if response contains an error
      if (data.error) {
        return data as ErrorResponse;
      }

      return data as T;
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          return {
            error: {
              code: 'TIMEOUT',
              message: 'Request timed out'
            }
          } as ErrorResponse;
        }
        
        return {
          error: {
            code: 'NETWORK_ERROR',
            message: error.message
          }
        } as ErrorResponse;
      }

      return {
        error: {
          code: 'UNKNOWN_ERROR',
          message: 'An unknown error occurred'
        }
      } as ErrorResponse;
    }
  }

  public async authenticate(language?: string): Promise<RGSResponse<AuthenticateResponse>> {
    const request: AuthenticateRequest = {
      sessionID: this.sessionId,
      language: language || this.language
    };

    return this.makeRequest<AuthenticateResponse>('/wallet/authenticate', request);
  }

  public async play(amount: number, mode: string = 'BASE'): Promise<RGSResponse<PlayResponse>> {
    const request: PlayRequest = {
      sessionID: this.sessionId,
      amount,
      mode,
      ...(this.currency && { currency: this.currency })
    };

    return this.makeRequest<PlayResponse>('/wallet/play', request);
  }

  public async getBalance(): Promise<RGSResponse<BalanceResponse>> {
    const request: BalanceRequest = {
      sessionID: this.sessionId
    };

    return this.makeRequest<BalanceResponse>('/wallet/balance', request);
  }

  public async endRound(): Promise<RGSResponse<EndRoundResponse>> {
    const request: EndRoundRequest = {
      sessionID: this.sessionId
    };

    return this.makeRequest<EndRoundResponse>('/wallet/end-round', request);
  }

  public async sendEvent(event: string): Promise<RGSResponse<EventResponse>> {
    const request: EventRequest = {
      sessionID: this.sessionId,
      event
    };

    return this.makeRequest<EventResponse>('/bet/event', request);
  }

  // Utility methods
  public updateSessionId(sessionId: string): void {
    this.sessionId = sessionId;
  }

  public updateLanguage(language: string): void {
    this.language = language;
  }

  public updateCurrency(currency: string): void {
    this.currency = currency;
  }

  public isErrorResponse<T>(response: RGSResponse<T>): response is ErrorResponse {
    return 'error' in response;
  }
}