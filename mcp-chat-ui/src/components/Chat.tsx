import React from 'react';
import { useTranslation } from 'react-i18next';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import ToolConfirmationDialog from './ToolConfirmationDialog';
import { useChatStore } from '../store/chatStore';

const Chat: React.FC = () => {
  const { t } = useTranslation();
  
  // Get chat state from store
  const {
    messages,
    isLoading,
    pendingToolCall,
    sendMessage,
    deleteMessage,
    confirmToolCall,
    cancelToolCall,
  } = useChatStore();

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-800">
      {/* Messages area */}
      <MessageList
        messages={messages}
        isLoading={isLoading}
        autoScroll={true}
        onDeleteMessage={deleteMessage}
        className="p-4 lg:p-6"
      />

      {/* Input area */}
      <MessageInput
        onSendMessage={sendMessage}
        isLoading={isLoading}
        placeholder={t('chat.messagePlaceholder')}
      />

      {/* Tool Confirmation Dialog */}
      <ToolConfirmationDialog
        isOpen={!!pendingToolCall}
        toolCall={pendingToolCall}
        onConfirm={confirmToolCall}
        onCancel={cancelToolCall}
        isExecuting={isLoading}
      />
    </div>
  );
};

export default Chat;
