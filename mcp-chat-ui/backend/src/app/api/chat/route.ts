import { NextResponse } from 'next/server';
import { withCors } from '@/lib/cors';
import { handleAsyncRoute, ValidationError } from '@/lib/errors';
import { validateChatRequest } from '@/lib/validation';
import { ensureInitialized } from '@/lib/initialization';
import { ChatRequest, ChatResponse } from '@/types';
import { createLLMService, getDefaultProviderConfig } from '@/services/LLMService';
import { getSessionManager } from '@/services/SessionManager';
import { createChatProcessor } from '@/services/ChatProcessor';

async function chatHandler(request: Request): Promise<NextResponse> {
  if (request.method !== 'POST') {
    return NextResponse.json(
      { error: 'Method not allowed', sessionId: '', message: 'Only POST method is allowed' },
      { status: 405 }
    );
  }

  console.log('Processing chat request');

  // Ensure backend is initialized
  await ensureInitialized();

  const body = await request.json();
  const chatRequest = validateChatRequest(body);

  // Extract additional parameters from request body
  const { 
    apiKey, 
    baseUrl, 
    systemPrompt, 
    temperature, 
    maxTokens,
    availableTools 
  } = body;

  // Validate API key is provided
  if (!apiKey || typeof apiKey !== 'string' || apiKey.trim().length === 0) {
    throw new ValidationError('API key is required for chat requests');
  }

  // Basic API key format validation
  if (apiKey.length < 10) {
    throw new ValidationError('API key appears to be invalid (too short)');
  }

  try {
    // Create LLM service with user's configuration
    const defaultConfig = getDefaultProviderConfig(chatRequest.provider);
    const llmService = createLLMService({
      provider: chatRequest.provider,
      apiKey,
      baseUrl: baseUrl || defaultConfig.baseUrl,
      model: chatRequest.model,
      maxRetries: defaultConfig.maxRetries,
      retryDelay: defaultConfig.retryDelay,
      timeout: defaultConfig.timeout,
    });

    // Get session manager
    const sessionManager = getSessionManager();

    // Create chat processor
    const chatProcessor = createChatProcessor(llmService, sessionManager);

    // Process the chat query
    const response = await chatProcessor.processQuery({
      messages: chatRequest.messages,
      sessionId: chatRequest.sessionId,
      provider: chatRequest.provider,
      model: chatRequest.model,
      availableTools: availableTools || [],
      systemPrompt,
      temperature,
      maxTokens,
    });

    const chatResponse: ChatResponse = {
      reply: response.reply,
      toolCalls: response.toolCalls,
      sessionId: response.sessionId,
    };

    console.log(`Chat request processed successfully for session: ${response.sessionId}`);
    return NextResponse.json(chatResponse);
  } catch (error) {
    console.error('Chat processing error:', error);
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    const statusCode = error instanceof ValidationError ? 400 : 500;
    
    const chatResponse: ChatResponse = {
      sessionId: chatRequest.sessionId,
      error: errorMessage,
    };

    return NextResponse.json(chatResponse, { status: statusCode });
  }
}

export const POST = withCors(handleAsyncRoute(chatHandler));
export const OPTIONS = withCors(async () => new NextResponse(null, { status: 200 }));