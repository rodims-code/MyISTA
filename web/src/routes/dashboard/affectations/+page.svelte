<script lang="ts">
	import { CalendarCheck, DoorOpen, Layers, Briefcase, Search, Plus } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { Calendar, TimeGrid, DayGrid, List as ListPlugin, Interaction } from '@event-calendar/core';
	import { fetchCurrentUser } from '$lib/userApi';
	import '@event-calendar/core/index.css';

	let affectations = $state<any[]>([]);
	let salles = $state<any[]>([]);
	let events = $state<any[]>([]);
	let loading = $state(true);
	let search = $state('');
	let currentUser = $state<any>(null);

	// Modal
	let showModal = $state(false);
	let newEvent = $state({ titre: '', debut: '', fin: '', all_day: false, repetition: 'none', fin_repetition: '', filiere: '', niveau: '' });
	
	let showDetailsModal = $state(false);
	let selectedEvent = $state<any>(null);

	const filiereMap: Record<number, string> = {
		1: 'TSDI (Digital)',
		2: 'TCE (Commerce)',
		3: 'GE (Gestion)'
	};
	const niveauMap: Record<number, string> = {
		1: '1ère Année',
		2: '2ème Année'
	};

	let plugins = [TimeGrid, DayGrid, ListPlugin, Interaction];
	
	let options = $derived({
		view: 'timeGridWeek',
		events: events.map((e) => ({
			id: e.id,
			title: e.titre,
			start: e.debut,
			end: e.fin,
			allDay: e.all_day,
            backgroundColor: '#3b82f6'
		})),
		headerToolbar: {
			start: 'prev,next today',
			center: 'title',
			end: 'dayGridMonth,timeGridWeek,listWeek'
		},
        buttonText: {
            today: "Aujourd'hui",
            dayGridMonth: 'Mois',
            timeGridWeek: 'Semaine',
            listWeek: 'Liste'
        },
        locale: 'fr',
		selectable: currentUser?.role === 'admin',
		editable: currentUser?.role === 'admin',
		select: (info: any) => {
			if (currentUser?.role === 'admin') {
				// Convert to iso strings for inputs (YYYY-MM-DDThh:mm)
				const startIso = new Date(info.start.getTime() - info.start.getTimezoneOffset() * 60000).toISOString().slice(0,16);
				const endIso = new Date(info.end.getTime() - info.end.getTimezoneOffset() * 60000).toISOString().slice(0,16);
				newEvent = { titre: '', debut: startIso, fin: endIso, all_day: info.allDay };
				showModal = true;
			}
		},
		eventClick: (info: any) => {
			selectedEvent = info.event;
			showDetailsModal = true;
		}
	});

	onMount(async () => {
		try {
			currentUser = await fetchCurrentUser();
			const [affRes, sallesRes, eventsRes] = await Promise.all([
				api.get('/api/affectations/'),
				api.get('/api/salles/'),
				api.get('/api/events/')
			]);
			affectations = affRes.data;
			salles = sallesRes.data;
			events = eventsRes.data;
		} catch (error) {
			console.error('Erreur chargement:', error);
		} finally {
			loading = false;
		}
	});

	function getSalleNom(id: number) {
		return salles.find((s) => s.id === id)?.nom || `Salle #${id}`;
	}

	const filtered = $derived(
		affectations.filter((a) => {
			const salleNom = getSalleNom(a.salle).toLowerCase();
			const filiereNom = (filiereMap[a.filiere] || '').toLowerCase();
			const query = search.toLowerCase();
			return salleNom.includes(query) || filiereNom.includes(query);
		})
	);

	async function saveEvent() {
		try {
			const payload = {
				titre: newEvent.titre,
				debut: newEvent.debut,
				fin: newEvent.fin,
				all_day: newEvent.all_day,
				repetition: newEvent.repetition,
				fin_repetition: newEvent.fin_repetition || undefined,
				filiere: newEvent.filiere || null,
				niveau: newEvent.niveau || null
			};
			const res = await api.post('/api/events/', payload);
			if (Array.isArray(res.data)) {
				events = [...events, ...res.data];
			} else {
				events = [...events, res.data];
			}
			showModal = false;
		} catch (error) {
			console.error('Save error', error);
			alert('Erreur de sauvegarde');
		}
	}
</script>

<svelte:head>
	<title>Emplois du temps & Affectations — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-6">
	<!-- HEADER -->
	<div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
		<div>
			<h2 class="text-2xl font-bold text-base-content">Emplois du temps & Affectations</h2>
			<p class="mt-1 text-sm text-base-content/50">
				Calendrier de planification des salles par filière et niveau
			</p>
		</div>
		
		<div class="flex gap-2">
			{#if currentUser?.role === 'admin'}
				<button
					class="btn btn-primary shadow shadow-primary/30"
					onclick={() => {
						newEvent = { titre: '', debut: '', fin: '', all_day: false, repetition: 'none', fin_repetition: '', filiere: '', niveau: '' };
						showModal = true;
					}}
				>
					<Plus size={18} />
					Ajouter événement
				</button>
			{/if}
			<label class="input-bordered input flex w-full items-center gap-2 sm:w-64">
				<Search size={15} class="text-base-content/40" />
				<input
					type="text"
					placeholder="Rechercher…"
					class="grow"
					bind:value={search}
				/>
			</label>
		</div>
	</div>

	<div class="flex flex-col xl:flex-row gap-6 items-start">
		<!-- CALENDAR -->
		<div class="card flex-[2] w-full border border-base-200 bg-base-100 p-4 shadow-sm min-w-0">
			{#if loading}
				<div class="flex items-center gap-2 text-base-content/50 py-10 justify-center">
					<span class="loading loading-spinner loading-md"></span>
					Chargement du calendrier...
				</div>
			{:else}
				<Calendar {plugins} {options} />
			{/if}
		</div>

		<!-- AFFECTATIONS FIXES -->
		<div class="flex-1 w-full flex flex-col gap-4">
			<div class="flex items-center justify-between px-1">
				<h3 class="font-bold text-lg text-base-content/80">Affectations Fixes</h3>
				<span class="badge badge-primary badge-sm">{filtered.length}</span>
			</div>
			
			<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-1 gap-4">
				{#if loading}
					{#each Array(4) as _}
						<div class="card animate-pulse border border-base-200 bg-base-100">
							<div class="card-body h-32 p-6"></div>
						</div>
					{/each}
				{:else}
					{#each filtered as aff}
						<div
							class="group card border border-base-200 bg-base-100 shadow-sm transition-all hover:shadow-md"
						>
							<div class="card-body flex-row items-center gap-4 p-6">
								<div
									class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-content"
								>
									<DoorOpen size={24} />
								</div>
		
								<div class="min-w-0 flex-1">
									<h3 class="font-mono text-lg font-bold text-base-content">
										{getSalleNom(aff.salle)}
									</h3>
									<div class="mt-1 flex flex-col gap-1">
										<div class="flex items-center gap-2 text-xs text-base-content/60">
											<Briefcase size={12} />
											<span class="truncate"
												>{filiereMap[aff.filiere] || `Filière #${aff.filiere}`}</span
											>
										</div>
										<div class="flex items-center gap-2 text-xs text-base-content/60">
											<Layers size={12} />
											<span>{niveauMap[aff.niveau] || `Niveau #${aff.niveau}`}</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					{:else}
						<div class="col-span-full card bg-base-200/50 border border-dashed border-base-300 py-10">
							<div class="card-body items-center text-center gap-4">
								<CalendarCheck size={32} class="text-base-content/20" />
								<p class="text-base-content/40 text-sm font-medium">Aucune affectation trouvée</p>
							</div>
						</div>
					{/each}
				{/if}
			</div>
		</div>
	</div>
</div>

<!-- Modal Ajout Événement -->
<dialog class="modal" class:modal-open={showModal}>
	<div class="modal-box bg-base-100 text-base-content">
		<h3 class="font-bold text-lg mb-4">Nouvel événement</h3>
		<form onsubmit={(e) => { e.preventDefault(); saveEvent(); }} class="flex flex-col gap-4">
			<label class="form-control w-full">
				<div class="label"><span class="label-text">Titre</span></div>
				<input type="text" placeholder="Ex: TP Algo Salle 12" class="input input-bordered w-full" bind:value={newEvent.titre} required />
			</label>
			
			<div class="grid grid-cols-2 gap-4">
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Début</span></div>
					<input type="datetime-local" class="input input-bordered w-full" bind:value={newEvent.debut} required />
				</label>
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Fin</span></div>
					<input type="datetime-local" class="input input-bordered w-full" bind:value={newEvent.fin} required />
				</label>
			</div>

			<label class="label cursor-pointer justify-start gap-3 mt-2">
				<input type="checkbox" class="checkbox checkbox-primary" bind:checked={newEvent.all_day} />
				<span class="label-text">Toute la journée</span> 
			</label>
			
			<div class="grid grid-cols-2 gap-4">
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Filière</span></div>
					<select class="select select-bordered" bind:value={newEvent.filiere}>
						<option value="">Toutes (Global)</option>
						{#each Object.values(filiereMap) as filiere}
							<option value={filiere}>{filiere}</option>
						{/each}
					</select>
				</label>
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Niveau</span></div>
					<select class="select select-bordered" bind:value={newEvent.niveau}>
						<option value="">Tous</option>
						{#each Object.values(niveauMap) as n}
							<option value={n}>{n}</option>
						{/each}
					</select>
				</label>
			</div>

			<div class="grid grid-cols-2 gap-4">
				<label class="form-control w-full">
					<div class="label"><span class="label-text">Répétition</span></div>
					<select class="select select-bordered" bind:value={newEvent.repetition}>
						<option value="none">Aucune</option>
						<option value="quotidienne">Quotidienne</option>
						<option value="hebdomadaire">Hebdomadaire</option>
						<option value="mensuelle">Mensuelle</option>
					</select>
				</label>
				{#if newEvent.repetition !== 'none'}
					<label class="form-control w-full">
						<div class="label"><span class="label-text">Jusqu'au</span></div>
						<input type="date" class="input input-bordered w-full" bind:value={newEvent.fin_repetition} required />
					</label>
				{/if}
			</div>

			<div class="modal-action">
				<button type="button" class="btn" onclick={() => (showModal = false)}>Annuler</button>
				<button type="submit" class="btn btn-primary">Sauvegarder</button>
			</div>
		</form>
	</div>
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<form method="dialog" class="modal-backdrop" onclick={() => (showModal = false)}>
		<button>close</button>
	</form>
</dialog>

<!-- Modal Détails Événement -->
<dialog class="modal" class:modal-open={showDetailsModal}>
	<div class="modal-box bg-base-100 text-base-content relative">
        <form method="dialog" class="absolute right-4 top-4">
            <button class="btn btn-sm btn-circle btn-ghost" onclick={() => (showDetailsModal = false)}>✕</button>
        </form>
		{#if selectedEvent}
			<h3 class="font-bold text-xl mb-6 pr-8 text-primary">
				{selectedEvent.title}
			</h3>
			
			<div class="flex flex-col gap-4 text-sm bg-base-200/50 p-5 rounded-box border border-base-200/60">
				<div class="flex flex-col gap-1">
					<span class="text-base-content/50 uppercase text-[10px] font-bold tracking-wider">Début</span>
					<span class="font-medium text-base-content text-base">{new Date(selectedEvent.start).toLocaleString('fr-FR', { dateStyle: 'full', timeStyle: 'short' })}</span>
				</div>
                {#if selectedEvent.end}
				<div class="flex flex-col gap-1">
					<span class="text-base-content/50 uppercase text-[10px] font-bold tracking-wider">Fin</span>
					<span class="font-medium text-base-content text-base">{new Date(selectedEvent.end).toLocaleString('fr-FR', { dateStyle: 'full', timeStyle: 'short' })}</span>
				</div>
                {/if}
				{#if selectedEvent.allDay}
					<div class="badge badge-neutral mt-2">Toute la journée</div>
				{/if}
			</div>

			<div class="modal-action mt-6">
				<button class="btn" onclick={() => (showDetailsModal = false)}>Fermer</button>
			</div>
		{/if}
	</div>
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<form method="dialog" class="modal-backdrop" onclick={() => (showDetailsModal = false)}>
		<button>close</button>
	</form>
</dialog>

