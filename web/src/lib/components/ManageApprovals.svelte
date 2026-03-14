<script lang="ts">
	import { CheckCircle, XCircle, Loader2, FileText } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';

	let { open = $bindable(false) } = $props();

	let pendingDocs = $state<any[]>([]);
	let pendingInfos = $state<any[]>([]);
	let loading = $state(false);

	async function loadPending() {
		loading = true;
		try {
			// Dans une vraie app, on filtrerait côté serveur ?statut=en_attente
			const [resDocs, resInfos] = await Promise.all([
				api.get('/api/documents/'),
				api.get('/api/infos/')
			]);
			pendingDocs = resDocs.data.filter((d: any) => d.statut === 'en_attente');
			pendingInfos = resInfos.data.filter((i: any) => i.statut === 'en_attente');
		} catch (error) {
			console.error('Erreur chargement validations:', error);
		} finally {
			loading = false;
		}
	}

	async function approve(type: 'doc' | 'info', id: number) {
		try {
			const endpoint = type === 'doc' ? `/api/documents/${id}/` : `/api/infos/${id}/`;
			await api.patch(endpoint, { statut: 'approuve' });

			if (type === 'doc') {
				pendingDocs = pendingDocs.filter((d) => d.id !== id);
			} else {
				pendingInfos = pendingInfos.filter((i) => i.id !== id);
			}
		} catch (error) {
			console.error('Erreur approbation:', error);
			alert("Impossible d'approuver l'élément.");
		}
	}

	async function reject(type: 'doc' | 'info', id: number) {
		if (!confirm('Êtes-vous sûr de vouloir rejeter et supprimer cet élément ?')) return;

		try {
			const endpoint = type === 'doc' ? `/api/documents/${id}/` : `/api/infos/${id}/`;
			await api.delete(endpoint); // Le rejet équivaut à une suppression

			if (type === 'doc') {
				pendingDocs = pendingDocs.filter((d) => d.id !== id);
			} else {
				pendingInfos = pendingInfos.filter((i) => i.id !== id);
			}
		} catch (error) {
			console.error('Erreur rejet:', error);
			alert("Impossible de rejeter l'élément.");
		}
	}

	$effect(() => {
		if (open) {
			loadPending();
		}
	});

	function close() {
		open = false;
	}
</script>

<dialog class="modal" class:modal-open={open} aria-labelledby="approval-modal-title">
	<div class="modal-box max-w-3xl bg-base-100">
		<form method="dialog">
			<button class="btn absolute top-2 right-2 btn-circle btn-ghost btn-sm" onclick={close}
				>✕</button
			>
		</form>
		<h3 id="approval-modal-title" class="mb-6 flex items-center gap-2 text-lg font-bold">
			<CheckCircle size={20} class="text-secondary" />
			Validations en attente
		</h3>

		{#if loading}
			<div class="flex justify-center py-8">
				<Loader2 class="animate-spin text-primary" size={32} />
			</div>
		{:else if pendingDocs.length === 0 && pendingInfos.length === 0}
			<div class="py-10 text-center text-base-content/50">
				<FileText size={48} class="mx-auto mb-3 opacity-20" />
				<p>Aucun élément en attente de validation.</p>
			</div>
		{:else}
			{#if pendingDocs.length > 0}
				<div class="mb-6">
					<h4 class="mb-3 text-sm font-semibold text-base-content/70 uppercase">Documents</h4>
					<div class="overflow-x-auto">
						<table class="table w-full table-sm">
							<thead>
								<tr>
									<th>Titre</th>
									<th>Cours</th>
									<th>Date</th>
									<th class="text-right">Action</th>
								</tr>
							</thead>
							<tbody>
								{#each pendingDocs as doc}
									<tr class="hover">
										<td class="font-medium">{doc.titre}</td>
										<td>{doc.cours}</td>
										<td class="text-xs text-base-content/50"
											>{new Date(doc.date_upload).toLocaleDateString()}</td
										>
										<td class="flex justify-end gap-1 text-right">
											<button
												class="tooltip btn text-success-content btn-xs btn-success"
												data-tip="Approuver"
												onclick={() => approve('doc', doc.id)}
											>
												<CheckCircle size={14} />
											</button>
											<button
												class="tooltip btn text-error-content btn-xs btn-error"
												data-tip="Rejeter"
												onclick={() => reject('doc', doc.id)}
											>
												<XCircle size={14} />
											</button>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>
			{/if}

			{#if pendingInfos.length > 0}
				<div>
					<h4 class="mb-3 text-sm font-semibold text-base-content/70 uppercase">
						Informations Essentielles
					</h4>
					<div class="overflow-x-auto">
						<table class="table w-full table-sm">
							<thead>
								<tr>
									<th>Titre</th>
									<th>Catégorie</th>
									<th>Date</th>
									<th class="text-right">Action</th>
								</tr>
							</thead>
							<tbody>
								{#each pendingInfos as info}
									<tr class="hover">
										<td class="font-medium">{info.titre}</td>
										<td><span class="badge badge-sm">{info.categorie || '-'}</span></td>
										<td class="text-xs text-base-content/50"
											>{new Date(info.created_at).toLocaleDateString()}</td
										>
										<td class="flex justify-end gap-1 text-right">
											<button
												class="tooltip btn text-success-content btn-xs btn-success"
												data-tip="Approuver"
												onclick={() => approve('info', info.id)}
											>
												<CheckCircle size={14} />
											</button>
											<button
												class="tooltip btn text-error-content btn-xs btn-error"
												data-tip="Rejeter"
												onclick={() => reject('info', info.id)}
											>
												<XCircle size={14} />
											</button>
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>
			{/if}
		{/if}
	</div>
	<form method="dialog" class="modal-backdrop" onclick={close}>
		<button>close</button>
	</form>
</dialog>
