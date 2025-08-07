import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { ChatSession, Message, ToolCall, LLMProvider } from '../types';

interface ChatStore {
  // Current session state
  currentSession: ChatSession | null;
  messages: Message[];
  isLoading: boolean;
  pendingToolCall: ToolCall | null;
  
  // Chat history
  sessions: ChatSession[];
  
  // Actions
  sendMessage: (content: string) => Promise<void>;
  confirmToolCall: (toolCall: ToolCall) => Promise<void>;
  cancelToolCall: () => void;
  loadSession: (sessionId: string) => Promise<void>;
  createNewSession: (provider: LLMProvider, model: string, mcpServers?: string[]) => void;
  updateSessionTitle: (sessionId: string, title: string) => void;
  deleteSession: (sessionId: string) => void;
  archiveSession: (sessionId: string) => void;
  searchSessions: (query: string) => ChatSession[];
  
  // Message management
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  updateMessage: (messageId: string, updates: Partial<Message>) => void;
  deleteMessage: (messageId: string) => void;
  
  // Session persistence
  saveSession: () => void;
  loadSessions: () => void;
  
  // Tool call management
  setPendingToolCall: (toolCall: ToolCall | null) => void;
  setLoading: (loading: boolean) => void;
  
  // Utility functions
  generateSessionTitle: (messages: Message[]) => string;
  clearCurrentSession: () => void;
}

const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

const generateSessionTitle = (messages: Message[]): string => {
  // Find the first user message to generate a title
  const firstUserMessage = messages.find(m => m.role === 'user');
  if (!firstUserMessage) {
    return 'New Chat';
  }
  
  // Take first 50 characters and add ellipsis if longer
  const content = firstUserMessage.content.trim();
  if (content.length <= 50) {
    return content;
  }
  
  return content.substring(0, 47) + '...';
};

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      // Initial state
      currentSession: null,
      messages: [],
      isLoading: false,
      pendingToolCall: null,
      sessions: [],
      
      // Actions
      sendMessage: async (content: string) => {
        const { currentSession, addMessage, saveSession } = get();
        
        if (!currentSession) {
          throw new Error('No active session');
        }
        
        // Add user message
        const userMessage: Omit<Message, 'id' | 'timestamp'> = {
          role: 'user',
          content: content.trim(),
        };
        
        addMessage(userMessage);
        set({ isLoading: true });
        
        try {
          // TODO: This will be implemented when we connect to the backend API
          // For now, we just add the message and save the session
          saveSession();
          
          // Simulate API call delay
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Add a placeholder assistant response
          const assistantMessage: Omit<Message, 'id' | 'timestamp'> = {
            role: 'assistant',
            content: 'This is a placeholder response. Backend integration will be implemented in a later task.',
          };
          
          addMessage(assistantMessage);
          saveSession();
          
        } catch (error) {
          console.error('Error sending message:', error);
          // TODO: Add proper error handling
        } finally {
          set({ isLoading: false });
        }
      },
      
      confirmToolCall: async (toolCall: ToolCall) => {
        const { currentSession, addMessage, saveSession } = get();
        
        if (!currentSession) {
          throw new Error('No active session');
        }
        
        set({ isLoading: true, pendingToolCall: null });
        
        try {
          // TODO: This will be implemented when we connect to the backend API
          // For now, we just add a placeholder tool result
          
          const toolMessage: Omit<Message, 'id' | 'timestamp'> = {
            role: 'tool',
            content: `Tool "${toolCall.function.name}" executed successfully. (Placeholder result)`,
            toolCallId: toolCall.id,
          };
          
          addMessage(toolMessage);
          
          // Add assistant response to tool result
          const assistantMessage: Omit<Message, 'id' | 'timestamp'> = {
            role: 'assistant',
            content: 'Tool execution completed. Backend integration will be implemented in a later task.',
          };
          
          addMessage(assistantMessage);
          saveSession();
          
        } catch (error) {
          console.error('Error executing tool:', error);
          // TODO: Add proper error handling
        } finally {
          set({ isLoading: false });
        }
      },
      
      cancelToolCall: () => {
        const { currentSession, addMessage, saveSession } = get();
        
        if (!currentSession) {
          return;
        }
        
        set({ pendingToolCall: null });
        
        // Add a message indicating the tool was cancelled
        const assistantMessage: Omit<Message, 'id' | 'timestamp'> = {
          role: 'assistant',
          content: 'Tool execution was cancelled by the user.',
        };
        
        addMessage(assistantMessage);
        saveSession();
      },
      
      loadSession: async (sessionId: string) => {
        const { sessions } = get();
        const session = sessions.find(s => s.id === sessionId);
        
        if (!session) {
          throw new Error(`Session ${sessionId} not found`);
        }
        
        set({
          currentSession: session,
          messages: session.messages,
          pendingToolCall: null,
          isLoading: false,
        });
      },
      
      createNewSession: (provider: LLMProvider, model: string, mcpServers: string[] = []) => {
        const newSession: ChatSession = {
          id: generateId(),
          title: 'New Chat',
          messages: [],
          createdAt: new Date(),
          updatedAt: new Date(),
          provider,
          model,
          mcpServers,
        };
        
        set(state => ({
          currentSession: newSession,
          messages: [],
          sessions: [newSession, ...state.sessions],
          pendingToolCall: null,
          isLoading: false,
        }));
        
        get().saveSession();
      },
      
      updateSessionTitle: (sessionId: string, title: string) => {
        set(state => {
          const updatedSessions = state.sessions.map(session =>
            session.id === sessionId
              ? { ...session, title, updatedAt: new Date() }
              : session
          );
          
          const updatedCurrentSession = state.currentSession?.id === sessionId
            ? { ...state.currentSession, title, updatedAt: new Date() }
            : state.currentSession;
          
          return {
            sessions: updatedSessions,
            currentSession: updatedCurrentSession,
          };
        });
        
        get().saveSession();
      },
      
      deleteSession: (sessionId: string) => {
        set(state => {
          const updatedSessions = state.sessions.filter(s => s.id !== sessionId);
          const updatedCurrentSession = state.currentSession?.id === sessionId
            ? null
            : state.currentSession;
          
          return {
            sessions: updatedSessions,
            currentSession: updatedCurrentSession,
            messages: updatedCurrentSession?.messages || [],
          };
        });
        
        get().saveSession();
      },
      
      archiveSession: (sessionId: string) => {
        // For now, archiving is the same as deleting
        // In the future, we could add an 'archived' flag to sessions
        get().deleteSession(sessionId);
      },
      
      searchSessions: (query: string): ChatSession[] => {
        const { sessions } = get();
        
        if (!query.trim()) {
          return sessions;
        }
        
        const lowercaseQuery = query.toLowerCase();
        
        return sessions.filter(session => {
          // Search in title
          if (session.title.toLowerCase().includes(lowercaseQuery)) {
            return true;
          }
          
          // Search in message content
          return session.messages.some(message =>
            message.content.toLowerCase().includes(lowercaseQuery)
          );
        });
      },
      
      // Message management
      addMessage: (messageData: Omit<Message, 'id' | 'timestamp'>) => {
        const message: Message = {
          ...messageData,
          id: generateId(),
          timestamp: new Date(),
        };
        
        set(state => {
          const updatedMessages = [...state.messages, message];
          const updatedCurrentSession = state.currentSession
            ? {
                ...state.currentSession,
                messages: updatedMessages,
                updatedAt: new Date(),
                // Auto-generate title from first user message if still "New Chat"
                title: state.currentSession.title === 'New Chat' && message.role === 'user'
                  ? generateSessionTitle([message])
                  : state.currentSession.title,
              }
            : null;
          
          const updatedSessions = state.sessions.map(session =>
            session.id === updatedCurrentSession?.id ? updatedCurrentSession : session
          );
          
          return {
            messages: updatedMessages,
            currentSession: updatedCurrentSession,
            sessions: updatedSessions,
          };
        });
      },
      
      updateMessage: (messageId: string, updates: Partial<Message>) => {
        set(state => {
          const updatedMessages = state.messages.map(message =>
            message.id === messageId ? { ...message, ...updates } : message
          );
          
          const updatedCurrentSession = state.currentSession
            ? { ...state.currentSession, messages: updatedMessages, updatedAt: new Date() }
            : null;
          
          const updatedSessions = state.sessions.map(session =>
            session.id === updatedCurrentSession?.id ? updatedCurrentSession : session
          );
          
          return {
            messages: updatedMessages,
            currentSession: updatedCurrentSession,
            sessions: updatedSessions,
          };
        });
        
        get().saveSession();
      },
      
      deleteMessage: (messageId: string) => {
        set(state => {
          const updatedMessages = state.messages.filter(m => m.id !== messageId);
          const updatedCurrentSession = state.currentSession
            ? { ...state.currentSession, messages: updatedMessages, updatedAt: new Date() }
            : null;
          
          const updatedSessions = state.sessions.map(session =>
            session.id === updatedCurrentSession?.id ? updatedCurrentSession : session
          );
          
          return {
            messages: updatedMessages,
            currentSession: updatedCurrentSession,
            sessions: updatedSessions,
          };
        });
        
        get().saveSession();
      },
      
      // Session persistence
      saveSession: () => {
        // The persist middleware handles this automatically
        // This method is here for explicit saves if needed
      },
      
      loadSessions: () => {
        // The persist middleware handles this automatically on store initialization
        // This method is here for explicit loads if needed
      },
      
      // Tool call management
      setPendingToolCall: (toolCall: ToolCall | null) => {
        set({ pendingToolCall: toolCall });
      },
      
      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },
      
      // Utility functions
      generateSessionTitle: (messages: Message[]): string => {
        return generateSessionTitle(messages);
      },
      
      clearCurrentSession: () => {
        set({
          currentSession: null,
          messages: [],
          pendingToolCall: null,
          isLoading: false,
        });
      },
    }),
    {
      name: 'chat-store',
      storage: createJSONStorage(() => localStorage),
      // Only persist sessions, not the current session state
      partialize: (state) => ({
        sessions: state.sessions,
      }),
    }
  )
);