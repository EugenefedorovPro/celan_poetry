import AxiosInstance from "./http";

export interface CollectionInterface {
  pk: number;
  name: string;
  genre: string;
  year_publication: number;
  is_real_celan_collection: string;
  number_verses: number;
  notes: string;
}

export const collectionApi = async (): Promise<CollectionInterface[]> => {
  const url: string = "/collection/";
  try {
    const response = await AxiosInstance.get<CollectionInterface[]>(url);
    return response.data;
  } catch (error) {
    console.log("Failed to fetch Collection", error);
    throw error;
  }
};

