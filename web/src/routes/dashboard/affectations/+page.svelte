<script lang="ts">
	import { CalendarCheck, DoorOpen, Layers, Briefcase, Search, Loader2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';

	let affectations = $state<any[]>([]);
	let salles = $state<any[]>([]);
	let loading = $state(true);
	let search = $state('');

	// Static mappings for Filiere/Niveau since no GET endpoints exist
	const filiereMap: Record<number, string> = {
		1: 'TSDI (Digital)',
		2: 'TCE (Commerce)',
		3: 'GE (Gestion)'
	};
	const niveauMap: Record<number, string> = {
		1: '1ère Année',
		2: '2ème Année'
	};

	onMount(async () => {
		try {
			const [affRes, sallesRes] = await Promise.all([
				api.get('/api/affectations/'),
				api.get('/api/salles/')
			]);
			affectations = affRes.data;
			salles = sallesRes.data;
		} catch (error) {
			console.error('Erreur chargement affectations:', error);
		} finally {
			loading = false;
		}
	});

	function getSalleNom(id: number) {
		return salles.find((s) => s.id === id)?.nom || `Salle #${id}`;
	}

	const filtered = $derived(
		affectations.filter((a) => {
			const salleNom = getSalleNom(a.salle).toLowerCase();
			const filiereNom = (filiereMap[a.filiere] || '').toLowerCase();
			const query = search.toLowerCase();
			return salleNom.includes(query) || filiereNom.includes(query);
		})
	);
</script>

<svelte:head>
	<title>Affectation des Salles — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-6">
	<div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
		<div>
			<h2 class="text-2xl font-bold text-base-content">Affectation des Salles</h2>
			<p class="mt-1 text-sm text-base-content/50">
				Planification des salles par filière et niveau
			</p>
		</div>
		<label class="input-bordered input flex w-full items-center gap-2 sm:w-64">
			<Search size={15} class="text-base-content/40" />
			<input
				type="text"
				placeholder="Rechercher une affectation…"
				class="grow"
				bind:value={search}
			/>
		</label>
	</div>

	<div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
		{#if loading}
			{#each Array(6) as _}
				<div class="card animate-pulse border border-base-200 bg-base-100">
					<div class="card-body h-32 p-6"></div>
				</div>
			{/each}
		{:else}
			{#each filtered as aff}
				<div
					class="group card border border-base-200 bg-base-100 shadow-sm transition-all hover:shadow-md"
				>
					<div class="card-body flex-row items-center gap-4 p-6">
						<div
							class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-content"
						>
							<DoorOpen size={24} />
						</div>

						<div class="min-w-0 flex-1">
							<h3 class="font-mono text-lg font-bold text-base-content">
								{getSalleNom(aff.salle)}
							</h3>
							<div class="mt-1 flex flex-col gap-1">
								<div class="flex items-center gap-2 text-xs text-base-content/60">
									<Briefcase size={12} />
									<span class="truncate"
										>{filiereMap[aff.filiere] || `Filière #${aff.filiere}`}</span
									>
								</div>
								<div class="flex items-center gap-2 text-xs text-base-content/60">
									<Layers size={12} />
									<span>{niveauMap[aff.niveau] || `Niveau #${aff.niveau}`}</span>
								</div>
							</div>
						</div>

						<div class="badge badge-outline badge-sm">Actif</div>
					</div>
				</div>
			{:else}
				<div class="col-span-full card bg-base-200/50 border border-dashed border-base-300 py-20">
					<div class="card-body items-center text-center gap-4">
						<CalendarCheck size={48} class="text-base-content/20" />
						<p class="text-base-content/40 font-medium">Aucune affectation trouvée</p>
					</div>
				</div>
			{/each}
		{/if}
	</div>
</div>
