<script lang="ts">
	import { Heart, MessageCircle, FileText, Download, Share2, Bookmark } from 'lucide-svelte';
	import CommentSection from './CommentSection.svelte';
	import { createEventDispatcher, onMount } from 'svelte';
	import { fetchComments } from '$lib/networkApi';

	export let post: any;

	const dispatch = createEventDispatcher();

	let showComments = false;
	let comments: any[] = [];
	let isLoadingComments = false;

	async function loadComments() {
		if (showComments && comments.length === 0 && post.comments_count > 0) {
			isLoadingComments = true;
			comments = await fetchComments(post.id);
			isLoadingComments = false;
		}
	}

	function toggleComments() {
		showComments = !showComments;
		loadComments();
	}

	function handleLike() {
		dispatch('like', post.id);
	}

	function handleFavorite() {
		dispatch('favorite', post.id);
	}

	async function handleCommentSubmit(event: CustomEvent) {
		const { postId, content } = event.detail;
		try {
			const newComment = await import('$lib/networkApi').then((m) =>
				m.createComment(postId, content)
			);
			comments = [...comments, newComment];
			post.comments_count++;
			dispatch('comment', { postId, content }); // Notify parent if it wants to know
		} catch (error) {
			console.error('Erreur lors de la création du commentaire', error);
		}
	}

	// Permet au parent de mettre à jour la liste des commentaires (optionnel)
	export function updateComments(newComment: any) {
		comments = [...comments, newComment];
		post.comments_count++;
	}

	function formatDate(dateString: string) {
		const date = new Date(dateString);
		return date.toLocaleDateString('fr-FR', {
			day: 'numeric',
			month: 'short',
			hour: '2-digit',
			minute: '2-digit'
		});
	}

	let isImageModalOpen = false;

	function openImage() {
		isImageModalOpen = true;
	}

	function closeImage() {
		isImageModalOpen = false;
	}
</script>

<div
	class="relative mb-8 overflow-hidden rounded-[2rem] border border-base-200/50 bg-base-100 shadow-xl shadow-base-200/50 transition-all duration-300 hover:shadow-2xl hover:shadow-base-200"
>
	{#if post.image}
		<!-- IMAGE LAYOUT AVEC OVERLAY GLASSMORPHISM -->
		<div class="group relative w-full">
			<!-- L'image en fond -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<img
				src={post.image}
				alt="Post media"
				class="max-h-[600px] min-h-[400px] w-full cursor-pointer object-cover"
				onclick={openImage}
			/>

			<!-- Bouton d'expansion en haut à droite pour bien montrer qu'on peut cliquer -->
			<button
				class="btn absolute top-4 right-4 btn-circle border-0 bg-black/30 text-white opacity-0 backdrop-blur-md transition-opacity btn-sm group-hover:opacity-100 hover:bg-black/50"
				onclick={openImage}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="16"
					height="16"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					><path d="M15 3h6v6" /><path d="M9 21H3v-6" /><path d="M21 3l-7 7" /><path
						d="M3 21l7-7"
					/></svg
				>
			</button>

			<!-- Fading Blur Background Overlay -->
			<div
				class="pointer-events-none absolute right-0 bottom-0 left-0 h-64"
				style="backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); mask-image: linear-gradient(to top, black 60%, transparent 100%); -webkit-mask-image: linear-gradient(to top, black 60%, transparent 100%);"
			>
				<div
					class="absolute inset-0 bg-gradient-to-t from-base-100/90 via-base-100/40 to-transparent"
				></div>
			</div>

			<!-- Contenu textuel par dessus le blur -->
			<div class="absolute right-0 bottom-0 left-0 p-5 pt-12">
				<!-- Author Info -->
				<div class="mb-3 flex items-center justify-between">
					<div class="flex items-center gap-3">
						<div
							class="placeholder avatar cursor-pointer"
							onclick={() => dispatch('userClick', post.author)}
						>
							<div
								class="flex w-10 items-center justify-center rounded-full bg-gradient-to-tr from-primary to-secondary text-primary-content shadow-md"
							>
								<span class="text-base font-bold"
									>{post.author_details?.username?.charAt(0).toUpperCase() || 'U'}</span
								>
							</div>
						</div>
						<div>
							<h3
								class="cursor-pointer text-sm font-bold drop-shadow-sm transition-colors hover:text-primary"
								onclick={() => dispatch('userClick', post.author)}
							>
								{post.author_details?.username}
							</h3>
							<p class="text-[10px] font-medium tracking-wide uppercase opacity-80">
								{formatDate(post.created_at)} • {post.author_details?.filiere || 'Étudiant'}
							</p>
						</div>
					</div>
				</div>

				<!-- Text Content -->
				{#if post.content}
					<p
						class="mb-4 line-clamp-3 text-sm leading-relaxed font-medium whitespace-pre-wrap drop-shadow-sm"
					>
						{post.content}
					</p>
				{/if}

				<!-- Actions -->
				<div class="flex items-center justify-between">
					<div class="flex gap-2">
						<button
							class="btn gap-2 rounded-full border-0 px-4 btn-sm {post.is_liked
								? 'bg-white/70 text-error hover:bg-white/90 dark:bg-black/50 dark:hover:bg-black/70'
								: 'bg-white/50 shadow-sm hover:bg-white/70 dark:bg-black/40 dark:hover:bg-black/60'}"
							onclick={handleLike}
						>
							<Heart size={18} fill={post.is_liked ? 'currentColor' : 'none'} />
							<span class="font-bold drop-shadow-sm">{post.likes_count || 0}</span>
						</button>

						<button
							class="btn gap-2 rounded-full border-0 bg-white/50 px-4 shadow-sm btn-sm hover:bg-white/70 dark:bg-black/40 dark:hover:bg-black/60"
							onclick={toggleComments}
						>
							<MessageCircle size={18} />
							<span class="font-bold drop-shadow-sm">{post.comments_count || 0}</span>
						</button>
					</div>

					<div class="flex gap-2">
						<button
							class="btn btn-circle border-0 btn-sm {post.is_favorited
								? 'bg-white/70 text-warning hover:bg-white/90 dark:bg-black/50 dark:hover:bg-black/70'
								: 'bg-white/50 hover:bg-white/70 dark:bg-black/40 dark:hover:bg-black/60'} shadow-sm"
							onclick={handleFavorite}
							aria-label="Enregistrer"
						>
							<Bookmark size={16} fill={post.is_favorited ? 'currentColor' : 'none'} />
						</button>
						<button
							class="btn btn-circle border-0 bg-white/50 shadow-sm btn-sm hover:bg-white/70 dark:bg-black/40 dark:hover:bg-black/60"
						>
							<Share2 size={16} />
						</button>
					</div>
				</div>
			</div>
		</div>
	{:else}
		<!-- TEXT/FILE ONLY LAYOUT (NO IMAGE) -->
		<div class="p-5">
			<!-- Header: User Info -->
			<div class="mb-4 flex items-center justify-between">
				<div class="flex items-center gap-4">
					<div
						class="placeholder avatar cursor-pointer"
						onclick={() => dispatch('userClick', post.author)}
					>
						<div
							class="flex w-12 items-center justify-center rounded-full bg-gradient-to-tr from-primary to-secondary text-primary-content shadow-md"
						>
							<span class="text-xl font-bold"
								>{post.author_details?.username?.charAt(0).toUpperCase() || 'U'}</span
							>
						</div>
					</div>
					<div>
						<h3
							class="cursor-pointer text-base font-bold transition-colors hover:text-primary"
							onclick={() => dispatch('userClick', post.author)}
						>
							{post.author_details?.username}
						</h3>
						<p class="mt-0.5 text-xs font-medium tracking-wide text-base-content/50 uppercase">
							{formatDate(post.created_at)} • {post.author_details?.filiere || 'Étudiant'}
						</p>
					</div>
				</div>
			</div>

			<!-- Content -->
			{#if post.content}
				<div class="pb-4">
					<p class="text-[15px] leading-relaxed whitespace-pre-wrap text-base-content/90">
						{post.content}
					</p>
				</div>
			{/if}

			<!-- Actions -->
			<div class="mt-2 flex items-center justify-between border-t border-base-200/50 pt-2">
				<div class="flex gap-2">
					<button
						class="btn gap-2 rounded-full px-4 btn-ghost btn-sm {post.is_liked
							? 'bg-error/10 text-error'
							: 'text-base-content/70 hover:bg-error/10 hover:text-error'}"
						onclick={handleLike}
					>
						<Heart size={20} fill={post.is_liked ? 'currentColor' : 'none'} />
						<span class="font-bold">{post.likes_count || 0}</span>
					</button>

					<button
						class="btn gap-2 rounded-full px-4 text-base-content/70 btn-ghost btn-sm hover:bg-primary/10 hover:text-primary"
						onclick={toggleComments}
					>
						<MessageCircle size={20} />
						<span class="font-bold">{post.comments_count || 0}</span>
					</button>
				</div>

				<div class="flex gap-1">
					<button
						class="btn btn-circle btn-ghost btn-sm {post.is_favorited
							? 'bg-warning/10 text-warning'
							: 'text-base-content/70 hover:bg-warning/10 hover:text-warning'}"
						onclick={handleFavorite}
						aria-label="Enregistrer"
					>
						<Bookmark size={18} fill={post.is_favorited ? 'currentColor' : 'none'} />
					</button>
					<button class="btn btn-circle text-base-content/70 btn-ghost btn-sm hover:bg-base-200">
						<Share2 size={18} />
					</button>
				</div>
			</div>
		</div>
	{/if}

	<!-- Media: Fichier (s'affiche toujours en dessous si présent) -->
	{#if post.fichier}
		<div class="px-5 pt-2 pb-5 {post.image ? 'bg-base-100' : ''}">
			<div
				class="bg-base-50 group flex cursor-pointer items-center justify-between rounded-2xl border border-base-200 p-4 shadow-sm transition-colors hover:bg-base-200/50"
			>
				<div class="flex items-center gap-4 overflow-hidden">
					<div
						class="rounded-xl bg-secondary/10 p-3 text-secondary transition-transform group-hover:scale-110"
					>
						<FileText size={24} />
					</div>
					<div>
						<span class="block truncate text-sm font-bold"
							>{post.fichier.split('/').pop() || 'Document joint'}</span
						>
						<span class="text-xs text-base-content/50">Fichier attaché</span>
					</div>
				</div>
				<a
					href={post.fichier}
					target="_blank"
					class="btn btn-circle shadow-md btn-sm btn-primary"
					download
					onclick={(e) => e.stopPropagation()}
				>
					<Download size={16} />
				</a>
			</div>
		</div>
	{/if}

	<!-- Comments Section (S'affiche en dessous du blur si ouvert) -->
	{#if showComments}
		<div class="border-t border-base-200/50 bg-base-100 px-5 pt-4 pb-5">
			{#if isLoadingComments}
				<div class="flex justify-center py-6">
					<span class="loading loading-md loading-spinner text-primary"></span>
				</div>
			{:else}
				<CommentSection {comments} postId={post.id} on:submit={handleCommentSubmit} />
			{/if}
		</div>
	{/if}
</div>

<!-- Image Modal (Vue sans blur) -->
{#if isImageModalOpen && post.image}
	<div
		class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4 backdrop-blur-sm"
		onclick={closeImage}
	>
		<button
			class="btn absolute top-4 right-4 btn-circle text-white btn-ghost hover:bg-white/20"
			onclick={closeImage}
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				width="24"
				height="24"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round"><path d="M18 6 6 18" /><path d="m6 6 12 12" /></svg
			>
		</button>
		<!-- Image en entier SANS BLUR OVERLAY -->
		<img
			src={post.image}
			alt="Post media full"
			class="max-h-full max-w-full rounded-xl object-contain shadow-2xl"
			onclick={(e) => e.stopPropagation()}
		/>
	</div>
{/if}
