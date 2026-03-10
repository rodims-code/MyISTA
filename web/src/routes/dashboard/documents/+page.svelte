<script lang="ts">
	import { FileText, Download, Search, Loader2, Upload } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { PUBLIC_API_URL } from '$env/static/public';

	let documents = $state<any[]>([]);
	let loading = $state(true);
	let search = $state('');

	onMount(async () => {
		try {
			const res = await api.get('/api/documents/');
			documents = res.data;
		} catch (error) {
			console.error('Erreur chargement documents:', error);
		} finally {
			loading = false;
		}
	});

	const filtered = $derived(
		documents.filter(
			(d) =>
				d.titre.toLowerCase().includes(search.toLowerCase()) ||
				d.cours.toLowerCase().includes(search.toLowerCase())
		)
	);

	function formatBytes(bytes: number, decimals = 2) {
		if (bytes === 0) return '0 Bytes';
		const k = 1024;
		const dm = decimals < 0 ? 0 : decimals;
		const sizes = ['Bytes', 'Ko', 'Mo', 'Go'];
		const i = Math.floor(Math.log(bytes) / Math.log(k));
		return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
	}

	function getDownloadUrl(path: string) {
		if (path.startsWith('http')) return path;
		return `${PUBLIC_API_URL.replace(/\/$/, '')}${path}`;
	}
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
		<div class="flex items-center gap-2">
			<label class="input-bordered input flex w-full items-center gap-2 sm:w-64">
				<Search size={15} class="text-base-content/40" />
				<input type="text" placeholder="Rechercher…" class="grow" bind:value={search} />
			</label>
			<button class="btn gap-2 btn-sm btn-primary">
				<Upload size={16} />
				<span class="hidden sm:inline">Ajouter</span>
			</button>
		</div>
	</div>

	{#if loading}
		<div class="flex justify-center py-20">
			<Loader2 size={48} class="animate-spin text-primary/30" />
		</div>
	{:else}
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
							<p class="truncate text-sm font-semibold text-base-content">{doc.titre}</p>
							<div class="mt-1 flex items-center gap-2">
								<span class="badge badge-ghost badge-xs">{doc.cours}</span>
								<span class="text-xs text-base-content/40">
									{new Date(doc.date_upload).toLocaleDateString()}
								</span>
							</div>
						</div>
						<a
							href={getDownloadUrl(doc.fichier)}
							target="_blank"
							class="btn btn-square text-base-content/40 btn-ghost btn-sm hover:text-primary"
							title="Télécharger"
						>
							<Download size={16} />
						</a>
					</div>
				</div>
			{:else}
				<div class="md:col-span-2 flex flex-col items-center py-16 gap-3 text-base-content/40">
					<FileText size={36} class="opacity-30" />
					<p class="text-sm">Aucun document trouvé</p>
				</div>
			{/each}
		</div>
	{/if}
</div>
