<script lang="ts">
	import { FileText, Download, Search, Loader2, Upload, Eye, Star } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { fetchCurrentUser } from '$lib/userApi';
	import AddDocument from '$lib/components/AddDocument.svelte';

	let documents = $state<any[]>([]);
	let loading = $state(true);
	let search = $state('');
	let currentUser = $state<any>(null);
	let showAddDocModal = $state(false);

	let previewDoc = $state<any>(null);
	let previewUrl = $state('');
	let showPreviewModal = $state(false);

	onMount(async () => {
		try {
			currentUser = await fetchCurrentUser();
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

	const favorisDocuments = $derived(
		currentUser?.favoris ? filtered.filter((d) => currentUser.favoris.includes(d.id)) : []
	);

	const autresDocuments = $derived(
		currentUser?.favoris ? filtered.filter((d) => !currentUser.favoris.includes(d.id)) : filtered
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

	async function handleDownload(doc: any) {
		const url = getDownloadUrl(doc.fichier);
		const cleanUrl = url.split('?')[0].split('#')[0];
		const filename = cleanUrl.split('/').pop() || doc.titre || 'document';

		try {
			const response = await fetch(url);
			if (!response.ok) throw new Error('Erreur réseau');
			const blob = await response.blob();
			const blobUrl = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = blobUrl;
			a.download = filename;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			window.URL.revokeObjectURL(blobUrl);
		} catch (error) {
			console.error('Erreur de téléchargement:', error);
			window.open(url, '_blank'); // Fallback: ouvrir dans un nouvel onglet
		}
	}

	function openPreview(doc: any) {
		previewDoc = doc;
		previewUrl = getDownloadUrl(doc.fichier);
		showPreviewModal = true;
	}

	function isImage(path: string) {
		const cleanPath = path.split('?')[0].split('#')[0];
		return cleanPath.match(/\.(jpeg|jpg|gif|png|webp|svg)$/i) != null;
	}

	function isPdf(path: string) {
		const cleanPath = path.split('?')[0].split('#')[0];
		return cleanPath.match(/\.(pdf)$/i) != null;
	}

	function isOfficeDoc(path: string) {
		const cleanPath = path.split('?')[0].split('#')[0];
		return cleanPath.match(/\.(doc|docx|ppt|pptx|xls|xlsx)$/i) != null;
	}

	async function toggleFavorite(doc: any) {
		try {
			const res = await api.post(`/api/documents/${doc.id}/toggle_favorite/`);
			if (res.data.status === 'added') {
				currentUser.favoris = [...(currentUser.favoris || []), doc.id];
			} else {
				currentUser.favoris = (currentUser.favoris || []).filter((id: number) => id !== doc.id);
			}
		} catch (error) {
			console.error('Erreur toggle favori:', error);
		}
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
			{#if currentUser && currentUser.role !== 'student'}
				<button class="btn gap-2 btn-sm btn-primary" onclick={() => (showAddDocModal = true)}>
					<Upload size={16} />
					<span class="hidden sm:inline">Ajouter</span>
				</button>
			{/if}
		</div>
	</div>

	{#if loading}
		<div class="flex justify-center py-20">
			<Loader2 size={48} class="animate-spin text-primary/30" />
		</div>
	{:else}
		{#snippet documentCard(doc)}
			<div class="card border border-base-200 bg-base-100 shadow-sm transition-shadow hover:shadow-md">
				<div class="card-body flex-row items-center gap-4 p-5">
					<div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
						<FileText size={22} />
					</div>
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-semibold text-base-content">{doc.titre}</p>
						<div class="mt-1 flex flex-wrap items-center gap-2">
							<span class="badge badge-ghost badge-xs">{doc.cours}</span>
							<span class="text-xs text-base-content/40">
								{new Date(doc.date_upload).toLocaleDateString()}
							</span>
							{#if currentUser && currentUser.role !== 'student'}
								<span class="badge badge-xs {doc.statut === 'approuve' ? 'badge-success badge-outline' : 'badge-warning badge-outline'}">
									{doc.statut === 'approuve' ? 'Approuvé' : 'En attente'}
								</span>
							{/if}
						</div>
					</div>
					
					<div class="flex gap-2 shrink-0">
						{#if currentUser}
							<button
								onclick={() => toggleFavorite(doc)}
								class="btn btn-square btn-ghost btn-sm {currentUser.favoris?.includes(doc.id) ? 'text-warning hover:text-warning/80' : 'text-base-content/40 hover:text-warning'}"
								title={currentUser.favoris?.includes(doc.id) ? "Retirer des favoris" : "Ajouter aux favoris"}
							>
								<Star size={18} fill={currentUser.favoris?.includes(doc.id) ? "currentColor" : "none"} />
							</button>
						{/if}
						<button
							onclick={() => openPreview(doc)}
							class="btn btn-square text-base-content/40 btn-ghost btn-sm hover:text-info"
							title="Prévisualiser"
						>
							<Eye size={18} />
						</button>
						<button
							onclick={() => handleDownload(doc)}
							class="btn btn-square text-base-content/40 btn-ghost btn-sm hover:text-primary"
							title="Télécharger"
						>
							<Download size={18} />
						</button>
					</div>
				</div>
			</div>
		{/snippet}

		{#if favorisDocuments.length > 0}
			<div class="mb-4">
				<h3 class="text-lg font-bold flex items-center gap-2 mb-4 text-warning">
					<Star size={20} class="fill-current" />
					Vos Favoris
				</h3>
				<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
					{#each favorisDocuments as doc}
						{@render documentCard(doc)}
					{/each}
				</div>
			</div>
			
			<div class="divider mb-4">Autres documents</div>
		{/if}

		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			{#each autresDocuments as doc}
				{@render documentCard(doc)}
			{:else}
				<div class="md:col-span-2 flex flex-col items-center py-16 gap-3 text-base-content/40">
					<FileText size={36} class="opacity-30" />
					<p class="text-sm">Aucun document trouvé</p>
				</div>
			{/each}
		</div>
	{/if}
</div>

<AddDocument bind:open={showAddDocModal} />

<!-- Modal de prévisualisation -->
{#if showPreviewModal && previewDoc}
	<div class="modal modal-open">
		<div class="modal-box w-11/12 max-w-5xl h-[90vh] flex flex-col p-4 bg-base-100">
			<div class="flex justify-between items-center mb-4">
				<h3 class="font-bold text-lg truncate pr-4">{previewDoc.titre}</h3>
				<form method="dialog">
					<button class="btn btn-sm btn-circle btn-ghost" onclick={() => showPreviewModal = false}>❌</button>
				</form>
			</div>
			
			<div class="flex-1 bg-base-200 rounded-lg overflow-hidden flex items-center justify-center relative">
				{#if isImage(previewUrl)}
					<img src={previewUrl} alt={previewDoc.titre} class="max-w-full max-h-full object-contain" />
				{:else if isPdf(previewUrl)}
					<iframe src={previewUrl} title={previewDoc.titre} class="w-full h-full border-0"></iframe>
				{:else if isOfficeDoc(previewUrl)}
					<iframe src="https://view.officeapps.live.com/op/embed.aspx?src={encodeURIComponent(previewUrl)}" title={previewDoc.titre} class="w-full h-full border-0"></iframe>
				{:else}
					<div class="flex flex-col items-center gap-4 text-base-content/50 p-8 text-center">
						<FileText size={48} />
						<p>Ce type de fichier ne peut pas être prévisualisé directement.</p>
						<p class="text-sm">Veuillez télécharger le fichier pour le consulter.</p>
					</div>
				{/if}
			</div>

			<div class="modal-action mt-4 flex justify-between w-full">
				<button class="btn" onclick={() => showPreviewModal = false}>Fermer</button>
				<button class="btn btn-primary" onclick={() => handleDownload(previewDoc)}>
					<Download size={18} class="mr-2" />
					Télécharger
				</button>
			</div>
		</div>
		<div class="modal-backdrop" onclick={() => showPreviewModal = false}>
			<button class="cursor-default">close</button>
		</div>
	</div>
{/if}
