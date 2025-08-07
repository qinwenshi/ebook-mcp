import { LLMProvider, Message } from '@/types';
import { InternalServerError, ValidationError } from '@/lib/errors';

export interface LLMCompletionRequest {
  messages: Array<{ role: string; content: string }>;
  maxTokens?: number;
  temperature?: number;
  model?: string;
}

export interface LLMCompletionResponse {
  content: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export interface LLMServiceConfig {
  provider: LLMProvider;
  apiKey: string;
  baseUrl?: string;
  model: string;
}

export class LLMService {
  private config: LLMServiceConfig;

  constructor(config: LLMServiceConfig) {
    this.config = config;
    this.validateConfig();
  }

  /**
   * Generate a completion using the configured LLM provider
   */
  async generateCompletion(request: LLMCompletionRequest): Promise<LLMCompletionResponse> {
    try {
      switch (this.config.provider) {
        case 'openai':
          return await this.callOpenAI(request);
        case 'deepseek':
          return await this.callDeepSeek(request);
        case 'openrouter':
          return await this.callOpenRouter(request);
        default:
          throw new ValidationError(`Unsupported LLM provider: ${this.config.provider}`);
      }
    } catch (error) {
      console.error('LLM completion failed:', error);
      if (error instanceof ValidationError) {
        throw error;
      }
      throw new InternalServerError(`LLM completion failed: ${error}`);
    }
  }

  /**
   * Test the connection to the LLM provider
   */
  async testConnection(): Promise<boolean> {
    try {
      const response = await this.generateCompletion({
        messages: [{ role: 'user', content: 'Hello' }],
        maxTokens: 5,
        temperature: 0,
      });
      return !!response.content;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }

  private validateConfig(): void {
    if (!this.config.apiKey) {
      throw new ValidationError('API key is required');
    }
    if (!this.config.model) {
      throw new ValidationError('Model is required');
    }
    if (!['openai', 'deepseek', 'openrouter'].includes(this.config.provider)) {
      throw new ValidationError('Invalid LLM provider');
    }
  }

  private async callOpenAI(request: LLMCompletionRequest): Promise<LLMCompletionResponse> {
    const baseUrl = this.config.baseUrl || 'https://api.openai.com/v1';
    const url = `${baseUrl}/chat/completions`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({
        model: request.model || this.config.model,
        messages: request.messages,
        max_tokens: request.maxTokens || 100,
        temperature: request.temperature || 0.7,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`OpenAI API error: ${response.status} ${error}`);
    }

    const data = await response.json();
    return {
      content: data.choices[0]?.message?.content || '',
      usage: data.usage ? {
        promptTokens: data.usage.prompt_tokens,
        completionTokens: data.usage.completion_tokens,
        totalTokens: data.usage.total_tokens,
      } : undefined,
    };
  }

  private async callDeepSeek(request: LLMCompletionRequest): Promise<LLMCompletionResponse> {
    const baseUrl = this.config.baseUrl || 'https://api.deepseek.com/v1';
    const url = `${baseUrl}/chat/completions`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({
        model: request.model || this.config.model,
        messages: request.messages,
        max_tokens: request.maxTokens || 100,
        temperature: request.temperature || 0.7,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`DeepSeek API error: ${response.status} ${error}`);
    }

    const data = await response.json();
    return {
      content: data.choices[0]?.message?.content || '',
      usage: data.usage ? {
        promptTokens: data.usage.prompt_tokens,
        completionTokens: data.usage.completion_tokens,
        totalTokens: data.usage.total_tokens,
      } : undefined,
    };
  }

  private async callOpenRouter(request: LLMCompletionRequest): Promise<LLMCompletionResponse> {
    const baseUrl = this.config.baseUrl || 'https://openrouter.ai/api/v1';
    const url = `${baseUrl}/chat/completions`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
        'HTTP-Referer': 'http://localhost:3000', // Required by OpenRouter
        'X-Title': 'MCP Chat UI', // Optional but recommended
      },
      body: JSON.stringify({
        model: request.model || this.config.model,
        messages: request.messages,
        max_tokens: request.maxTokens || 100,
        temperature: request.temperature || 0.7,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`OpenRouter API error: ${response.status} ${error}`);
    }

    const data = await response.json();
    return {
      content: data.choices[0]?.message?.content || '',
      usage: data.usage ? {
        promptTokens: data.usage.prompt_tokens,
        completionTokens: data.usage.completion_tokens,
        totalTokens: data.usage.total_tokens,
      } : undefined,
    };
  }
}

// Factory function to create LLM service instances
export function createLLMService(config: LLMServiceConfig): LLMService {
  return new LLMService(config);
}