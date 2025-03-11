export interface Paste {
  id: string;
  content: string;
  createdAt: Date;
  language?: string;
  expiresAt?: Date;
}

export type LanguageOption = {
  value: string;
  label: string;
  ext: string;
};
