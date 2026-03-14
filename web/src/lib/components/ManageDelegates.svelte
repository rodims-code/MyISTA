<script lang="ts">
	import { Users, Search, Loader2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';

	let { open = $bindable(false) } = $props();

	let search = $state('');
	let users = $state<any[]>([]);
	let loading = $state(false);
	let errorMsg = $state('');

	const filteredUsers = $derived(
		users.filter(
			(u) =>
				u.username.toLowerCase().includes(search.toLowerCase()) ||
				u.matricule.toLowerCase().includes(search.toLowerCase())
		)
	);

	async function loadUsers() {
		loading = true;
		try {
			// We'll need a way to list users, maybe a new endpoint if we don't have one,
			// but assuming for now we can fetch them or we build a small fetcher
			// For now, let's assume we can fetch students
			const res = await api.get('/api/users/?role=student,delegate'); // Example endpoint, we might need to create this in Django
			users = res.data;
		} catch (err) {
			console.error('Erreur chargement utilisateurs', err);
			errorMsg = 'Impossible de charger la liste des étudiants.';
		} finally {
			loading = false;
		}
	}

	async function setRole(userId: number, role: string) {
		try {
			await api.patch(`/api/users/${userId}/role/`, { role });
			// Update local state to reflect change
			users = users.map((u) => (u.id === userId ? { ...u, role } : u));
		} catch (err) {
			console.error('Erreur modification rôle', err);
			alert('Erreur lors de la modification du rôle.');
		}
	}

	// Load users when modal opens
	$effect(() => {
		if (open) {
			loadUsers();
		}
	});

	function close() {
		open = false;
	}
</script>

<dialog class="modal" class:modal-open={open} aria-labelledby="delegate-modal-title">
	<div class="modal-box max-w-2xl bg-base-100">
		<form method="dialog">
			<button class="btn absolute top-2 right-2 btn-circle btn-ghost btn-sm" onclick={close}
				>✕</button
			>
		</form>
		<h3 id="delegate-modal-title" class="mb-4 flex items-center gap-2 text-lg font-bold">
			<Users size={20} class="text-primary" />
			Gestion des Délégués
		</h3>

		<div class="form-control mb-4">
			<label class="input-bordered input flex items-center gap-2">
				<Search size={16} class="opacity-50" />
				<input
					type="text"
					class="grow"
					placeholder="Rechercher par nom ou matricule..."
					bind:value={search}
				/>
			</label>
		</div>

		{#if loading}
			<div class="flex justify-center py-8">
				<Loader2 class="animate-spin text-primary" size={32} />
			</div>
		{:else if errorMsg}
			<div class="alert py-2 text-sm alert-error">{errorMsg}</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="table w-full table-sm">
					<thead>
						<tr>
							<th>Matricule</th>
							<th>Nom</th>
							<th>Filière</th>
							<th>Rôle actuel</th>
							<th>Action</th>
						</tr>
					</thead>
					<tbody>
						{#each filteredUsers as user}
							<tr class="hover">
								<td class="font-mono text-xs">{user.matricule}</td>
								<td class="font-semibold">{user.username}</td>
								<td>{user.filiere || '-'}</td>
								<td>
									<span
										class="badge badge-outline badge-sm {user.role === 'delegate'
											? 'badge-primary'
											: ''}"
									>
										{user.role}
									</span>
								</td>
								<td>
									{#if user.role === 'student'}
										<button
											class="btn btn-xs btn-primary"
											onclick={() => setRole(user.id, 'delegate')}
										>
											Nommer Délégué
										</button>
									{:else if user.role === 'delegate'}
										<button
											class="btn text-error btn-ghost btn-xs"
											onclick={() => setRole(user.id, 'student')}
										>
											Retirer rôle
										</button>
									{/if}
								</td>
							</tr>
						{:else}
							<tr>
								<td colspan="5" class="text-center py-4 text-base-content/50 text-sm"
									>Aucun étudiant trouvé.</td
								>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
	<form method="dialog" class="modal-backdrop" onclick={close}>
		<button>close</button>
	</form>
</dialog>
