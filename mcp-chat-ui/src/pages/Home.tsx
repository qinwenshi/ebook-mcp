import React from 'react';
import { useTranslation } from 'react-i18next';
import { Chat, ServerList, LanguageSelector } from '@/components';

const Home: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="space-y-6">
      {/* Header with language selector */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          {t('navigation.home')}
        </h1>
        <LanguageSelector className="w-48" />
      </div>
      
      {/* Main content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <ServerList />
        </div>
        <div className="lg:col-span-2">
          <Chat />
        </div>
      </div>
    </div>
  );
};

export default Home;
