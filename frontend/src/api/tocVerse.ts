import AxiosInstance from "./http";

export interface TocVerseInterface {
  id: number;
  title: string;
}

export const tocVerseApi = async (
  collectionId: number
): Promise<TocVerseInterface[]> => {
  const url: string = `/collection/${collectionId}/verses/toc/`;
  const response = await AxiosInstance.get<TocVerseInterface[]>(url);
  return response.data;
};
