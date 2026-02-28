<script lang="ts">
	import { FileText, Download, Search } from 'lucide-svelte';

	const documents = [
		{ nom: 'Programme Semestriel S4', filiere: 'TSDI', date: '2026-02-20', taille: '820 Ko' },
		{ nom: 'Planning TP Informatique', filiere: 'TSDI', date: '2026-02-18', taille: '340 Ko' },
		{ nom: 'Liste des Modules S3', filiere: 'TCE', date: '2026-02-15', taille: '210 Ko' },
		{ nom: 'Règlement Intérieur ISTA', filiere: 'Tous', date: '2026-01-10', taille: '1.2 Mo' },
		{ nom: 'Calendrier des Examens 2026', filiere: 'Tous', date: '2026-01-05', taille: '512 Ko' }
	];

	let search = $state('');
	const filtered = $derived(
		documents.filter(
			(d) =>
				d.nom.toLowerCase().includes(search.toLowerCase()) ||
				d.filiere.toLowerCase().includes(search.toLowerCase())
		)
	);
</script>

<svelte:head>
	<title>Documents — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-6">
	<div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
		<div>
			<h2 class="text-2xl font-bold text-base-content">Documents</h2>
			<p class="mt-1 text-sm text-base-content/50">
				Ressources et documents académiques centralisés
			</p>
		</div>
		<label class="input-bordered input flex w-full items-center gap-2 sm:w-64">
			<Search size={15} class="text-base-content/40" />
			<input type="text" placeholder="Rechercher…" class="grow" bind:value={search} />
		</label>
	</div>

	<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
		{#each filtered as doc}
			<div
				class="card border border-base-200 bg-base-100 shadow-sm transition-shadow hover:shadow-md"
			>
				<div class="card-body flex-row items-center gap-4 p-5">
					<div
						class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary"
					>
						<FileText size={22} />
					</div>
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-semibold text-base-content">{doc.nom}</p>
						<div class="mt-1 flex items-center gap-2">
							<span class="badge badge-ghost badge-xs">{doc.filiere}</span>
							<span class="text-xs text-base-content/40">{doc.date} · {doc.taille}</span>
						</div>
					</div>
					<button
						class="btn btn-square text-base-content/40 btn-ghost btn-sm hover:text-primary"
						title="Télécharger"
					>
						<Download size={16} />
					</button>
				</div>
			</div>
		{:else}
			<div class="md:col-span-2 flex flex-col items-center py-16 gap-3 text-base-content/40">
				<FileText size={36} class="opacity-30" />
				<p class="text-sm">Aucun document trouvé</p>
			</div>
		{/each}
	</div>
</div>
