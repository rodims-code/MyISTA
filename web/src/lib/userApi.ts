import api from "./index"
import {ACCESS_TOKEN} from "./constants"

export async function fetchCurrentUser() {
  try {
    const res = await api.get("api/user/me/");
    console.log(res.data);
    return res.data; // { id, username, email, role }
  } catch (error) {
    console.error("Erreur récupération user:", error);
    return null;
  }
}

// Mettre à jour l'utilisateur connecté
export async function updateCurrentUser(payload: any) {
  try {
    const res = await api.patch("api/user/me/", payload);
    return res.data;
  } catch (error) {
    console.error("Erreur mise à jour user:", error);
    throw error;
  }
}

export async function fetchCurrentSalle(formData: FormData) {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (!token) {
    throw new Error("No access token found");
  }
  return await api.get("api/salles/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
export async function fetchCurrentBatiments() {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (!token) {
    throw new Error("No access token found");
  }
  return await api.get("api/batiments/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}