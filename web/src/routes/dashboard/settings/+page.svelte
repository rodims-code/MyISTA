<script lang="ts">
	import { Settings, User, Save, Loader2, CheckCircle2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { ACCESS_TOKEN } from '$lib/constants';
	import { fetchCurrentUser, updateCurrentUser } from '$lib/userApi';
	import { theme } from '$lib/theme';
	import { fetchPosts, likePost } from '$lib/networkApi';
	import PostCard from '$lib/components/network/PostCard.svelte';

	let userData = $state<any>({});
	let loading = $state(true);
	let saving = $state(false);
	let successMsg = $state('');
	let errorMsg = $state('');
	
	// Nouvelles variables pour le profil
	let userPosts = $state<any[]>([]);
	let followersCount = $state(0);
	let followingCount = $state(0);

	onMount(async () => {
		try {
			userData = await fetchCurrentUser();
			if (!userData) {
				errorMsg = 'Impossible de charger votre profil.';
			} else {
				// Charger les posts de l'utilisateur
				const allPosts = await fetchPosts();
				userPosts = allPosts.filter((p: any) => p.author === userData.id);

				// Charger les stats de follow
				try {
					const resFollows = await api.get('api/network/follows/');
					const allFollows = resFollows.data;
					followersCount = allFollows.filter((f: any) => f.following === userData.id).length;
					followingCount = allFollows.filter((f: any) => f.follower === userData.id).length;
				} catch (e) {
					console.error('Erreur chargement follows:', e);
				}
			}
		} catch (err) {
			console.error('Erreur chargement profil:', err);
			errorMsg = 'Impossible de charger votre profil.';
		} finally {
			loading = false;
		}
	});

	async function handleSave() {
		saving = true;
		successMsg = '';
		errorMsg = '';
		try {
			const { matricule, date_inscription, role, ...updateData } = userData;
			userData = await updateCurrentUser(updateData);
			successMsg = 'Profil mis à jour avec succès !';
			setTimeout(() => (successMsg = ''), 3000);
		} catch (err) {
			errorMsg = 'Une erreur est survenue lors de la sauvegarde.';
		} finally {
			saving = false;
		}
	}

	async function handleLike(event: CustomEvent) {
		const postId = event.detail;
		try {
			const res = await likePost(postId);
			userPosts = userPosts.map((p) => {
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
</script>

<svelte:head>
	<title>Paramètres — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-6">
	<div>
		<h2 class="text-2xl font-bold text-base-content">Paramètres</h2>
		<p class="mt-1 text-sm text-base-content/50">
			Gérez vos préférences et informations personnelles
		</p>
	</div>

	<div class="flex flex-col gap-6 lg:flex-row">
		<div class="card w-full max-w-2xl border border-base-200 bg-base-100 shadow-sm">
			<div class="card-body gap-5 p-6">
				<div class="mb-2 flex items-center justify-between">
					<div class="flex items-center gap-3">
						<div
							class="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary"
						>
							<User size={20} />
						</div>
						<div>
							<h3 class="text-sm font-bold text-base-content">Profil utilisateur</h3>
							<p class="text-xs text-base-content/40">Informations de votre compte</p>
						</div>
					</div>
					{#if successMsg}
						<div class="badge animate-bounce gap-2 badge-success">
							<CheckCircle2 size={14} />
							{successMsg}
						</div>
					{/if}
				</div>

				{#if loading}
					<div class="flex justify-center py-10">
						<Loader2 size={32} class="animate-spin text-primary" />
					</div>
				{:else}
					<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
						<div class="form-control">
							<label class="label pb-1"><span class="label-text font-medium">Matricule</span></label
							>
							<input type="text" class="input-bordered input" value={userData.matricule} disabled />
							<label class="label"
								><span class="label-text-alt text-base-content/40 italic">Non modifiable</span
								></label
							>
						</div>

						<div class="form-control">
							<label class="label pb-1"
								><span class="label-text font-medium">Nom d'utilisateur</span></label
							>
							<input
								type="text"
								class="input-bordered input focus:input-primary"
								bind:value={userData.username}
							/>
						</div>

						<div class="form-control">
							<label class="label pb-1"><span class="label-text font-medium">Rôle</span></label>
							<input type="text" class="input-bordered input" value={userData.role} disabled />
						</div>

						<div class="form-control">
							<label class="label pb-1"><span class="label-text font-medium">Niveau</span></label>
							<input
								type="text"
								class="input-bordered input"
								value={userData.niveau || 'Non défini'}
								disabled
							/>
						</div>

						<div class="form-control">
							<label class="label pb-1"><span class="label-text font-medium">Filière</span></label>
							<input
								type="text"
								class="input-bordered input"
								value={userData.filiere || 'Non défini'}
								disabled
							/>
						</div>
					</div>

					{#if errorMsg}
						<div class="alert py-2 text-sm alert-error">{errorMsg}</div>
					{/if}

					<button class="btn mt-2 gap-2 btn-primary" onclick={handleSave} disabled={saving}>
						{#if saving}
							<Loader2 size={16} class="animate-spin" />
						{:else}
							<Save size={16} />
						{/if}
						Sauvegarder les modifications
					</button>
				{/if}
			</div>
		</div>

		<div class="card max-w-lg border border-base-200 bg-base-100 shadow-sm">
			<div class="card-body gap-4 p-6">
				<div class="flex items-center gap-3">
					<div
						class="flex h-10 w-10 items-center justify-center rounded-xl bg-base-200 text-base-content/50"
					>
						<Settings size={20} />
					</div>
					<div>
						<h3 class="text-sm font-bold text-base-content">Apparence</h3>
						<p class="text-xs text-base-content/40">Personnalisez l'interface</p>
					</div>
				</div>
				<div class="form-control">

					<div class="dropdown mb-72">
						<div tabindex="0" role="button" class="btn m-1">
							Theme
							<svg
								width="12px"
								height="12px"
								class="inline-block h-2 w-2 fill-current opacity-60"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 2048 2048"
							>
								<path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path>
							</svg>
						</div>
						<ul
							tabindex="-1"
							class="dropdown-content z-1 w-52 rounded-box bg-base-300 p-2 shadow-2xl"
						>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="Cupcake (Light)"
									value="cupcake"
									bind:group={$theme}
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="black"
									value="black"
									bind:group={$theme}
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="cmyk"
									value="cmyk"
									bind:group={$theme}
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="caramellatte"
									value="caramellatte"
									bind:group={$theme}
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="light"
									value="light"
									bind:group={$theme}
								/>
							</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Section Profil & Publications (Fusion) -->
	{#if !loading}
		<div class="mt-6">
			<h2 class="text-xl font-bold text-base-content mb-4">Mes Publications & Statistiques</h2>
			
			<div class="flex flex-col lg:flex-row gap-6">
				<!-- Statistiques -->
				<div class="card w-full lg:w-1/3 h-fit border border-base-200 bg-base-100 shadow-sm">
					<div class="card-body p-6 text-center">
						<div class="avatar mx-auto mb-4">
							<div class="w-24 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2 bg-primary text-primary-content flex items-center justify-center text-4xl font-bold">
								<span>{userData?.username?.charAt(0).toUpperCase() || 'U'}</span>
							</div>
						</div>
						<h3 class="text-lg font-bold">{userData.username}</h3>
						<p class="text-sm text-base-content/60 mb-4">{userData.filiere || 'Étudiant'}</p>
						
						<div class="flex justify-center gap-6 border-t border-base-200 pt-4">
							<div class="flex flex-col">
								<span class="text-xl font-bold">{userPosts.length}</span>
								<span class="text-xs text-base-content/60 uppercase tracking-wider">Posts</span>
							</div>
							<div class="flex flex-col">
								<span class="text-xl font-bold">{followersCount}</span>
								<span class="text-xs text-base-content/60 uppercase tracking-wider">Abonnés</span>
							</div>
							<div class="flex flex-col">
								<span class="text-xl font-bold">{followingCount}</span>
								<span class="text-xs text-base-content/60 uppercase tracking-wider">Abonnements</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Liste des publications -->
				<div class="flex-1 flex flex-col gap-4">
					{#if userPosts.length === 0}
						<div class="text-center py-10 bg-base-200 rounded-2xl border border-base-300 border-dashed">
							<p class="text-base-content/60">Vous n'avez pas encore publié de post.</p>
						</div>
					{:else}
						{#each userPosts as post (post.id)}
							<PostCard {post} on:like={handleLike} />
						{/each}
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
