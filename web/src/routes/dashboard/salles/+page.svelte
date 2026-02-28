<script lang="ts">
	import { DoorOpen, Search } from 'lucide-svelte';

	const salles = [
		{ id: 'A-101', type: 'Cours', capacite: 30, statut: 'Disponible', niveau: 1 },
		{ id: 'A-102', type: 'Cours', capacite: 30, statut: 'Occupée', niveau: 1 },
		{ id: 'B-201', type: 'TD', capacite: 20, statut: 'Disponible', niveau: 2 },
		{ id: 'B-204', type: 'TP', capacite: 15, statut: 'Occupée', niveau: 2 },
		{ id: 'C-301', type: 'Cours', capacite: 40, statut: 'Disponible', niveau: 3 },
		{ id: 'C-305', type: 'TD', capacite: 20, statut: 'Disponible', niveau: 3 }
	];

	let search = $state('');
	const filtered = $derived(
		salles.filter(
			(s) =>
				s.id.toLowerCase().includes(search.toLowerCase()) ||
				s.type.toLowerCase().includes(search.toLowerCase())
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
					<th>Type</th>
					<th>Capacité</th>
					<th>Niveau</th>
					<th>Statut</th>
				</tr>
			</thead>
			<tbody>
				{#each filtered as salle}
					<tr class="hover:bg-base-50 border-base-200">
						<td class="font-mono font-bold text-primary">{salle.id}</td>
						<td><span class="badge badge-ghost badge-sm">{salle.type}</span></td>
						<td>{salle.capacite} places</td>
						<td>Niveau {salle.niveau}</td>
						<td>
							{#if salle.statut === 'Disponible'}
								<span class="badge gap-1 badge-sm badge-success">
									<span class="h-1.5 w-1.5 rounded-full bg-current"></span>
									{salle.statut}
								</span>
							{:else}
								<span class="badge gap-1 badge-sm badge-error">
									<span class="h-1.5 w-1.5 rounded-full bg-current"></span>
									{salle.statut}
								</span>
							{/if}
						</td>
					</tr>
				{:else}
					<tr>
						<td colspan="5" class="text-center py-10 text-base-content/40">
							<DoorOpen size={28} class="mx-auto mb-2 opacity-30" />
							Aucune salle trouvée
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
