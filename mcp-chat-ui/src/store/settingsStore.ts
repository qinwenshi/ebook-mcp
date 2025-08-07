import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { 
  Settings, 
  LLMProviderConfig, 
  MCPServerConfig, 
  UserPreferences,
  Theme,
  Language 
} from '../types';

interface SettingsStore {
  // Settings data
  llmProviders: LLMProviderConfig[];
  mcpServers: MCPServerConfig[];
  preferences: UserPreferences;
  
  // Loading states
  isLoading: boolean;
  isSaving: boolean;
  
  // Actions for LLM providers
  addLLMProvider: (config: Omit<LLMProviderConfig, 'id'>) => void;
  updateLLMProvider: (id: string, config: Partial<LLMProviderConfig>) => void;
  removeLLMProvider: (id: string) => void;
  toggleLLMProvider: (id: string) => void;
  testLLMConnection: (id: string) => Promise<boolean>;
  
  // Actions for MCP servers
  addMCPServer: (config: Omit<MCPServerConfig, 'id' | 'status'>) => void;
  updateMCPServer: (id: string, config: Partial<MCPServerConfig>) => void;
  removeMCPServer: (id: string) => void;
  toggleMCPServer: (id: string) => void;
  testMCPConnection: (id: string) => Promise<boolean>;
  
  // Actions for preferences
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
  changeLanguage: (language: Language) => void;
  changeTheme: (theme: Theme) => void;
  
  // General actions
  loadSettings: () => Promise<void>;
  saveSettings: () => Promise<void>;
  resetSettings: () => void;
  exportSettings: () => string;
  importSettings: (settingsJson: string) => Promise<boolean>;
  importMCPServers: (mcpConfigJson: string) => Promise<boolean>;
}

// Default settings
const defaultSettings: Settings = {
  llmProviders: [],
  mcpServers: [],
  preferences: {
    theme: 'system',
    language: 'en',
    autoScroll: true,
    soundEnabled: false,
  },
};

// Generate unique ID
const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
};

// Encrypt/decrypt functions for API keys (basic implementation)
const encryptApiKey = (apiKey: string): string => {
  if (!apiKey) return '';
  try {
    // In a real implementation, use proper encryption
    // For now, just base64 encode (NOT secure, just for demo)
    return btoa(apiKey);
  } catch (error) {
    console.warn('Failed to encrypt API key:', error);
    return apiKey;
  }
};

const decryptApiKey = (encryptedKey: string): string => {
  if (!encryptedKey) return '';
  try {
    return atob(encryptedKey);
  } catch (error) {
    console.warn('Failed to decrypt API key:', error);
    return encryptedKey; // Return as-is if decryption fails
  }
};

// Storage utilities
const STORAGE_KEY = 'mcp-chat-ui-settings';

const saveToStorage = (settings: Settings): void => {
  try {
    // Validate settings before saving
    if (!settings || typeof settings !== 'object') {
      throw new Error('Invalid settings object');
    }

    // Encrypt API keys before storing
    const settingsToStore = {
      ...settings,
      llmProviders: (settings.llmProviders || []).map(provider => ({
        ...provider,
        apiKey: encryptApiKey(provider.apiKey || ''),
      })),
    };
    
    const serialized = JSON.stringify(settingsToStore);
    localStorage.setItem(STORAGE_KEY, serialized);
  } catch (error) {
    console.error('Failed to save settings to localStorage:', error);
    throw error; // Re-throw to allow caller to handle
  }
};

const loadFromStorage = (): Settings => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return { ...defaultSettings };
    
    const parsed = JSON.parse(stored);
    
    // Validate parsed data structure
    if (!parsed || typeof parsed !== 'object') {
      console.warn('Invalid settings data in localStorage, using defaults');
      return { ...defaultSettings };
    }
    
    // Decrypt API keys after loading and merge with defaults
    const settings: Settings = {
      ...defaultSettings,
      ...parsed,
      llmProviders: (parsed.llmProviders || []).map((provider: any) => ({
        id: provider.id || generateId(),
        name: provider.name || 'openai',
        apiKey: decryptApiKey(provider.apiKey || ''),
        baseUrl: provider.baseUrl,
        models: provider.models || [],
        enabled: provider.enabled !== false, // Default to true
      })),
      mcpServers: (parsed.mcpServers || []).map((server: any) => ({
        id: server.id || generateId(),
        name: server.name || '',
        command: server.command || '',
        args: Array.isArray(server.args) ? server.args : [],
        env: server.env || {},
        enabled: server.enabled !== false, // Default to true
        status: server.status || 'disconnected',
      })),
      preferences: {
        ...defaultSettings.preferences,
        ...parsed.preferences,
      },
    };
    
    return settings;
  } catch (error) {
    console.error('Failed to load settings from localStorage:', error);
    return { ...defaultSettings };
  }
};

export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set, get) => ({
      // Initial state
      ...defaultSettings,
      isLoading: false,
      isSaving: false,
      
      // LLM Provider actions
      addLLMProvider: (config) => {
        const newProvider: LLMProviderConfig = {
          ...config,
          id: generateId(),
        };
        
        set((state) => ({
          llmProviders: [...state.llmProviders, newProvider],
        }));
        
        get().saveSettings();
      },
      
      updateLLMProvider: (id, config) => {
        set((state) => ({
          llmProviders: state.llmProviders.map(provider =>
            provider.id === id ? { ...provider, ...config } : provider
          ),
        }));
        
        get().saveSettings();
      },
      
      removeLLMProvider: (id) => {
        set((state) => ({
          llmProviders: state.llmProviders.filter(provider => provider.id !== id),
        }));
        
        get().saveSettings();
      },
      
      toggleLLMProvider: (id) => {
        set((state) => ({
          llmProviders: state.llmProviders.map(provider =>
            provider.id === id ? { ...provider, enabled: !provider.enabled } : provider
          ),
        }));
        
        get().saveSettings();
      },
      
      testLLMConnection: async (id) => {
        const provider = get().llmProviders.find(p => p.id === id);
        if (!provider) return false;
        
        try {
          // Mock connection test - in real implementation, make actual API call
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Simulate success/failure based on API key presence
          return provider.apiKey.length > 0;
        } catch (error) {
          console.error('LLM connection test failed:', error);
          return false;
        }
      },
      
      // MCP Server actions
      addMCPServer: (config) => {
        const newServer: MCPServerConfig = {
          ...config,
          id: generateId(),
          status: 'disconnected',
        };
        
        set((state) => ({
          mcpServers: [...state.mcpServers, newServer],
        }));
        
        get().saveSettings();
      },
      
      updateMCPServer: (id, config) => {
        set((state) => ({
          mcpServers: state.mcpServers.map(server =>
            server.id === id ? { ...server, ...config } : server
          ),
        }));
        
        get().saveSettings();
      },
      
      removeMCPServer: (id) => {
        set((state) => ({
          mcpServers: state.mcpServers.filter(server => server.id !== id),
        }));
        
        get().saveSettings();
      },
      
      toggleMCPServer: (id) => {
        set((state) => ({
          mcpServers: state.mcpServers.map(server =>
            server.id === id ? { ...server, enabled: !server.enabled } : server
          ),
        }));
        
        get().saveSettings();
      },
      
      testMCPConnection: async (id) => {
        const server = get().mcpServers.find(s => s.id === id);
        if (!server) return false;
        
        try {
          // Mock connection test - in real implementation, test actual MCP connection
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Update server status
          get().updateMCPServer(id, { status: 'connected' });
          return true;
        } catch (error) {
          console.error('MCP connection test failed:', error);
          get().updateMCPServer(id, { status: 'error' });
          return false;
        }
      },
      
      // Preferences actions
      updatePreferences: (preferences) => {
        set((state) => ({
          preferences: { ...state.preferences, ...preferences },
        }));
        
        get().saveSettings();
      },
      
      changeLanguage: (language) => {
        set((state) => ({
          preferences: { ...state.preferences, language },
        }));
        
        // Update i18n language
        // Note: This will be handled by the i18n initialization
        // The actual language change will be managed by the i18n system
        try {
          // In a real implementation, this would trigger i18n language change
          console.debug('Language changed to:', language);
        } catch (error) {
          console.warn('Failed to update i18n language:', error);
        }
        
        get().saveSettings();
      },
      
      changeTheme: (theme) => {
        set((state) => ({
          preferences: { ...state.preferences, theme },
        }));
        
        // Apply theme to document
        const applyTheme = () => {
          const root = document.documentElement;
          if (theme === 'dark') {
            root.classList.add('dark');
          } else if (theme === 'light') {
            root.classList.remove('dark');
          } else {
            // System theme
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (prefersDark) {
              root.classList.add('dark');
            } else {
              root.classList.remove('dark');
            }
          }
        };

        // Apply theme immediately
        applyTheme();

        // Listen for system theme changes if using system theme
        if (theme === 'system') {
          const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
          const handleSystemThemeChange = () => applyTheme();
          
          // Remove existing listener if any
          mediaQuery.removeEventListener('change', handleSystemThemeChange);
          // Add new listener
          mediaQuery.addEventListener('change', handleSystemThemeChange);
        }
        
        get().saveSettings();
      },
      
      // General actions
      loadSettings: async () => {
        set({ isLoading: true });
        
        try {
          const settings = loadFromStorage();
          set({ ...settings, isLoading: false });
          
          // Apply theme after loading
          get().changeTheme(settings.preferences.theme);
        } catch (error) {
          console.error('Failed to load settings:', error);
          set({ isLoading: false });
        }
      },
      
      saveSettings: async () => {
        set({ isSaving: true });
        
        try {
          const { isLoading, isSaving, ...settings } = get();
          saveToStorage(settings);
          set({ isSaving: false });
        } catch (error) {
          console.error('Failed to save settings:', error);
          set({ isSaving: false });
          throw error; // Re-throw to allow UI to show error
        }
      },
      
      resetSettings: () => {
        set({ ...defaultSettings });
        localStorage.removeItem(STORAGE_KEY);
      },
      
      exportSettings: () => {
        const { isLoading, isSaving, ...settings } = get();
        return JSON.stringify(settings, null, 2);
      },
      
      importSettings: async (settingsJson) => {
        try {
          if (!settingsJson || typeof settingsJson !== 'string') {
            throw new Error('Invalid settings JSON string');
          }

          const settings = JSON.parse(settingsJson);
          
          // Validate settings structure
          if (!settings || typeof settings !== 'object') {
            throw new Error('Invalid settings format: not an object');
          }

          if (!Array.isArray(settings.llmProviders)) {
            throw new Error('Invalid settings format: llmProviders must be an array');
          }

          if (!Array.isArray(settings.mcpServers)) {
            throw new Error('Invalid settings format: mcpServers must be an array');
          }

          if (!settings.preferences || typeof settings.preferences !== 'object') {
            throw new Error('Invalid settings format: preferences must be an object');
          }
          
          // Merge with defaults to ensure all required fields are present
          const validatedSettings: Settings = {
            llmProviders: settings.llmProviders.map((provider: any) => ({
              id: provider.id || generateId(),
              name: provider.name || 'openai',
              apiKey: provider.apiKey || '',
              baseUrl: provider.baseUrl,
              models: Array.isArray(provider.models) ? provider.models : [],
              enabled: provider.enabled !== false,
            })),
            mcpServers: settings.mcpServers.map((server: any) => ({
              id: server.id || generateId(),
              name: server.name || '',
              command: server.command || '',
              args: Array.isArray(server.args) ? server.args : [],
              env: server.env || {},
              enabled: server.enabled !== false,
              status: server.status || 'disconnected',
            })),
            preferences: {
              ...defaultSettings.preferences,
              ...settings.preferences,
            },
          };
          
          set({ ...defaultSettings, ...validatedSettings });
          await get().saveSettings();
          
          return true;
        } catch (error) {
          console.error('Failed to import settings:', error);
          return false;
        }
      },

      importMCPServers: async (mcpConfigJson) => {
        try {
          const newServers = importMCPServersFromJSON(mcpConfigJson);
          
          if (newServers.length === 0) {
            throw new Error('No valid MCP servers found in configuration');
          }

          set((state) => ({
            mcpServers: [...state.mcpServers, ...newServers],
          }));

          await get().saveSettings();
          return true;
        } catch (error) {
          console.error('Failed to import MCP servers:', error);
          return false;
        }
      },
    }),
    {
      name: STORAGE_KEY,
      // Only persist the settings data, not the loading states or actions
      partialize: (state) => ({
        llmProviders: state.llmProviders,
        mcpServers: state.mcpServers,
        preferences: state.preferences,
      }),
    }
  )
);

// Helper function to import MCP servers from JSON config format
export const importMCPServersFromJSON = (mcpConfigJson: string): MCPServerConfig[] => {
  try {
    const config = JSON.parse(mcpConfigJson);
    
    // Support the format: {"mcpServers": {"server-name": {"command": "...", "args": [...]}}}
    if (config.mcpServers && typeof config.mcpServers === 'object') {
      return Object.entries(config.mcpServers).map(([name, serverConfig]: [string, any]) => ({
        id: generateId(),
        name,
        command: serverConfig.command || '',
        args: Array.isArray(serverConfig.args) ? serverConfig.args : [],
        env: serverConfig.env || {},
        enabled: serverConfig.enabled !== false,
        status: 'disconnected' as const,
      }));
    }
    
    // Support direct array format: [{"name": "...", "command": "...", "args": [...]}]
    if (Array.isArray(config)) {
      return config.map((serverConfig: any) => ({
        id: generateId(),
        name: serverConfig.name || '',
        command: serverConfig.command || '',
        args: Array.isArray(serverConfig.args) ? serverConfig.args : [],
        env: serverConfig.env || {},
        enabled: serverConfig.enabled !== false,
        status: 'disconnected' as const,
      }));
    }
    
    return [];
  } catch (error) {
    console.error('Failed to parse MCP servers JSON:', error);
    return [];
  }
};

// Initialize settings on app start
export const initializeSettings = async () => {
  const store = useSettingsStore.getState();
  await store.loadSettings();
};