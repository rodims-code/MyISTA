<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchFavorites, likePost, toggleFavorite } from '$lib/networkApi';
	import PostCard from '$lib/components/network/PostCard.svelte';
	import { goto } from '$app/navigation';
	import { Bookmark } from 'lucide-svelte';

	let favoriteItems: any[] = [];
	let isLoading = true;

	$: posts = favoriteItems.map((item) => item.post_details).filter(Boolean);

	onMount(async () => {
		favoriteItems = await fetchFavorites();
		isLoading = false;
	});

	async function handleLike(event: CustomEvent) {
		const postId = event.detail;
		try {
			const res = await likePost(postId);
			favoriteItems = favoriteItems.map((item) => {
				if (item.post_details?.id === postId) {
					const post = item.post_details;
					return {
						...item,
						post_details: {
							...post,
							is_liked: res.status === 'liked',
							likes_count:
								res.status === 'liked' ? post.likes_count + 1 : Math.max(0, post.likes_count - 1)
						}
					};
				}
				return item;
			});
		} catch (error) {
			console.error('Erreur like:', error);
		}
	}

	async function handleFavorite(event: CustomEvent) {
		const postId = event.detail;
		try {
			const res = await toggleFavorite(postId);
			if (res.status === 'removed') {
				favoriteItems = favoriteItems.filter((item) => item.post_details?.id !== postId);
			}
		} catch (error) {
			console.error('Erreur favori:', error);
		}
	}

	function goToProfile(event: CustomEvent) {
		goto(`/dashboard/profile/${event.detail}`);
	}
</script>

<div class="mx-auto max-w-2xl py-4">
	<div class="mb-6">
		<h1 class="text-2xl font-bold">Favoris</h1>
		<p class="text-sm text-base-content/60">Publications enregistrées pour les retrouver vite.</p>
	</div>

	{#if isLoading}
		<div class="flex justify-center py-16">
			<span class="loading loading-lg loading-spinner text-primary"></span>
		</div>
	{:else if posts.length === 0}
		<div class="rounded-2xl border border-dashed border-base-300 bg-base-200 py-14 text-center">
			<Bookmark class="mx-auto mb-3 text-base-content/30" size={40} />
			<p class="text-base-content/60">Aucune publication enregistrée.</p>
		</div>
	{:else}
		<div class="flex flex-col">
			{#each posts as post (post.id)}
				<PostCard
					{post}
					on:like={handleLike}
					on:favorite={handleFavorite}
					on:userClick={goToProfile}
				/>
			{/each}
		</div>
	{/if}
</div>
