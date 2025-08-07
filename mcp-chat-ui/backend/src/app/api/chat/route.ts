import { NextResponse } from 'next/server';
import { withCors } from '@/lib/cors';
import { handleAsyncRoute } from '@/lib/errors';
import { validateChatRequest } from '@/lib/validation';
import { ChatRequest, ChatResponse } from '@/types';

async function chatHandler(request: Request): Promise<NextResponse> {
  if (request.method !== 'POST') {
    return NextResponse.json(
      { error: 'Method not allowed', sessionId: '', message: 'Only POST method is allowed' },
      { status: 405 }
    );
  }

  const body = await request.json();
  const chatRequest = validateChatRequest(body);

  // TODO: Implement actual LLM integration
  // For now, return a mock response
  const mockResponse: ChatResponse = {
    reply: `Mock response for session ${chatRequest.sessionId} using ${chatRequest.provider}/${chatRequest.model}`,
    sessionId: chatRequest.sessionId,
  };

  return NextResponse.json(mockResponse);
}

export const POST = withCors(handleAsyncRoute(chatHandler));
export const OPTIONS = withCors(async () => new NextResponse(null, { status: 200 }));