<script lang="ts">
	import { onMount } from 'svelte';
	import {
		fetchPosts,
		createPost,
		likePost,
		createComment,
		toggleFavorite,
		searchNetworkUsers
	} from '$lib/networkApi';
	import PostCard from '$lib/components/network/PostCard.svelte';
	import CreatePostModal from '$lib/components/network/CreatePostModal.svelte';
	import { goto } from '$app/navigation';
	import { Search, X, UserRound } from 'lucide-svelte';

	let posts: any[] = [];
	let isLoading = true;
	let searchQuery = '';
	let userResults: any[] = [];
	let isSearchingUsers = false;
	let searchTimer: ReturnType<typeof setTimeout>;

	$: normalizedSearch = searchQuery.trim().toLowerCase();
	$: filteredPosts = normalizedSearch
		? posts.filter((post) => {
				const searchable = [
					post.content,
					post.author_details?.username,
					post.author_details?.filiere,
					post.author_details?.niveau,
					post.fichier?.split('/').pop()
				]
					.filter(Boolean)
					.join(' ')
					.toLowerCase();

				return searchable.includes(normalizedSearch);
			})
		: posts;

	onMount(async () => {
		await loadPosts();
	});

	async function loadPosts() {
		isLoading = true;
		posts = await fetchPosts();
		isLoading = false;
	}

	async function handleCreatePost(event: CustomEvent) {
		try {
			const newPost = await createPost(event.detail);
			posts = [newPost, ...posts];
		} catch (error) {
			console.error(error);
			alert('Erreur lors de la création du post');
		}
	}

	async function handleLike(event: CustomEvent) {
		const postId = event.detail;
		try {
			const res = await likePost(postId);

			posts = posts.map((p) => {
				if (p.id === postId) {
					return {
						...p,
						is_liked: res.status === 'liked',
						likes_count: res.status === 'liked' ? p.likes_count + 1 : Math.max(0, p.likes_count - 1)
					};
				}
				return p;
			});
		} catch (error) {
			console.error('Erreur like:', error);
		}
	}

	async function handleFavorite(event: CustomEvent) {
		const postId = event.detail;
		try {
			const res = await toggleFavorite(postId);

			posts = posts.map((p) => {
				if (p.id === postId) {
					const isFavorited = res.status === 'saved';
					return {
						...p,
						is_favorited: isFavorited,
						favorites_count: isFavorited
							? (p.favorites_count || 0) + 1
							: Math.max(0, (p.favorites_count || 0) - 1)
					};
				}
				return p;
			});
		} catch (error) {
			console.error('Erreur favori:', error);
		}
	}

	async function handleComment(event: CustomEvent) {
		const { postId } = event.detail;
		try {
			posts = posts.map((p) => {
				if (p.id === postId) {
					return { ...p, comments_count: p.comments_count + 1 };
				}
				return p;
			});
		} catch (error) {
			console.error('Erreur comment:', error);
		}
	}

	function goToProfile(event: CustomEvent) {
		const user = event.detail;
		goto(`/dashboard/profile/${user}`);
	}

	function handleSearchInput() {
		clearTimeout(searchTimer);

		if (searchQuery.trim().length < 2) {
			userResults = [];
			isSearchingUsers = false;
			return;
		}

		isSearchingUsers = true;
		searchTimer = setTimeout(async () => {
			userResults = await searchNetworkUsers(searchQuery);
			isSearchingUsers = false;
		}, 250);
	}

	function clearSearch() {
		searchQuery = '';
		userResults = [];
		isSearchingUsers = false;
		clearTimeout(searchTimer);
	}
</script>

<div class="mx-auto max-w-2xl py-4">
	<div class="mb-6">
		<h1 class="mb-2 text-2xl font-bold">Fil d'actualité</h1>
		<p class="text-sm text-base-content/60">Découvrez ce qui se passe sur le campus.</p>

		<div class="relative mt-4">
			<label class="input-bordered input w-full rounded-full">
				<Search size={18} class="opacity-50" />
				<input
					type="search"
					class="grow"
					placeholder="Rechercher posts, profils, filières..."
					bind:value={searchQuery}
					oninput={handleSearchInput}
				/>
				{#if searchQuery}
					<button
						class="btn btn-circle btn-ghost btn-xs"
						onclick={clearSearch}
						aria-label="Effacer"
					>
						<X size={14} />
					</button>
				{/if}
			</label>

			{#if normalizedSearch}
				<div
					class="absolute z-20 mt-2 w-full overflow-hidden rounded-2xl border border-base-200 bg-base-100 shadow-xl"
				>
					<div class="flex items-center justify-between border-b border-base-200 px-4 py-3 text-sm">
						<span class="font-semibold">{filteredPosts.length} publication(s)</span>
						{#if isSearchingUsers}
							<span class="loading loading-xs loading-spinner text-primary"></span>
						{:else}
							<span class="text-base-content/50">{userResults.length} profil(s)</span>
						{/if}
					</div>

					{#if userResults.length > 0}
						<div class="max-h-64 overflow-y-auto p-2">
							{#each userResults as user}
								<button
									class="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left hover:bg-base-200"
									onclick={() => goto(`/dashboard/profile/${user.id}`)}
								>
									<div class="placeholder avatar">
										<div class="h-9 w-9 rounded-full bg-primary text-primary-content">
											<span>{user.username?.charAt(0).toUpperCase() || 'U'}</span>
										</div>
									</div>
									<div class="min-w-0 flex-1">
										<p class="truncate text-sm font-bold">{user.username}</p>
										<p class="truncate text-xs text-base-content/50">
											{user.filiere || 'ISTA'}
											{user.niveau ? `- ${user.niveau}` : ''}
										</p>
									</div>
									<UserRound size={16} class="text-base-content/40" />
								</button>
							{/each}
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</div>

	<CreatePostModal on:submit={handleCreatePost} />

	{#if isLoading}
		<div class="flex justify-center py-10">
			<span class="loading loading-lg loading-spinner text-primary"></span>
		</div>
	{:else if posts.length === 0}
		<div class="rounded-2xl border border-dashed border-base-300 bg-base-200 py-10 text-center">
			<p class="text-base-content/60">Aucun post pour le moment.</p>
			<p class="mt-1 text-sm text-base-content/40">Soyez le premier à publier !</p>
		</div>
	{:else if filteredPosts.length === 0}
		<div class="rounded-2xl border border-dashed border-base-300 bg-base-200 py-10 text-center">
			<p class="text-base-content/60">Aucun résultat pour « {searchQuery} ».</p>
		</div>
	{:else}
		<div class="flex flex-col">
			{#each filteredPosts as post (post.id)}
				<PostCard
					{post}
					on:like={handleLike}
					on:comment={handleComment}
					on:favorite={handleFavorite}
					on:userClick={goToProfile}
				/>
			{/each}
		</div>
	{/if}
</div>
