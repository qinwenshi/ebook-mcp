import { useTranslation } from 'react-i18next';
import { useCallback } from 'react';

export type SupportedLanguage = 'en' | 'zh';

export const SUPPORTED_LANGUAGES: SupportedLanguage[] = ['en', 'zh'];

export const LANGUAGE_NAMES: Record<SupportedLanguage, string> = {
  en: 'English',
  zh: '中文',
};

export const useLanguage = () => {
  const { i18n } = useTranslation();

  const currentLanguage = i18n.language as SupportedLanguage;

  const changeLanguage = useCallback(
    async (language: SupportedLanguage) => {
      try {
        await i18n.changeLanguage(language);
        // Store the language preference in localStorage
        localStorage.setItem('i18nextLng', language);
      } catch (error) {
        console.error('Failed to change language:', error);
      }
    },
    [i18n]
  );

  const isLanguageSupported = useCallback(
    (language: string): language is SupportedLanguage => {
      return SUPPORTED_LANGUAGES.includes(language as SupportedLanguage);
    },
    []
  );

  const getLanguageName = useCallback(
    (language: SupportedLanguage) => {
      return LANGUAGE_NAMES[language];
    },
    []
  );

  return {
    currentLanguage,
    changeLanguage,
    isLanguageSupported,
    getLanguageName,
    supportedLanguages: SUPPORTED_LANGUAGES,
    languageNames: LANGUAGE_NAMES,
  };
};