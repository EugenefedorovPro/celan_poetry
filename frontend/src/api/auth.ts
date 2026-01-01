import AxiosInstance from "./http";

export type LoginResponse = {
  access: string;
  refresh: string;
};

export async function login(
  username: string,
  password: string
): Promise<LoginResponse> {
  const { data } = await AxiosInstance.post<LoginResponse>(
    "/token/",
    { username, password },
    {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true,
    }
  );

  // persist tokens
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);

  return data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}
