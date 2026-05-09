import api from "./index";

export async function fetchPosts() {
  try {
    const res = await api.get("api/network/posts/");
    return res.data;
  } catch (error) {
    console.error("Erreur récupération posts:", error);
    return [];
  }
}

export async function createPost(formData: FormData) {
  try {
    const res = await api.post("api/network/posts/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return res.data;
  } catch (error) {
    console.error("Erreur création post:", error);
    throw error;
  }
}

export async function likePost(postId: number) {
  try {
    const res = await api.post(`api/network/posts/${postId}/like/`);
    return res.data;
  } catch (error) {
    console.error("Erreur like post:", error);
    throw error;
  }
}

export async function fetchComments(postId: number) {
  // Optionnel si les commentaires sont inclus dans le post ou récupérés séparément
  try {
    const res = await api.get(`api/network/comments/?post=${postId}`);
    return res.data;
  } catch (error) {
    console.error("Erreur récupération commentaires:", error);
    return [];
  }
}

export async function createComment(postId: number, content: string) {
  try {
    const res = await api.post("api/network/comments/", {
      post: postId,
      content,
    });
    return res.data;
  } catch (error) {
    console.error("Erreur création commentaire:", error);
    throw error;
  }
}

export async function toggleFollow(followingId: string | number) {
  try {
    const res = await api.post("api/network/follows/toggle/", {
      following_id: followingId,
    });
    return res.data;
  } catch (error) {
    console.error("Erreur toggle follow:", error);
    throw error;
  }
}

export async function fetchFollows() {
  try {
    const res = await api.get("api/network/follows/");
    return res.data;
  } catch (error) {
    console.error("Erreur récupération follows:", error);
    return [];
  }
}
