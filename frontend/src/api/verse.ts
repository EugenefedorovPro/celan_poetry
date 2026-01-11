import AxiosInstance from "../api/http";

// types/verse.ts

export type Lang = "ru" | "uk" | "en";

export type VerseTranslationType = {
  id: number;
  lang: Lang;
  lang_display: string;
  title: string;
  text: string;
  translator: string;
  source: string;
  year: number | null;
};

export type WordType = {
  id: number;
  lemma: string;
  freq: number;
  neologism: boolean;
};

export type WordTranslationType = {
  id: number;
  lemma: string;
  word_id: string;
  lang: Lang;
  lang_display: string;
  sense: string;
  trans: string;
};

export type VerseType = {
  id: number;
  title: string;
  text: string;
  collection_name: string;
  year_writing: number;
  year_publication: number;
  verse_translations: VerseTranslationType[];
  words: WordType[];
  word_translations: WordTranslationType[];
};

export const verseApi = async (verseId: number): Promise<VerseType> => {
  const url = `/verse/${verseId}/`;
  const response = await AxiosInstance.get<VerseType>(url);
  return response.data;
};
