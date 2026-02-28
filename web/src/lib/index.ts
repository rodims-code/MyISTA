// place files you want to import through the `$lib` alias in this folder.
import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants";

const api = axios.create({
  baseURL: process.env.VITE_API_URL,
});

// Intercepteur requête → ajoute le token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur réponse → gère le refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 || error.response?.status === 403) {
      try {
        const refresh = localStorage.getItem(REFRESH_TOKEN);
        if (refresh) {
          // Demande un nouveau access
          const res = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}api/token/refresh/`,
            { refresh }
          );

          localStorage.setItem(ACCESS_TOKEN, res.data.access);

          // Met à jour le header et rejoue la requête
          originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
          return api(originalRequest);
        }
      } catch (err) {
        // Refresh invalide → déconnexion
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        window.location.href = "/auth/login";
      }
    }

    return Promise.reject(error);
  }
);

export default api;