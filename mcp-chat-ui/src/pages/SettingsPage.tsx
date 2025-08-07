import React from 'react';
import { useTranslation } from 'react-i18next';
import { Card } from '@/components/ui';
import { LanguageSelector } from '@/components';
import SettingsTest from '@/components/SettingsTest';

const SettingsPage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="h-full overflow-y-auto">
      {/* Settings Test Interface */}
      <SettingsTest />
    </div>
  );
};

export default SettingsPage;