// frontend/src/api/AxiosInterceptor.tsx
import axios, { AxiosHeaders } from "axios";

import type {
  AxiosError,
  AxiosInstance,
  AxiosRequestHeaders,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from "axios";

type TokenRefreshResponse = {
  access: string;
  refresh?: string;
};

type RetryableConfig = InternalAxiosRequestConfig & {
  __isRetryRequest?: boolean;
};

function isTokenExpiredError(err: unknown): boolean {
  if (!err || typeof err !== "object") return false;

  const maybeAxiosErr = err as { response?: { data?: unknown } };
  const data = maybeAxiosErr.response?.data;

  if (!data || typeof data !== "object") return false;

  const messages = (data as { messages?: unknown }).messages;
  if (!Array.isArray(messages) || messages.length === 0) return false;

  const first = messages[0];
  if (!first || typeof first !== "object") return false;

  const message = (first as { message?: unknown }).message;
  return typeof message === "string" && message.includes("Token is expired");
}

function setAuthorizationHeader(
  config: InternalAxiosRequestConfig,
  token: string
): void {
  // Axios v1 often uses AxiosHeaders internally
  if (config.headers instanceof AxiosHeaders) {
    config.headers.set("Authorization", `Bearer ${token}`);
    return;
  }

  // Otherwise treat it like a plain object
  const headersObj: Record<string, string> = config.headers
    ? (config.headers as unknown as Record<string, string>)
    : {};

  headersObj.Authorization = `Bearer ${token}`;
  config.headers = headersObj as unknown as AxiosRequestHeaders;
}

const axiosInstance: AxiosInstance = axios.create({
  baseURL: "http://localhost:8004",
});

const REFRESH_URL = "/token/refresh/";

axiosInstance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = localStorage.getItem("access_token");
    if (accessToken) {
      setAuthorizationHeader(config, accessToken);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

async function resendRequest(
  instance: AxiosInstance,
  config: InternalAxiosRequestConfig
): Promise<AxiosResponse<unknown>> {
  return instance.request<unknown>(config);
}

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<unknown>) => {
    if (!error.config) return Promise.reject(error);

    const config: RetryableConfig = error.config as RetryableConfig;

    // avoid infinite loop
    const isRefreshCall =
      typeof config.url === "string" && config.url.includes(REFRESH_URL);

    if (isRefreshCall || config.__isRetryRequest) {
      return Promise.reject(error);
    }

    if (!isTokenExpiredError(error)) {
      return Promise.reject(error);
    }

    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) return Promise.reject(error);

      const refreshResp = await axiosInstance.post<TokenRefreshResponse>(
        REFRESH_URL,
        { refresh: refreshToken }
      );

      const { access, refresh } = refreshResp.data;

      localStorage.setItem("access_token", access);
      if (refresh) localStorage.setItem("refresh_token", refresh);

      config.__isRetryRequest = true;
      setAuthorizationHeader(config, access);

      return await resendRequest(axiosInstance, config);
    } catch (refreshErr) {
      return Promise.reject(refreshErr);
    }
  }
);

export default axiosInstance;
