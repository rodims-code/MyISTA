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
		categorie: '',
		filiere: '',
		niveau: ''
	});

	let currentUser = $state<any>(null);

	import { onMount } from 'svelte';
	import { fetchCurrentUser } from '$lib/userApi';

	onMount(async () => {
		currentUser = await fetchCurrentUser();
	});

	let filieresPrepo = $state([{ nom: 'A' }, { nom: 'B' }, { nom: 'C' }, { nom: 'D' }, { nom: 'E' }, { nom: 'F' }, { nom: 'G' }, { nom: 'H' }, { nom: 'I' }, { nom: 'J' }]);
	let filieresLicence = $state([{ nom: 'Environnement' }, { nom: 'Météorologie' }, { nom: 'Systèmes de Navigation aérienne' }, { nom: 'Exploitation aéronautique' }, { nom: 'Electricité' }, { nom: 'Energies renouvelables' }, { nom: 'Ingénierie Biomédicale' }, { nom: 'Biotechnologie' }, { nom: 'Electronique' }, { nom: 'Télécommunications' }, { nom: 'Mécanique' }, { nom: 'Informatique' }, { nom: 'Maintenance industrielle' }]);
	let niveaux = $state([{ nom: 'PREPO' }, { nom: 'LICENCE 1' }, { nom: 'LICENCE 2' }, { nom: 'LICENCE 3' }]);

	let availableFilieres = $derived(() => {
		if (currentUser && currentUser.role === 'delegate' && currentUser.filiere) return [{ nom: currentUser.filiere }];
		if (!newInfo.niveau) return [];
		if (newInfo.niveau === 'PREPO') return filieresPrepo;
		else if (['LICENCE 1', 'LICENCE 2', 'LICENCE 3'].includes(newInfo.niveau)) return filieresLicence;
		return [];
	});

	$effect(() => {
		if (open && currentUser && currentUser.role === 'delegate') {
			newInfo.niveau = currentUser.niveau;
			newInfo.filiere = currentUser.filiere;
		}
	});

	$effect(() => {
		if (newInfo.niveau && newInfo.filiere && (!currentUser || currentUser.role !== 'delegate')) {
			const validFilieres = availableFilieres.map((f: any) => f.nom);
			if (!validFilieres.includes(newInfo.filiere)) {
				newInfo.filiere = '';
			}
		}
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
				newInfo = { titre: '', contenu: '', categorie: '', filiere: '', niveau: '' };
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

			<div class="grid grid-cols-2 gap-4">
				<div class="form-control">
					<label class="label"><span class="label-text">Filière</span></label>
					<select class="select-bordered select w-full" bind:value={newInfo.filiere} disabled={currentUser?.role === 'delegate'}>
						<option value="">
							{currentUser?.role === 'admin' ? "Visible à tous (Aucune filière)" : "Choisir la filière"}
						</option>
						{#each availableFilieres as f}
							<option value={f.nom}>{f.nom}</option>
						{/each}
					</select>
				</div>
				<div class="form-control">
					<label class="label"><span class="label-text">Niveau</span></label>
					<select class="select-bordered select w-full" bind:value={newInfo.niveau} disabled={currentUser?.role === 'delegate'}>
						<option value="">
							{currentUser?.role === 'admin' ? "Visible à tous (Aucun niveau)" : "Choisir le niveau"}
						</option>
						{#each niveaux as n}
							<option value={n.nom}>{n.nom}</option>
						{/each}
					</select>
				</div>
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
