<script lang="ts">
	import { Info, Calendar, Tag, ChevronRight, Loader2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { fetchCurrentUser } from '$lib/userApi';

	let infos = $state<any[]>([]);
	let loading = $state(true);
	let currentUser = $state<any>(null);

	onMount(async () => {
		try {
			currentUser = await fetchCurrentUser();
			const res = await api.get('/api/infos/');
			infos = res.data;
		} catch (error) {
			console.error('Erreur chargement infos:', error);
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>Infos Essentielles — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-8">
	<!-- Header -->
	<div>
		<h2 class="text-2xl font-bold text-base-content">Infos Essentielles</h2>
		<p class="mt-1 text-sm text-base-content/50">
			Dernières nouvelles et annonces importantes de l'ISTA
		</p>
	</div>

	{#if loading}
		<div class="flex flex-col items-center justify-center gap-4 py-20">
			<Loader2 size={40} class="animate-spin text-primary/40" />
			<p class="font-medium text-base-content/40">Chargement des annonces...</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-6">
			{#each infos as info}
				<div
					class="group card overflow-hidden border border-base-200 bg-base-100 shadow-sm transition-all hover:shadow-md"
				>
					<div class="flex flex-col md:flex-row">
						<!-- Left accent color bar based on category or default -->
						<div class="h-2 w-full bg-primary md:h-auto md:w-2"></div>

						<div class="card-body flex-1 p-6">
							<div class="mb-4 flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
								<div class="flex items-center gap-2">
									{#if info.categorie}
										<div class="badge gap-1 badge-outline px-3 py-3 badge-primary">
											<Tag size={12} />
											{info.categorie}
										</div>
									{/if}
									<span class="flex items-center gap-1 text-xs font-medium text-base-content/40">
										<Calendar size={12} />
										{new Date(info.created_at).toLocaleDateString()}
									</span>
									{#if currentUser && currentUser.role !== 'student'}
										<span class="badge badge-sm {info.statut === 'approuve' ? 'badge-success badge-outline' : 'badge-warning badge-outline'}">
											{info.statut === 'approuve' ? 'Approuvé' : 'En attente'}
										</span>
									{/if}
								</div>
							</div>

							<h3
								class="mb-3 text-xl font-bold text-base-content transition-colors group-hover:text-primary"
							>
								{info.titre}
							</h3>

							<p class="text-sm leading-relaxed whitespace-pre-wrap text-base-content/70">
								{info.contenu}
							</p>

							<div class="mt-4 card-actions justify-end">
								<button class="btn gap-2 font-bold text-primary btn-ghost btn-sm">
									Lire la suite
									<ChevronRight size={14} />
								</button>
							</div>
						</div>
					</div>
				</div>
			{:else}
				<div class="card bg-base-100 border border-dashed border-base-300 py-16">
					<div class="card-body items-center text-center gap-4">
						<div
							class="w-16 h-16 rounded-full bg-base-200 flex items-center justify-center text-base-content/30"
						>
							<Info size={32} />
						</div>
						<div class="max-w-xs">
							<h3 class="font-bold text-lg text-base-content">Aucune annonce</h3>
							<p class="text-sm text-base-content/50 mt-1">
								Il n'y a pas d'informations essentielles à afficher pour le moment.
							</p>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
