<script lang="ts">
	import { FileText, Upload, Loader2 } from 'lucide-svelte';
	import api from '$lib/index';

	let { open = $bindable(false) } = $props();

	let loading = $state(false);
	let errorMsg = $state('');
	let successMsg = $state('');

	let newInfo = $state({
		titre: '',
		contenu: '',
		categorie: ''
	});

	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		errorMsg = '';
		successMsg = '';

		try {
			await api.post('/api/infos/', newInfo);
			successMsg = 'Information ajoutée avec succès !';
			setTimeout(() => {
				close();
				successMsg = '';
				newInfo = { titre: '', contenu: '', categorie: '' };
			}, 2000);
		} catch (error) {
			console.error("Erreur d'ajout information:", error);
			errorMsg = "Erreur lors de l'ajout de l'information.";
		} finally {
			loading = false;
		}
	}

	function close() {
		open = false;
	}
</script>

<dialog class="modal" class:modal-open={open} aria-labelledby="add-info-modal-title">
	<div class="modal-box bg-base-100">
		<form method="dialog">
			<button
				class="btn absolute top-2 right-2 btn-circle btn-ghost btn-sm"
				onclick={close}
				type="button">❌</button
			>
		</form>
		<h3 id="add-info-modal-title" class="mb-6 flex items-center gap-2 text-lg font-bold">
			<FileText size={20} class="text-accent" />
			Diffuser une information
		</h3>

		{#if successMsg}
			<div class="mt-2 mb-4 alert py-2 text-sm alert-success">{successMsg}</div>
		{/if}
		{#if errorMsg}
			<div class="mt-2 mb-4 alert py-2 text-sm alert-error">{errorMsg}</div>
		{/if}

		<form onsubmit={handleSubmit} class="flex flex-col gap-4">
			<div class="form-control grid">
				<label class="label"><span class="label-text">Titre de l'Avis</span></label>
				<input
					type="text"
					class="input-bordered input w-full"
					bind:value={newInfo.titre}
					required
					placeholder="Ex: Rattrapage d'algorithmique"
				/>
			</div>

			<div class="form-control grid">
				<label class="label"><span class="label-text">Catégorie</span></label>
				<select class="select-bordered select w-full" bind:value={newInfo.categorie} required>
					<option value="" disabled selected>Choisir une catégorie</option>
					<option value="Urgent">Urgent</option>
					<option value="Examen">Examen</option>
					<option value="Scolarité">Scolarité</option>
					<option value="Autre">Autre</option>
				</select>
			</div>

			<div class="form-control grid">
				<label class="label"><span class="label-text">Contenu / Message</span></label>
				<textarea
					class="textarea-bordered textarea h-50 w-full"
					bind:value={newInfo.contenu}
					required
					placeholder="Détails de l'information..."
				></textarea>
			</div>

			<div class="modal-action">
				<button type="button" class="btn btn-ghost" onclick={close} disabled={loading}
					>Annuler</button
				>
				<button type="submit" class="btn gap-2 btn-accent" disabled={loading}>
					{#if loading}
						<Loader2 class="animate-spin" size={16} />
						Envoi...
					{:else}
						<Upload size={16} />
						Publier
					{/if}
				</button>
			</div>
		</form>
	</div>
	<form method="dialog" class="modal-backdrop" onclick={close}>
		<button type="button">close</button>
	</form>
</dialog>
