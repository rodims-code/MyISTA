<script lang="ts">
	import { Info, Calendar, Tag, ChevronRight, Loader2, Filter, AlertTriangle, Pin } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { fetchCurrentUser } from '$lib/userApi';

	let infos = $state<any[]>([]);
	let loading = $state(true);
	let currentUser = $state<any>(null);
	let selectedInfo = $state<any>(null);
	let modalElement = $state<HTMLDialogElement | null>(null);
	
	let showEditModal = $state(false);
	let editingInfoId = $state<number | null>(null);
	let newInfo = $state({ titre: '', contenu: '', categorie: '', filiere: '', niveau: '' });

	let filieresPrepo = $state([{ nom: 'A' }, { nom: 'B' }, { nom: 'C' }, { nom: 'D' }, { nom: 'E' }, { nom: 'F' }, { nom: 'G' }, { nom: 'H' }, { nom: 'I' }, { nom: 'J' }]);
	let filieresLicence = $state([{ nom: 'Environnement' }, { nom: 'Météorologie' }, { nom: 'Systèmes de Navigation aérienne' }, { nom: 'Exploitation aéronautique' }, { nom: 'Electricité' }, { nom: 'Energies renouvelables' }, { nom: 'Ingénierie Biomédicale' }, { nom: 'Biotechnologie' }, { nom: 'Electronique' }, { nom: 'Télécommunications' }, { nom: 'Mécanique' }, { nom: 'Informatique' }, { nom: 'Maintenance industrielle' }]);
	let niveaux = $state([{ nom: 'PREPO' }, { nom: 'LICENCE 1' }, { nom: 'LICENCE 2' }, { nom: 'LICENCE 3' }]);

	let availableFilieres = $derived.by(() => {
		if (currentUser && currentUser.role === 'delegate' && currentUser.filiere) {
			return [{ nom: currentUser.filiere }];
		}
		if (!newInfo.niveau) return [];
		if (newInfo.niveau === 'PREPO') return filieresPrepo;
		if (['LICENCE 1', 'LICENCE 2', 'LICENCE 3'].includes(newInfo.niveau)) return filieresLicence;
		return [];
	});

	$effect(() => {
		if (showEditModal && (!editingInfoId) && currentUser && currentUser.role === 'delegate') {
			newInfo.niveau = currentUser.niveau;
			newInfo.filiere = currentUser.filiere;
		}
	});

	$effect(() => {
		newInfo.niveau;
		if (!currentUser || currentUser.role !== 'delegate') {
			if (newInfo.filiere) {
				const validFilieres = availableFilieres.map((f: any) => f.nom);
				if (!validFilieres.includes(newInfo.filiere)) {
					newInfo.filiere = '';
				}
			} else {
				newInfo.filiere = '';
			}
		}
	});

	let activeFilter = $state('Toutes');
	let availableFilters = $derived(['Toutes', ...Array.from(new Set(infos.map(i => i.categorie?.trim()).filter(Boolean)))]);
	
	let displayedInfos = $derived(
		[...infos]
			.filter(i => {
				if (activeFilter === 'Toutes') return true;
				const cat = i.categorie?.trim() || '';
				return cat === activeFilter;
			})
			.sort((a, b) => {
				const aUrgent = (a.categorie || '').toLowerCase().includes('urgent');
				const bUrgent = (b.categorie || '').toLowerCase().includes('urgent');
				
				if (activeFilter === 'Toutes') {
					if (aUrgent && !bUrgent) return -1;
					if (!aUrgent && bUrgent) return 1;
				}
				const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
				const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
				return dateB - dateA;
			})
	);

	function openModal(info: any) {
		selectedInfo = info;
		modalElement?.showModal();
	}

	onMount(async () => {
		try {
			currentUser = await fetchCurrentUser();
			const res = await api.get('/api/infos/');
			infos = res.data;
		} catch (error) {
			console.error('Erreur chargement infos:', error);
		} finally {
			loading = false;
		}
	});

	async function saveInfo() {
		try {
			if (editingInfoId) {
				const res = await api.put(`/api/infos/${editingInfoId}/`, newInfo);
				infos = infos.map((i) => (i.id === editingInfoId ? res.data : i));
			} else {
				const res = await api.post('/api/infos/', newInfo);
				infos = [res.data, ...infos];
			}
			showEditModal = false;
			editingInfoId = null;
		} catch (error) {
			console.error('Save info error:', error);
			alert('Erreur lors de la sauvegarde. Assurez-vous que tous les champs requis sont remplis.');
		}
	}

	async function deleteInfo() {
		if (!selectedInfo || !confirm('Voulez-vous vraiment supprimer cette information ?')) return;
		try {
			await api.delete(`/api/infos/${selectedInfo.id}/`);
			infos = infos.filter((i) => i.id !== selectedInfo.id);
			modalElement?.close();
			selectedInfo = null;
		} catch (error) {
			console.error('Delete info error:', error);
			alert('Erreur lors de la suppression');
		}
	}

	function editInfo() {
		if (!selectedInfo) return;
		newInfo = {
			titre: selectedInfo.titre,
			contenu: selectedInfo.contenu,
			categorie: selectedInfo.categorie || '',
			filiere: selectedInfo.filiere || '',
			niveau: selectedInfo.niveau || ''
		};
		editingInfoId = selectedInfo.id;
		modalElement?.close();
		showEditModal = true;
	}
</script>

<svelte:head>
	<title>Infos Essentielles — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-8">
	<!-- Header -->
	<div class="flex flex-col sm:flex-row justify-between gap-4 items-start sm:items-center">
		<div>
			<h2 class="text-2xl font-bold text-base-content">Infos Essentielles</h2>
			<p class="mt-1 text-sm text-base-content/50">
				Dernières nouvelles et annonces importantes de l'ISTA
			</p>
		</div>
		{#if currentUser?.role === 'admin' || currentUser?.role === 'delegate'}
		<button 
			class="btn btn-primary shadow shadow-primary/30"
			onclick={() => {
				newInfo = { titre: '', contenu: '', categorie: '', filiere: '', niveau: '' };
				editingInfoId = null;
				showEditModal = true;
			}}
		>
			Ajouter une info
		</button>
		{/if}
	</div>

	<!-- Filters -->
	{#if !loading && infos.length > 0}
		<div class="flex flex-wrap items-center gap-2 py-1">
			<div class="flex items-center gap-2 mr-2 text-sm font-medium text-base-content/60">
				<Filter size={16} />
				Filtres:
			</div>
			{#each availableFilters as filter}
				<button
					class="btn btn-sm rounded-full transition-all {activeFilter === filter 
						? (filter.toLowerCase().includes('urgent') ? 'btn-warning border-warning text-warning-content' : 'btn-primary border-primary text-primary-content') 
						: 'btn-ghost bg-base-200 hover:bg-base-300'}"
					onclick={() => activeFilter = filter}
				>
					{#if filter.toLowerCase().includes('urgent')}
						<AlertTriangle size={14} class={activeFilter === filter ? '' : 'text-warning'} />
					{/if}
					{filter}
				</button>
			{/each}
		</div>
	{/if}

	{#if loading}
		<div class="flex flex-col items-center justify-center gap-4 py-20">
			<Loader2 size={40} class="animate-spin text-primary/40" />
			<p class="font-medium text-base-content/40">Chargement des annonces...</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-6">
			{#each displayedInfos as info}
				{@const isUrgent = info.categorie && info.categorie.toLowerCase().includes('urgent')}
				<div
					class="group card overflow-hidden border {isUrgent ? 'border-warning bg-warning/5' : 'border-base-200 bg-base-100'} shadow-sm transition-all hover:shadow-md"
				>
					<div class="flex flex-col md:flex-row">
						<!-- Left accent color bar based on category or default -->
						<div class="h-2 w-full {isUrgent ? 'bg-warning' : 'bg-primary'} md:h-auto md:w-2"></div>

						<div class="card-body flex-1 p-6">
							<div class="mb-4 flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
								<div class="flex items-center gap-2">
									{#if info.categorie}
										<div class="badge gap-1 badge-outline px-3 py-3 {isUrgent ? 'badge-warning' : 'badge-primary'}">
											<Tag size={12} />
											{info.categorie}
										</div>
									{/if}
									<span class="flex items-center gap-1 text-xs font-medium text-base-content/40">
										<Calendar size={12} />
										{new Date(info.created_at).toLocaleDateString()}
									</span>
									{#if currentUser && currentUser.role !== 'student'}
										<span class="badge badge-sm {info.statut === 'approuve' ? 'badge-success badge-outline' : 'badge-warning badge-outline'}">
											{info.statut === 'approuve' ? 'Approuvé' : 'En attente'}
										</span>
									{/if}
								</div>
							</div>

							<h3
								class="mb-3 text-xl font-bold text-base-content transition-colors group-hover:text-primary flex items-center gap-2"
							>
								{#if isUrgent && activeFilter === 'Toutes'}
									<Pin size={18} class="text-warning fill-warning/20 transform rotate-45 shrink-0" />
								{/if}
								{info.titre}
							</h3>

							<p class="text-sm leading-relaxed whitespace-pre-wrap text-base-content/70 line-clamp-3">
								{info.contenu}
							</p>

							<div class="mt-4 card-actions justify-end">
								<button 
									class="btn gap-2 font-bold text-primary btn-ghost btn-sm"
									onclick={() => openModal(info)}
								>
									Lire la suite
									<ChevronRight size={14} />
								</button>
							</div>
						</div>
					</div>
				</div>
			{:else}
				<div class="card bg-base-100 border border-dashed border-base-300 py-16">
					<div class="card-body items-center text-center gap-4">
						<div
							class="w-16 h-16 rounded-full bg-base-200 flex items-center justify-center text-base-content/30"
						>
							<Info size={32} />
						</div>
						<div class="max-w-xs">
							<h3 class="font-bold text-lg text-base-content">Aucune annonce</h3>
							<p class="text-sm text-base-content/50 mt-1">
								Il n'y a pas d'informations essentielles à afficher pour le moment.
							</p>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}

	<!-- Modal details -->
	<dialog bind:this={modalElement} class="modal modal-bottom sm:modal-middle">
		<div class="modal-box">
			<form method="dialog">
				<button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
			</form>
			{#if selectedInfo}
				<div class="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center pr-8">
					<div class="flex items-center gap-2">
						{#if selectedInfo.categorie}
							<div class="badge gap-1 badge-outline px-3 py-3 badge-primary">
								<Tag size={12} />
								{selectedInfo.categorie}
							</div>
						{/if}
						<span class="flex items-center gap-1 text-xs font-medium text-base-content/40">
							<Calendar size={12} />
							{new Date(selectedInfo.created_at).toLocaleDateString()}
						</span>
					</div>
				</div>
				
				<h3 class="font-bold text-xl mb-4 text-base-content">{selectedInfo.titre}</h3>
				<div class="bg-base-200/50 p-4 rounded-lg">
					<p class="whitespace-pre-wrap text-sm leading-relaxed text-base-content/80">{selectedInfo.contenu}</p>
				</div>
			{/if}
			<div class="modal-action flex justify-between w-full">
				<div class="flex gap-2">
					{#if currentUser?.role === 'admin' || currentUser?.role === 'delegate'}
						<button type="button" class="btn btn-error btn-outline" onclick={deleteInfo}>Supprimer</button>
						<button type="button" class="btn btn-primary" onclick={editInfo}>Modifier</button>
					{/if}
				</div>
				<form method="dialog">
					<button class="btn">Fermer</button>
				</form>
			</div>
		</div>
		<form method="dialog" class="modal-backdrop">
			<button>close</button>
		</form>
	</dialog>

	<!-- Form Modal for Create/Edit -->
	<dialog class="modal" class:modal-open={showEditModal}>
		<div class="modal-box bg-base-100 text-base-content">
			<h3 class="font-bold text-lg mb-4">{editingInfoId ? "Modifier l'information" : "Nouvelle information"}</h3>
			<form onsubmit={(e) => { e.preventDefault(); saveInfo(); }} class="flex flex-col gap-4">
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Titre</span></div>
					<input type="text" placeholder="Titre de l'annonce" class="input input-bordered w-full" bind:value={newInfo.titre} required />
				</label>
				
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
				
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Catégorie</span></div>
					<input type="text" placeholder="Ex: Urgent, Événement, Rappel..." class="input input-bordered w-full" bind:value={newInfo.categorie} />
				</label>
				
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Contenu</span></div>
					<textarea class="textarea textarea-bordered h-32 w-full" placeholder="Détails de l'annonce..." bind:value={newInfo.contenu} required></textarea>
				</label>
				
				{#if (currentUser?.role !== 'admin') && !editingInfoId}
					<div class="alert alert-info py-2 shadow-sm text-sm">
						<Info size={18} />
						<span>L'information sera en attente d'approbation par un administrateur.</span>
					</div>
				{/if}

				<div class="modal-action">
					<button type="button" class="btn" onclick={() => (showEditModal = false)}>Annuler</button>
					<button type="submit" class="btn btn-primary">Sauvegarder</button>
				</div>
			</form>
		</div>
		<form method="dialog" class="modal-backdrop" onclick={() => (showEditModal = false)}>
			<button>close</button>
		</form>
	</dialog>
</div>
