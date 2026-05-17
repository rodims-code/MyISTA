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
	<title>Mon Profil & Paramètres — MyISTA</title>
</svelte:head>

{#if loading}
	<div class="flex justify-center py-20">
		<Loader2 size={40} class="animate-spin text-primary" />
	</div>
{:else}
	<div class="flex flex-col gap-6 max-w-6xl mx-auto">
		<!-- En-tête du Profil (Banner, Avatar, Stats) -->
		<div class="card bg-base-100 shadow-sm border border-base-200 overflow-hidden">
			<!-- Bannière -->
			<div class="h-32 bg-gradient-to-r from-primary/30 via-secondary/30 to-primary/20 relative"></div>
			
			<div class="px-6 pb-6 relative">
				<div class="flex flex-col sm:flex-row justify-between items-start sm:items-end -mt-12 mb-4 gap-4">
					<div class="avatar">
						<div class="w-24 h-24 rounded-full ring-4 ring-base-100 bg-gradient-to-tr from-primary to-secondary text-primary-content flex items-center justify-center text-4xl font-bold shadow-lg">
							<span>{userData?.username?.charAt(0).toUpperCase() || 'U'}</span>
						</div>
					</div>
					
					<!-- Statistiques Desktop/Tablette (en haut à droite) -->
					<div class="hidden sm:flex gap-8 text-center bg-base-200/50 p-3 rounded-2xl">
						<div class="flex flex-col">
							<span class="text-2xl font-bold">{userPosts.length}</span>
							<span class="text-xs text-base-content/60 font-semibold uppercase tracking-wider">Posts</span>
						</div>
						<div class="flex flex-col">
							<span class="text-2xl font-bold">{followersCount}</span>
							<span class="text-xs text-base-content/60 font-semibold uppercase tracking-wider">Abonnés</span>
						</div>
						<div class="flex flex-col">
							<span class="text-2xl font-bold">{followingCount}</span>
							<span class="text-xs text-base-content/60 font-semibold uppercase tracking-wider">Abonnements</span>
						</div>
					</div>
				</div>
				
				<div>
					<h1 class="text-2xl font-bold text-base-content">{userData.username}</h1>
					<p class="text-sm font-medium text-base-content/60 mt-1">
						{userData.filiere || 'Filière non définie'} • {userData.niveau || 'Niveau non défini'} • <span class="badge badge-sm badge-outline">{userData.role}</span>
					</p>
				</div>

				<!-- Statistiques Mobile (en bas) -->
				<div class="flex sm:hidden justify-around mt-6 pt-4 border-t border-base-200 text-center">
					<div class="flex flex-col">
						<span class="text-xl font-bold">{userPosts.length}</span>
						<span class="text-xs text-base-content/60 font-semibold uppercase tracking-wider">Posts</span>
					</div>
					<div class="flex flex-col">
						<span class="text-xl font-bold">{followersCount}</span>
						<span class="text-xs text-base-content/60 font-semibold uppercase tracking-wider">Abonnés</span>
					</div>
					<div class="flex flex-col">
						<span class="text-xl font-bold">{followingCount}</span>
						<span class="text-xs text-base-content/60 font-semibold uppercase tracking-wider">Suivis</span>
					</div>
				</div>
			</div>
		</div>

		<!-- Contenu Principal (Paramètres à gauche, Posts à droite) -->
		<div class="flex flex-col lg:flex-row gap-6 items-start">
			
			<!-- Colonne de Gauche : Formulaires de Paramètres -->
			<div class="w-full lg:w-1/3 flex flex-col gap-6 lg:sticky lg:top-6">
				
				<!-- Carte Informations Personnelles -->
				<div class="card bg-base-100 shadow-sm border border-base-200">
					<div class="card-body p-5">
						<div class="flex items-center gap-3 mb-4">
							<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
								<User size={20} />
							</div>
							<div>
								<h3 class="text-sm font-bold text-base-content">Informations</h3>
								<p class="text-xs text-base-content/40">Modifier votre profil</p>
							</div>
						</div>

						{#if successMsg}
							<div class="alert py-2 text-sm alert-success mb-4 flex items-center gap-2">
								<CheckCircle2 size={16} />
								{successMsg}
							</div>
						{/if}
						{#if errorMsg}
							<div class="alert py-2 text-sm alert-error mb-4">{errorMsg}</div>
						{/if}

						<div class="space-y-4">
							<div class="form-control">
								<label class="label pb-1"><span class="label-text font-medium">Matricule</span></label>
								<input type="text" class="input-bordered input input-sm w-full bg-base-200/50" value={userData.matricule} disabled />
							</div>

							<div class="form-control">
								<label class="label pb-1"><span class="label-text font-medium">Nom d'utilisateur</span></label>
								<input type="text" class="input-bordered input input-sm w-full focus:input-primary" bind:value={userData.username} />
							</div>

							<button class="btn btn-primary btn-sm mt-4 w-full gap-2" onclick={handleSave} disabled={saving}>
								{#if saving}
									<Loader2 size={16} class="animate-spin" />
								{:else}
									<Save size={16} />
								{/if}
								Enregistrer
							</button>
						</div>
					</div>
				</div>

				<!-- Carte Apparence -->
				<div class="card bg-base-100 shadow-sm border border-base-200">
					<div class="card-body p-5">
						<div class="flex items-center gap-3 mb-4">
							<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-base-200 text-base-content/60">
								<Settings size={20} />
							</div>
							<div>
								<h3 class="text-sm font-bold text-base-content">Apparence</h3>
								<p class="text-xs text-base-content/40">Personnalisez le thème</p>
							</div>
						</div>

						<div class="dropdown w-full">
							<div tabindex="0" role="button" class="btn btn-outline btn-sm w-full justify-between">
								Choisir un thème
								<svg width="12px" height="12px" class="inline-block h-2 w-2 fill-current opacity-60" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048"><path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path></svg>
							</div>
							<ul tabindex="-1" class="dropdown-content z-1 w-full rounded-box bg-base-300 p-2 shadow-2xl mt-1">
								<li><input type="radio" name="theme-dropdown" class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm" aria-label="Cupcake (Clair)" value="cupcake" bind:group={$theme} /></li>
								<li><input type="radio" name="theme-dropdown" class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm" aria-label="Black (Sombre)" value="black" bind:group={$theme} /></li>
								<li><input type="radio" name="theme-dropdown" class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm" aria-label="CMYK" value="cmyk" bind:group={$theme} /></li>
								<li><input type="radio" name="theme-dropdown" class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm" aria-label="Caramel Latte" value="caramellatte" bind:group={$theme} /></li>
								<li><input type="radio" name="theme-dropdown" class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm" aria-label="Light" value="light" bind:group={$theme} /></li>
							</ul>
						</div>
					</div>
				</div>
			</div>

			<!-- Colonne de Droite : Publications -->
			<div class="flex-1 flex flex-col w-full">
				<h2 class="text-lg font-bold text-base-content mb-4 px-2">Mon mur de publications</h2>
				
				<div class="flex flex-col gap-4">
					{#if userPosts.length === 0}
						<div class="text-center py-16 bg-base-100 rounded-2xl border border-base-200 border-dashed shadow-sm">
							<div class="w-16 h-16 rounded-full bg-base-200 flex items-center justify-center mx-auto mb-4">
								<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-base-content/40"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
							</div>
							<h3 class="font-bold text-base-content/80">Aucune publication</h3>
							<p class="text-sm text-base-content/50 mt-1 max-w-xs mx-auto">Vous n'avez pas encore partagé de contenu avec le réseau.</p>
						</div>
					{:else}
						{#each userPosts as post (post.id)}
							<PostCard {post} on:like={handleLike} />
						{/each}
					{/if}
				</div>
			</div>

		</div>
	</div>
{/if}
