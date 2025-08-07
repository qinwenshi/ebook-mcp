import { NextResponse } from 'next/server';
import { withCors } from '@/lib/cors';
import { handleAsyncRoute } from '@/lib/errors';
import { ValidationError } from '@/lib/errors';

interface CancelToolRequest {
  toolCallId: string;
  sessionId: string;
}

interface CancelToolResponse {
  success: boolean;
  message: string;
  error?: string;
}

function validateCancelToolRequest(data: any): CancelToolRequest {
  if (!data || typeof data !== 'object') {
    throw new ValidationError('Request body must be a valid JSON object');
  }

  const { toolCallId, sessionId } = data;

  if (!toolCallId || typeof toolCallId !== 'string') {
    throw new ValidationError('Tool call ID must be a valid string');
  }

  if (!sessionId || typeof sessionId !== 'string') {
    throw new ValidationError('Session ID must be a valid string');
  }

  return { toolCallId, sessionId };
}

async function cancelToolHandler(request: Request): Promise<NextResponse> {
  if (request.method !== 'POST') {
    return NextResponse.json(
      { 
        success: false,
        message: '',
        error: 'Method not allowed - Only POST method is allowed' 
      },
      { status: 405 }
    );
  }

  const body = await request.json();
  const cancelRequest = validateCancelToolRequest(body);

  // TODO: Implement actual tool cancellation logic
  // For now, return a mock response
  try {
    // In a real implementation, this would:
    // 1. Find the running tool execution by toolCallId and sessionId
    // 2. Send a cancellation signal to the MCP server
    // 3. Clean up any resources
    // 4. Return the cancellation status

    const response: CancelToolResponse = {
      success: true,
      message: `Tool execution ${cancelRequest.toolCallId} has been cancelled successfully`,
    };

    return NextResponse.json(response);

  } catch (error) {
    const errorResponse: CancelToolResponse = {
      success: false,
      message: '',
      error: `Failed to cancel tool execution: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };

    return NextResponse.json(errorResponse, { status: 500 });
  }
}

export const POST = withCors(handleAsyncRoute(cancelToolHandler));
export const OPTIONS = withCors(async () => new NextResponse(null, { status: 200 }));