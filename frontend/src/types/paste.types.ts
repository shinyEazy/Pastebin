export interface Paste {
  id: string;
  content: string;
  created_at: Date;
  expire_at?: string;
  views: number;
}

// export type LanguageOption = {
//   value: string;
//   label: string;
//   ext: string;
// };
