import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button, Textarea } from './ui';

const Chat: React.FC = () => {
  const { t } = useTranslation();
  const [message, setMessage] = useState('');

  const handleSendMessage = () => {
    if (message.trim()) {
      // TODO: Implement message sending logic
      console.log('Sending message:', message);
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-800">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 lg:p-6">
        <div className="max-w-4xl mx-auto">
          {/* Welcome message */}
          <div className="text-center py-8 lg:py-12">
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 lg:p-8 max-w-md mx-auto">
              <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                {t('chat.sessionTitle', 'Chat Session')}
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {t('chat.noMessages', 'No messages yet. Start a conversation!')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Input area */}
      <div className="flex-shrink-0 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
        <div className="p-4 lg:p-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-end space-x-3">
              <div className="flex-1">
                <Textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={t('chat.messagePlaceholder', 'Type your message here...')}
                  autoResize
                  minRows={1}
                  maxRows={4}
                  fullWidth
                />
              </div>
              <Button
                onClick={handleSendMessage}
                disabled={!message.trim()}
                className="px-4 py-2 h-11 flex-shrink-0"
                aria-label={t('chat.sendMessage', 'Send message')}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                <span className="ml-2 hidden sm:inline">
                  {t('chat.sendMessage', 'Send')}
                </span>
              </Button>
            </div>
            
            {/* Helper text */}
            <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-center">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
