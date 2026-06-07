import api from './index';

export async function fetchPosts() {
	try {
		const res = await api.get('api/network/posts/');
		return res.data;
	} catch (error) {
		console.error('Erreur récupération posts:', error);
		return [];
	}
}

export async function createPost(formData: FormData) {
	try {
		const res = await api.post('api/network/posts/', formData, {
			headers: {
				'Content-Type': 'multipart/form-data'
			}
		});
		return res.data;
	} catch (error) {
		console.error('Erreur création post:', error);
		throw error;
	}
}

export async function likePost(postId: number) {
	try {
		const res = await api.post(`api/network/posts/${postId}/like/`);
		return res.data;
	} catch (error) {
		console.error('Erreur like post:', error);
		throw error;
	}
}

export async function fetchComments(postId: number) {
	// Optionnel si les commentaires sont inclus dans le post ou récupérés séparément
	try {
		const res = await api.get(`api/network/comments/?post=${postId}`);
		return res.data;
	} catch (error) {
		console.error('Erreur récupération commentaires:', error);
		return [];
	}
}

export async function createComment(postId: number, content: string) {
	try {
		const res = await api.post('api/network/comments/', {
			post: postId,
			content
		});
		return res.data;
	} catch (error) {
		console.error('Erreur création commentaire:', error);
		throw error;
	}
}

export async function toggleFollow(followingId: string | number) {
	try {
		const res = await api.post('api/network/follows/toggle/', {
			following_id: followingId
		});
		return res.data;
	} catch (error) {
		console.error('Erreur toggle follow:', error);
		throw error;
	}
}

export async function fetchFollows() {
	try {
		const res = await api.get('api/network/follows/');
		return res.data;
	} catch (error) {
		console.error('Erreur récupération follows:', error);
		return [];
	}
}

export async function toggleFavorite(postId: number) {
	try {
		const res = await api.post(`api/network/posts/${postId}/favorite/`);
		return res.data;
	} catch (error) {
		console.error('Erreur favori post:', error);
		throw error;
	}
}

export async function fetchFavorites() {
	try {
		const res = await api.get('api/network/favorites/');
		return res.data;
	} catch (error) {
		console.error('Erreur rÃ©cupÃ©ration favoris:', error);
		return [];
	}
}

export async function fetchConversations() {
	try {
		const res = await api.get('api/network/conversations/');
		return res.data;
	} catch (error) {
		console.error('Erreur rÃ©cupÃ©ration conversations:', error);
		return [];
	}
}

export async function createConversation(participantId: string | number) {
	try {
		const res = await api.post('api/network/conversations/', {
			participant_id: participantId
		});
		return res.data;
	} catch (error) {
		console.error('Erreur crÃ©ation conversation:', error);
		throw error;
	}
}

export async function fetchMessages(conversationId: string | number) {
	try {
		const res = await api.get(`api/network/conversations/${conversationId}/messages/`);
		return res.data;
	} catch (error) {
		console.error('Erreur rÃ©cupÃ©ration messages:', error);
		return [];
	}
}

export async function sendMessage(conversationId: string | number, formData: FormData) {
	try {
		const res = await api.post(`api/network/conversations/${conversationId}/messages/`, formData, {
			headers: {
				'Content-Type': 'multipart/form-data'
			}
		});
		return res.data;
	} catch (error) {
		console.error('Erreur envoi message:', error);
		throw error;
	}
}

export async function markConversationSeen(conversationId: string | number) {
	try {
		const res = await api.post(`api/network/conversations/${conversationId}/mark_seen/`);
		return res.data;
	} catch (error) {
		console.error('Erreur lecture conversation:', error);
		throw error;
	}
}

export async function fetchNotifications() {
	try {
		const res = await api.get('api/network/notifications/');
		return res.data;
	} catch (error) {
		console.error('Erreur rÃ©cupÃ©ration notifications:', error);
		return [];
	}
}

export async function markNotificationRead(notificationId: string | number) {
	try {
		const res = await api.post(`api/network/notifications/${notificationId}/mark_read/`);
		return res.data;
	} catch (error) {
		console.error('Erreur lecture notification:', error);
		throw error;
	}
}

export async function markAllNotificationsRead() {
	try {
		const res = await api.post('api/network/notifications/mark_all_read/');
		return res.data;
	} catch (error) {
		console.error('Erreur lecture notifications:', error);
		throw error;
	}
}

export async function searchNetworkUsers(query: string) {
	if (!query.trim()) return [];

	try {
		const res = await api.get('api/network/users/', {
			params: { q: query.trim() }
		});
		return res.data;
	} catch (error) {
		console.error('Erreur recherche utilisateurs:', error);
		return [];
	}
}
