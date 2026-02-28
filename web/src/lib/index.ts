// place files you want to import through the `$lib` alias in this folder.
import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants";
// 1. On utilise l'import officiel de SvelteKit pour les variables d'env
import { PUBLIC_API_URL } from '$env/static/public'; 
import { browser } from '$app/environment';
import { goto } from '$app/navigation';

const api = axios.create({
    // Utilise la variable importée ci-dessus
    baseURL: PUBLIC_API_URL, 
});

// Intercepteur requête
api.interceptors.request.use(
    (config) => {
        // On vérifie qu'on est dans le navigateur avant de toucher au localStorage
        if (browser) {
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Intercepteur réponse
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Éviter une boucle infinie si le refresh lui-même échoue (401)
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refresh = localStorage.getItem(REFRESH_TOKEN);
                if (refresh) {
                    // On utilise la baseURL configurée plus haut
                    const res = await axios.post(`${PUBLIC_API_URL}api/token/refresh/`, { 
                        refresh 
                    });

                    const newAccessToken = res.data.access;
                    localStorage.setItem(ACCESS_TOKEN, newAccessToken);

                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return api(originalRequest);
                }
            } catch (err) {
                localStorage.removeItem(ACCESS_TOKEN);
                localStorage.removeItem(REFRESH_TOKEN);
                
                if (browser) {
                    goto('/auth/login'); // Utilisation de goto au lieu de window.location
                }
            }
        }
        return Promise.reject(error);
    }
);

export default api;