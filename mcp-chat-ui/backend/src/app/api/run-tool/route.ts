import { NextResponse } from 'next/server';
import { withCors } from '@/lib/cors';
import { handleAsyncRoute } from '@/lib/errors';
import { validateRunToolRequest } from '@/lib/validation';
import { RunToolRequest, RunToolResponse } from '@/types';

async function runToolHandler(request: Request): Promise<NextResponse> {
  if (request.method !== 'POST') {
    return NextResponse.json(
      { 
        result: '', 
        reply: '', 
        error: 'Method not allowed - Only POST method is allowed' 
      },
      { status: 405 }
    );
  }

  const body = await request.json();
  const toolRequest = validateRunToolRequest(body);

  // TODO: Implement actual MCP tool execution
  // For now, return a mock response based on the tool name
  const toolName = toolRequest.toolCall.function.name;
  const toolArgs = toolRequest.toolCall.function.arguments;

  let mockResult: string;
  let mockReply: string;

  try {
    const parsedArgs = JSON.parse(toolArgs);
    
    switch (toolName) {
      case 'read_file':
        mockResult = `Mock file content for: ${parsedArgs.path || 'unknown file'}`;
        mockReply = `I've read the file "${parsedArgs.path || 'unknown file'}" for you. Here's the content...`;
        break;
      
      case 'list_directory':
        mockResult = JSON.stringify([
          { name: 'file1.txt', type: 'file', size: 1024 },
          { name: 'folder1', type: 'directory' },
          { name: 'file2.md', type: 'file', size: 2048 },
        ]);
        mockReply = `I've listed the contents of the directory "${parsedArgs.path || 'unknown directory'}".`;
        break;
      
      case 'write_file':
        mockResult = `File written successfully: ${parsedArgs.path || 'unknown file'}`;
        mockReply = `I've written the content to "${parsedArgs.path || 'unknown file'}" successfully.`;
        break;
      
      default:
        mockResult = `Mock result for tool: ${toolName}`;
        mockReply = `I've executed the "${toolName}" tool with the provided arguments.`;
    }

    const response: RunToolResponse = {
      result: mockResult,
      reply: mockReply,
    };

    return NextResponse.json(response);

  } catch (error) {
    const errorResponse: RunToolResponse = {
      result: '',
      reply: '',
      error: `Failed to execute tool "${toolName}": ${error instanceof Error ? error.message : 'Unknown error'}`,
    };

    return NextResponse.json(errorResponse, { status: 500 });
  }
}

export const POST = withCors(handleAsyncRoute(runToolHandler));
export const OPTIONS = withCors(async () => new NextResponse(null, { status: 200 }));