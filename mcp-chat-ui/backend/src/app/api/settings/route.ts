import { NextResponse } from 'next/server';
import { withCors } from '@/lib/cors';
import { handleAsyncRoute } from '@/lib/errors';
import { validateSettings } from '@/lib/validation';
import { Settings } from '@/types';

// Mock settings storage - in production, this would be a database
let mockSettings: Settings = {
  llmProviders: [
    {
      id: 'openai-1',
      name: 'openai',
      apiKey: '',
      baseUrl: 'https://api.openai.com/v1',
      models: [
        {
          id: 'gpt-4',
          name: 'GPT-4',
          supportsToolCalling: true,
          maxTokens: 8192,
        },
        {
          id: 'gpt-3.5-turbo',
          name: 'GPT-3.5 Turbo',
          supportsToolCalling: true,
          maxTokens: 4096,
        },
      ],
    },
  ],
  mcpServers: [
    {
      id: 'filesystem-1',
      name: 'filesystem',
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-filesystem', '/tmp'],
      enabled: false,
      status: 'disconnected',
    },
  ],
  preferences: {
    theme: 'system',
    language: 'en',
    autoScroll: true,
    soundEnabled: false,
  },
};

async function getSettingsHandler(request: Request): Promise<NextResponse> {
  return NextResponse.json(mockSettings);
}

async function updateSettingsHandler(request: Request): Promise<NextResponse> {
  const body = await request.json();
  const validatedSettings = validateSettings(body);

  // Merge with existing settings
  mockSettings = {
    ...mockSettings,
    ...validatedSettings,
  };

  return NextResponse.json(mockSettings);
}

async function settingsHandler(request: Request): Promise<NextResponse> {
  switch (request.method) {
    case 'GET':
      return getSettingsHandler(request);
    case 'PUT':
      return updateSettingsHandler(request);
    default:
      return NextResponse.json(
        { error: 'Method not allowed', message: 'Only GET and PUT methods are allowed' },
        { status: 405 }
      );
  }
}

export const GET = withCors(handleAsyncRoute(getSettingsHandler));
export const PUT = withCors(handleAsyncRoute(updateSettingsHandler));
export const OPTIONS = withCors(async () => new NextResponse(null, { status: 200 }));