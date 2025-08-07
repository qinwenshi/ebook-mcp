import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button, Modal, Select } from './ui';

interface NewChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateChat: (provider: string, model: string) => void;
}

const NewChatModal: React.FC<NewChatModalProps> = ({
  isOpen,
  onClose,
  onCreateChat,
}) => {
  const { t } = useTranslation();
  const [selectedProvider, setSelectedProvider] = useState('');
  const [selectedModel, setSelectedModel] = useState('');

  const providerOptions = [
    { value: 'openai', label: t('providers.openai', 'OpenAI') },
    { value: 'deepseek', label: t('providers.deepseek', 'DeepSeek') },
    { value: 'openrouter', label: t('providers.openrouter', 'OpenRouter') },
  ];

  const modelOptions = {
    openai: [
      { value: 'gpt-4', label: 'GPT-4' },
      { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
      { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
    ],
    deepseek: [
      { value: 'deepseek-chat', label: 'DeepSeek Chat' },
      { value: 'deepseek-coder', label: 'DeepSeek Coder' },
    ],
    openrouter: [
      { value: 'anthropic/claude-3-sonnet', label: 'Claude 3 Sonnet' },
      { value: 'anthropic/claude-3-haiku', label: 'Claude 3 Haiku' },
      { value: 'meta-llama/llama-3-70b-instruct', label: 'Llama 3 70B' },
    ],
  };

  const handleCreateChat = () => {
    if (selectedProvider && selectedModel) {
      onCreateChat(selectedProvider, selectedModel);
      handleClose();
    }
  };

  const handleClose = () => {
    setSelectedProvider('');
    setSelectedModel('');
    onClose();
  };

  const handleProviderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedProvider(e.target.value);
    setSelectedModel(''); // Reset model when provider changes
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title={t('chat.newChat', 'New Chat')}
      size="md"
    >
      <div className="space-y-4">
        <div className="text-sm text-gray-600 dark:text-gray-400 mb-4">
          {t('chat.newChatDescription', 'Select an LLM provider and model to start a new conversation.')}
        </div>
        
        <Select
          label={t('chat.selectProvider', 'Select LLM Provider')}
          options={providerOptions}
          value={selectedProvider}
          onChange={handleProviderChange}
          placeholder={t('chat.selectProvider', 'Select LLM Provider')}
          fullWidth
        />
        
        {selectedProvider && (
          <Select
            label={t('chat.selectModel', 'Select Model')}
            options={modelOptions[selectedProvider as keyof typeof modelOptions] || []}
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            placeholder={t('chat.selectModel', 'Select Model')}
            fullWidth
          />
        )}
        
        {selectedProvider && selectedModel && (
          <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-md">
            <div className="text-sm text-blue-800 dark:text-blue-200">
              <div className="font-medium mb-1">
                {t('chat.selectedConfiguration', 'Selected Configuration:')}
              </div>
              <div>
                <span className="font-medium">{t('chat.provider', 'Provider')}:</span> {t(`providers.${selectedProvider}`, selectedProvider)}
              </div>
              <div>
                <span className="font-medium">{t('chat.model', 'Model')}:</span> {selectedModel}
              </div>
            </div>
          </div>
        )}
        
        <div className="flex justify-end space-x-3 pt-4">
          <Button
            variant="outline"
            onClick={handleClose}
          >
            {t('common.cancel', 'Cancel')}
          </Button>
          <Button
            variant="primary"
            onClick={handleCreateChat}
            disabled={!selectedProvider || !selectedModel}
          >
            {t('chat.createChat', 'Create Chat')}
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default NewChatModal;