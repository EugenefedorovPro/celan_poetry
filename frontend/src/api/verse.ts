import AxiosInstance from "../api/http";

export interface VerseInterface {
  id: number;
  title: string;
  text: string;
  collection: string;
  year_writing: number;
  year_publication: number;
}

export const verseApi = async (verseId: number): Promise<VerseInterface> => {
  const url = `/verse/${verseId}/`;
  const response = await AxiosInstance.get<VerseInterface>(url);
  return response.data;
};
