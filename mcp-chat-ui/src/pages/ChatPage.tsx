import React from 'react';
import { useTranslation } from 'react-i18next';
import { Chat } from '@/components';

const ChatPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="h-full flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Chat header - hidden on mobile since it's in the top bar */}
      <div className="hidden lg:block flex-shrink-0 px-6 py-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
            {t('navigation.chat', 'Chat')}
          </h1>
          {/* Future: Add chat controls like new chat, model selector, etc. */}
        </div>
      </div>

      {/* Chat content */}
      <div className="flex-1 overflow-hidden">
        <Chat />
      </div>
    </div>
  );
};

export default ChatPage;