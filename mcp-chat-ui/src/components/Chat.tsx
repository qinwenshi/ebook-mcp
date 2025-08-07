import React from 'react';
import { useTranslation } from 'react-i18next';

const Chat: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
        {t('navigation.chat')}
      </h2>
      <div className="space-y-4">
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <p className="text-gray-600 dark:text-gray-300">
            {t('chat.noMessages')}
          </p>
        </div>
        <div className="flex space-x-2">
          <input
            type="text"
            placeholder={t('chat.messagePlaceholder')}
            className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
          />
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
            {t('chat.sendMessage')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
