<script lang="ts">
	import { FilePlus, Upload, Loader2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';

	let { open = $bindable(false) } = $props();

	let loading = $state(false);
	let errorMsg = $state('');
	let successMsg = $state('');

	let newDoc = $state({
		titre: '',
		cours: '',
		filiere: '',
		niveau: '',
	});

	let filiere = $state<any[]>([]);
	let niveau = $state<any[]>([]);
	let fileInput = $state<HTMLInputElement | null>(null);

	async function loadFormOptions() {
		try {
			// Dans un cas réel, ces données viendraient de /api/filieres/ et /api/niveaux/ ou seraient injectées.
			// On hardcode ici pour la démo si les endpoints manquent (ou on fetch).
			const fRes = await api.get('/api/batiments/'); // TODO: utiliser de vraies routes si exposées
			// On masque avec de fausses options ou on attend que vous ayez exposé ces listes.
		} catch (e) {}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		errorMsg = '';
		successMsg = '';

		if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
			errorMsg = 'Veuillez sélectionner un fichier.';
			loading = false;
			return;
		}

		const formData = new FormData();
		formData.append('titre', newDoc.titre);
		formData.append('cours', newDoc.cours);
		// FIXME: il faudrait ajouter filiere_id et niveau_id
		formData.append('filiere', newDoc.filiere);
		formData.append('niveau', newDoc.niveau);
		formData.append('fichier', fileInput.files[0]);

		try {
			// Note: l'API gère le statut automatiquement selon le rôle
			await api.post('/api/documents/', formData, {
				headers: { 'Content-Type': 'multipart/form-data' }
			});
			successMsg = 'Document ajouté avec succès !';
			setTimeout(() => {
				close();
				successMsg = '';
			}, 2000);
		} catch (error) {
			console.error(error);
			errorMsg = "Erreur lors de l'ajout du document.";
		} finally {
			loading = false;
		}
	}

	$effect(() => {
		if (open) {
			// loadFormOptions();
		}
	});

	function close() {
		open = false;
	}
</script>

<dialog class="modal" class:modal-open={open} aria-labelledby="add-doc-modal-title">
	<div class="modal-box bg-base-100">
		<form method="dialog">
			<button
				class="btn absolute top-2 right-2 btn-circle btn-ghost btn-sm"
				onclick={close}
				type="button">❌</button
			>
		</form>
		<h3 id="add-doc-modal-title" class="mb-6 flex items-center gap-2 text-lg font-bold">
			<FilePlus size={20} class="text-primary" />
			Ajouter un Document
		</h3>

		{#if successMsg}
			<div class="mt-2 mb-4 alert py-2 text-sm alert-success">{successMsg}</div>
		{/if}
		{#if errorMsg}
			<div class="mt-2 mb-4 alert py-2 text-sm alert-error">{errorMsg}</div>
		{/if}

		<form onsubmit={handleSubmit} class="flex flex-col gap-4">
			<div class="form-control grid">
				<label class="label"><span class="label-text">Titre du document</span></label>
				<input type="text" class="input-bordered input w-full" bind:value={newDoc.titre} required />
			</div>

			<div class="form-control grid">
				<label class="label"><span class="label-text">Matière / Cours</span></label>
				<input type="text" class="input-bordered input w-full" bind:value={newDoc.cours} required />
			</div>

			<div class="grid grid-cols-2 gap-4">
				<div class="form-control">
					<label class="label"><span class="label-text">Filière</span></label>
					<select class="select-bordered select w-full" bind:value={newDoc.filiere} required>
						<option value="" disabled selected>Choisir la filliere</option>
						<option value="G">G</option>
					</select>
				</div>
				<div class="form-control">
					<label class="label"><span class="label-text">Niveau</span></label>
					<select class="select-bordered select w-full" bind:value={newDoc.niveau} required>
						<option value="" disabled selected>Choisir le niveau</option>
						<option value="PREPO">PREPO</option>
					</select>
				</div>
			</div>

			<div class="form-control">
				<label class="label"><span class="label-text">Fichier (PDF, DOCX...)</span></label>
				<input
					type="file"
					class="file-input-bordered file-input w-full"
					bind:this={fileInput}
					required
				/>
			</div>

			<div class="modal-action">
				<button type="button" class="btn btn-ghost" onclick={close} disabled={loading}
					>Annuler</button
				>
				<button type="submit" class="btn gap-2 btn-primary" disabled={loading}>
					{#if loading}
						<Loader2 class="animate-spin" size={16} />
						Envoi...
					{:else}
						<Upload size={16} />
						Ajouter
					{/if}
				</button>
			</div>
		</form>
	</div>
	<form method="dialog" class="modal-backdrop" onclick={close}>
		<button type="button">close</button>
	</form>
</dialog>
