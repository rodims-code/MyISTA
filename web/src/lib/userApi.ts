import api from "./index"

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