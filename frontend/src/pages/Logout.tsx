import { useEffect } from "react";
import AxiosInstance from "../api/http";

export const Logout = () => {
  useEffect(() => {
    AxiosInstance.post("/logout/")
      .catch(() => {}) // backend failure should not block logout
      .finally(() => {
        localStorage.clear();
        delete AxiosInstance.defaults.headers.common["Authorization"];
        window.location.replace("/login");
      });
  }, []);

  return null;
};
