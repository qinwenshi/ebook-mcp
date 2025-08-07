// Basic types for the application
export interface MCPServer {
  id: string;
  name: string;
  status: 'connected' | 'disconnected' | 'error';
}

export interface ChatMessage {
  id: string;
  content: string;
  timestamp: Date;
  sender: 'user' | 'assistant';
}
