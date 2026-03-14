<script lang="ts">
	import {
		LayoutGrid,
		Users,
		DoorOpen,
		FileText,
		TrendingUp,
		BookOpen,
		Clock,
		CheckCircle,
		UserPlus,
		FilePlus
	} from 'lucide-svelte';
	import { fetchCurrentUser } from '$lib/userApi';
	import api from '$lib/index';
	import { onMount } from 'svelte';

	import ManageDelegates from '$lib/components/ManageDelegates.svelte';
	import ManageApprovals from '$lib/components/ManageApprovals.svelte';
	import AddDocument from '$lib/components/AddDocument.svelte';
	import AddInfo from '$lib/components/AddInfo.svelte';

	let statsData = $state<any>({
		etudiants: 0,
		filieres: 0,
		salles: 0,
		documents: 0
	});

	let recentActivity = $state<any[]>([]);
	let currentUser = $state<any>(null);
	let loading = $state(true);

	let showDelegatesModal = $state(false);
	let showApprovalsModal = $state(false);
	let showAddDocModal = $state(false);
	let showAddInfoModal = $state(false);

	onMount(async () => {
		try {
			currentUser = await fetchCurrentUser();
			const res = await api.get('/api/dashboard/stats/');
			statsData = res.data.stats;
			recentActivity = res.data.recent_activity;
		} catch (error) {
			console.error('Erreur de chargement du tableau de bord:', error);
		} finally {
			loading = false;
		}
	});

	const stats = $derived([
		{
			label: 'Étudiants',
			value: statsData.etudiants,
			sub: 'Total inscrits',
			Icon: Users,
			color: 'text-primary',
			bg: 'bg-primary/10'
		},
		{
			label: 'Filières',
			value: statsData.filieres,
			sub: 'Actives',
			Icon: BookOpen,
			color: 'text-secondary',
			bg: 'bg-secondary/10'
		},
		{
			label: 'Salles',
			value: statsData.salles,
			sub: 'Disponibles',
			Icon: DoorOpen,
			color: 'text-accent',
			bg: 'bg-accent/10'
		},
		{
			label: 'Documents',
			value: statsData.documents,
			sub: 'Approuvés',
			Icon: FileText,
			color: 'text-success',
			bg: 'bg-success/10'
		}
	]);

	const activityIcon: Record<string, typeof Users> = {
		update: Clock,
		create: FileText,
		delete: DoorOpen,
		role_change: Users,
		approve: CheckCircle
	};

	const activityColor: Record<string, string> = {
		create: 'text-success bg-success/10',
		update: 'text-accent bg-accent/10',
		delete: 'text-error bg-error/10',
		role_change: 'text-primary bg-primary/10',
		approve: 'text-secondary bg-secondary/10'
	};

	const actionTranslation: Record<string, string> = {
		create: 'créé',
		update: 'modifié',
		delete: 'supprimé',
		role_change: 'changé le rôle de',
		approve: 'approuvé'
	};

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString('fr-FR', {
			day: '2-digit',
			month: 'short',
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<svelte:head>
	<title>Tableau de bord — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-8">
	<!-- Header -->
	<div>
		<h2 class="text-2xl font-bold text-base-content">Tableau de bord</h2>
		<p class="mt-1 text-sm text-base-content/50">Vue d'ensemble de la plateforme MyISTA</p>
	</div>

	<!-- Stat cards -->
	<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
		{#each stats as { label, value, sub, Icon, color, bg }}
			<div
				class="card border border-base-200 bg-base-100 shadow-sm transition-shadow hover:shadow-md"
			>
				<div class="card-body flex-row items-center gap-4 p-5">
					<div class="rounded-2xl p-3 {bg} {color} shrink-0">
						<Icon size={24} />
					</div>
					<div class="min-w-0 flex-1">
						<p class="text-3xl leading-none font-extrabold text-base-content">{value}</p>
						<p class="mt-1 text-xs font-semibold text-base-content/60">{label}</p>
						<p class="mt-0.5 flex items-center gap-1 text-xs text-base-content/40">
							<TrendingUp size={11} />
							{sub}
						</p>
					</div>
				</div>
			</div>
		{/each}
	</div>

	<!-- Activity + Quick links -->
	<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
		<!-- Activité récente (2/3) -->
		<div class="card border border-base-200 bg-base-100 shadow-sm lg:col-span-2">
			<div class="card-body p-6">
				<div class="mb-4 flex items-center gap-2">
					<Clock size={18} class="text-primary" />
					<h3 class="font-bold text-base-content">Activité récente</h3>
				</div>
				<ul class="flex flex-col gap-3">
					{#if loading}
						<li class="p-2 text-sm text-base-content/50">Chargement...</li>
					{:else if recentActivity.length === 0}
						<li class="p-2 text-sm text-base-content/50">Aucune activité récente.</li>
					{:else}
						{#each recentActivity as act}
							{@const AI = activityIcon[act.action] || Clock}
							<li class="flex items-start gap-3">
								<div
									class="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl {activityColor[
										act.action
									] || 'bg-base-200 text-base-content'}"
								>
									<AI size={15} />
								</div>
								<div class="min-w-0 flex-1">
									<p class="text-sm leading-snug text-base-content">
										<span class="font-semibold">{act.user_name}</span> a {actionTranslation[
											act.action
										] || act.action} : {act.cible_nom}
									</p>
									<p class="mt-0.5 text-xs text-base-content/40">{formatDate(act.date_action)}</p>
								</div>
							</li>
						{/each}
					{/if}
				</ul>
			</div>
		</div>

		<!-- Accès rapides (1/3) -->
		<div class="card border border-base-200 bg-base-100 shadow-sm">
			<div class="card-body p-6">
				<div class="mb-4 flex items-center gap-2">
					<LayoutGrid size={18} class="text-primary" />
					<h3 class="font-bold text-base-content">Accès rapides</h3>
				</div>
				<div class="flex flex-col gap-2">
					<a href="/dashboard/salles" class="btn justify-start gap-2 btn-outline btn-sm"
						><DoorOpen size={15} />Voir les salles</a
					>
					<a href="/dashboard/documents" class="btn justify-start gap-2 btn-outline btn-sm"
						><FileText size={15} />Documents</a
					>
					<a href="/dashboard/carte" class="btn justify-start gap-2 btn-outline btn-sm">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="15"
							height="15"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21" /><line
								x1="9"
								x2="9"
								y1="3"
								y2="18"
							/><line x1="15" x2="15" y1="6" y2="21" /></svg
						>
						Carte du campus
					</a>
				</div>
			</div>
		</div>
	</div>

	{#if currentUser && currentUser.role !== 'student'}
		<div>
			<div class="fab fab-flower">
				<!-- a focusable div with tabindex is necessary to work on all browsers. role="button" is necessary for accessibility -->
				<div tabindex="0" role="button" class="btn btn-circle btn-lg xl:btn-lg">
					<svg
						aria-label="New"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 16 16"
						fill="currentColor"
						class="size-6"
					>
						<path
							d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z"
						/>
					</svg>
				</div>

				<!-- Main Action button replaces the original button when FAB is open -->
				<button class="fab-main-action btn btn-circle btn-lg btn-primary">
					<FilePlus size={24} />
				</button>

				<!-- buttons that show up when FAB is open -->
				{#if currentUser.role === 'admin'}
					<button
						class="tooltip btn tooltip-left btn-circle btn-lg"
						data-tip="Nommer un délégué"
						onclick={() => (showDelegatesModal = true)}
					>
						<UserPlus size={24} />
					</button>
					<button
						class="tooltip btn tooltip-left btn-circle btn-lg"
						data-tip="Gérer les validations"
						onclick={() => (showApprovalsModal = true)}
					>
						<CheckCircle size={24} />
					</button>
				{/if}

				<button
					class="tooltip btn tooltip-left btn-circle btn-lg"
					data-tip="Ajouter une Information"
					onclick={() => (showAddInfoModal = true)}
				>
					<FileText size={24} />
				</button>
				<button
					class="tooltip btn tooltip-left btn-circle btn-lg"
					data-tip="Ajouter un Document"
					onclick={() => (showAddDocModal = true)}
				>
					<FilePlus size={24} />
				</button>
			</div>
		</div>
	{/if}
</div>

<ManageDelegates bind:open={showDelegatesModal} />
<ManageApprovals bind:open={showApprovalsModal} />
<AddDocument bind:open={showAddDocModal} />
<AddInfo bind:open={showAddInfoModal} />
