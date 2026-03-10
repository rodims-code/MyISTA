<script lang="ts">
	import { DoorOpen, Search, Loader2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { ACCESS_TOKEN } from '$lib/constants';
	import { fetchCurrentSalle, fetchCurrentBatiments } from '$lib/userApi';

	let salles = $state<any[]>([]);
	let batiments = $state<any[]>([]);
	let loading = $state(true);
	let search = $state('');

	onMount(async () => {
		try {
			const [sallesRes, batimentsRes] = await Promise.all([
				fetchCurrentSalle(),
				fetchCurrentBatiments()
			]);
			salles = sallesRes.data;
			batiments = batimentsRes.data;
		} catch (error) {
			console.error('Erreur lors du chargement des salles:', error);
		} finally {
			loading = false;
		}
	});

	function getBatimentNom(id: number) {
		return batiments.find((b) => b.id === id)?.nom || 'Inconnu';
	}

	const filtered = $derived(
		salles.filter(
			(s) =>
				s.nom.toLowerCase().includes(search.toLowerCase()) ||
				getBatimentNom(s.batiment).toLowerCase().includes(search.toLowerCase())
		)
	);
</script>

<svelte:head>
	<title>Salles — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-6">
	<div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
		<div>
			<h2 class="text-2xl font-bold text-base-content">Salles</h2>
			<p class="mt-1 text-sm text-base-content/50">Affectation et disponibilité des salles</p>
		</div>
		<label class="input-bordered input flex w-full items-center gap-2 sm:w-64">
			<Search size={15} class="text-base-content/40" />
			<input type="text" placeholder="Rechercher une salle…" class="grow" bind:value={search} />
		</label>
	</div>

	<div class="overflow-x-auto rounded-xl border border-base-200 shadow-sm">
		<table class="table bg-base-100">
			<thead class="bg-base-200 text-xs tracking-wide text-base-content/70 uppercase">
				<tr>
					<th>Salle</th>
					<th>Bâtiment</th>
					<th class="text-right">Actions</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					<tr>
						<td colspan="3" class="py-10 text-center">
							<Loader2 size={24} class="mx-auto animate-spin text-primary" />
						</td>
					</tr>
				{:else}
					{#each filtered as salle}
						<tr class="hover:bg-base-50 border-base-200">
							<td class="font-mono font-bold text-primary">{salle.nom}</td>
							<td>
								<span class="badge badge-ghost badge-sm">{getBatimentNom(salle.batiment)}</span>
							</td>
							<td class="text-right">
								<button class="btn btn-ghost btn-xs">Détails</button>
							</td>
						</tr>
					{:else}
						<tr>
							<td colspan="3" class="text-center py-10 text-base-content/40">
								<DoorOpen size={28} class="mx-auto mb-2 opacity-30" />
								Aucune salle trouvée
							</td>
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</div>
</div>
