import AxiosInstance from "../api/http";

export interface VerseInterface {
  id: number;
  title: string;
  text: string;
  collection: string;
}

export const verseApi = async (verseId: number): Promise<VerseInterface> => {
  const url = `/verse/${verseId}/`;
  const response = await AxiosInstance.get<VerseInterface>(url);
  return response.data;
};
