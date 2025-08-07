import React from 'react';
import { useTranslation } from 'react-i18next';
import { Card } from '@/components/ui';
import { LanguageSelector } from '@/components';

const SettingsPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-4xl mx-auto p-6">
        {/* Settings header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {t('navigation.settings', 'Settings')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {t('settings.description', 'Configure your MCP Chat UI preferences and connections')}
          </p>
        </div>

        {/* Settings sections */}
        <div className="space-y-6">
          {/* General Settings */}
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              {t('settings.general', 'General')}
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {t('settings.language', 'Language')}
                </label>
                <LanguageSelector />
              </div>
            </div>
          </Card>

          {/* LLM Provider Settings */}
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              {t('settings.llmProvider', 'LLM Provider')}
            </h2>
            <div className="text-gray-600 dark:text-gray-400">
              {t('settings.llmProviderDescription', 'Configure your AI model provider and API credentials')}
            </div>
            {/* Placeholder for LLM provider configuration */}
          </Card>

          {/* MCP Server Settings */}
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              {t('settings.mcpServers', 'MCP Servers')}
            </h2>
            <div className="text-gray-600 dark:text-gray-400">
              {t('settings.mcpServersDescription', 'Manage your Model Context Protocol server connections')}
            </div>
            {/* Placeholder for MCP server configuration */}
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;