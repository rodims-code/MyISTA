<script lang="ts">
	import { goto } from '$app/navigation';
	import api from '$lib/index';
	import {
		GraduationCap,
		User,
		Lock,
		IdCard,
		Briefcase,
		Layers,
		AlertCircle,
		Loader2
	} from 'lucide-svelte';

	let matricule = $state('');
	let username = $state('');
	let password = $state('');
	let filiere = $state<number | null>(null);
	let niveau = $state<number | null>(null);
	let loading = $state(false);
	let error = $state('');

	// Filieres and Niveaux placeholders (since there are no GET endpoints yet)
	const filieres = [
		{ id: 1, nom: 'G' },
//		{ id: 2, nom: 'TCE (Commerce)' },
//		{ id: 3, nom: 'GE (Gestion)' }
	];
	const niveaux = [
		{ id: 1, nom: 'Preparatoire' },
//		{ id: 2, nom: 'Licence 1' },
//		{ id: 3, nom: 'Licence 2' },
//		{ id: 4, nom: 'Licence 3' }
	];

	async function handleRegister(e: SubmitEvent) {
		e.preventDefault();
		loading = true;
		error = '';

		try {
			await api.post('/api/user/register/', {
				matricule,
				username,
				password,
				filiere,
				niveau,
				role: 'student'
			});
			// After registration, redirect to login
			goto('/auth/login?registered=success');
		} catch (err: any) {
			if (err.response?.data) {
				// Concatenate backend errors if any
				const data = err.response.data;
				error = Object.entries(data)
					.map(([key, val]) => `${key}: ${val}`)
					.join(' | ');
			} else {
				error = 'Une erreur est survenue lors de la création du compte.';
			}
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Inscription — MyISTA</title>
</svelte:head>

<div
	class="flex min-h-screen items-center justify-center bg-gradient-to-br from-base-200 via-base-100 to-base-200 px-4 py-12"
>
	<!-- Blobs décoratifs -->
	<div class="pointer-events-none fixed inset-0 overflow-hidden">
		<div
			class="absolute -top-[15%] -left-[10%] h-[45%] w-[45%] rounded-full bg-primary/10 blur-[140px]"
		></div>
		<div
			class="absolute -right-[10%] -bottom-[10%] h-[40%] w-[40%] rounded-full bg-secondary/10 blur-[120px]"
		></div>
	</div>

	<div class="relative z-10 w-full max-w-xl">
		<!-- Logo -->
		<div class="mb-8 text-center">
			<div
				class="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-primary shadow-lg shadow-primary/30"
			>
				<GraduationCap size={36} class="text-primary-content" />
			</div>
			<h1 class="text-3xl font-extrabold tracking-tight text-base-content">
				My<span class="text-primary">ISTA</span>
			</h1>
			<p class="mt-1 text-sm text-base-content/50">Plateforme académique de l'ISTA</p>
		</div>

		<!-- Card -->
		<div class="card border border-base-200 bg-base-100 shadow-2xl">
			<div class="card-body gap-6 p-8">
				<div class="text-center">
					<h2 class="text-xl font-bold text-base-content">Création de compte</h2>
					<p class="mt-1 text-sm text-base-content/50">
						Rejoignez la communauté MyISTA dès aujourd'hui.
					</p>
				</div>

				<!-- Erreur -->
				{#if error}
					<div class="alert px-4 py-3 text-sm alert-error">
						<AlertCircle size={16} />
						<span>{error}</span>
					</div>
				{/if}

				<form onsubmit={handleRegister} class="flex flex-col gap-5">
					<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
						<!-- Matricule -->
						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium">Matricule</span>
							</div>
							<label
								class="input-bordered input flex w-full items-center gap-3 transition-colors focus-within:input-primary"
							>
								<IdCard size={16} class="shrink-0 text-base-content/40" />
								<input
									type="text"
									placeholder="ex: 123456789"
									class="min-w-0 grow"
									bind:value={matricule}
									required
								/>
							</label>
						</label>

						<!-- Username -->
						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium">Nom d'utilisateur</span>
							</div>
							<label
								class="input-bordered input flex w-full items-center gap-3 transition-colors focus-within:input-primary"
							>
								<User size={16} class="shrink-0 text-base-content/40" />
								<input
									type="text"
									placeholder="ex: ahmed.bennani"
									class="min-w-0 grow"
									bind:value={username}
									required
								/>
							</label>
						</label>
					</div>

					<!-- Password -->
					<label class="form-control w-full">
						<div class="label pb-1">
							<span class="label-text font-medium">Mot de passe</span>
						</div>
						<label
							class="input-bordered input flex w-full items-center gap-3 transition-colors focus-within:input-primary"
						>
							<Lock size={16} class="shrink-0 text-base-content/40" />
							<input
								type="password"
								placeholder="••••••••"
								class="min-w-0 grow"
								bind:value={password}
								required
							/>
						</label>
					</label>

					<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
						<!-- Filiere -->
						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium">Filière</span>
							</div>
							<div class="relative">
								<select
									class="select-bordered select w-full pl-10 focus:select-primary"
									bind:value={filiere}
									required
								>
									<option value={null} disabled selected>Choisir une filière</option>
									{#each filieres as f}
										<option value={f.id}>{f.nom}</option>
									{/each}
								</select>
								<Briefcase
									size={16}
									class="absolute top-1/2 left-3 -translate-y-1/2 text-base-content/40"
								/>
							</div>
						</label>

						<!-- Niveau -->
						<label class="form-control w-full">
							<div class="label pb-1">
								<span class="label-text font-medium">Niveau</span>
							</div>
							<div class="relative">
								<select
									class="select-bordered select w-full pl-10 focus:select-primary"
									bind:value={niveau}
									required
								>
									<option value={null} disabled selected>Choisir un niveau</option>
									{#each niveaux as n}
										<option value={n.id}>{n.nom}</option>
									{/each}
								</select>
								<Layers
									size={16}
									class="absolute top-1/2 left-3 -translate-y-1/2 text-base-content/40"
								/>
							</div>
						</label>
					</div>

					<!-- Submit -->
					<button
						type="submit"
						class="btn mt-2 w-full shadow-lg shadow-primary/20 btn-primary"
						disabled={loading}
					>
						{#if loading}
							<Loader2 size={18} class="animate-spin" />
							Création en cours...
						{:else}
							Créer mon compte
						{/if}
					</button>
				</form>

				<div class="divider text-xs text-base-content/30">DÉJÀ INSCRIT ?</div>
				<a href="/auth/login" class="btn font-normal no-underline btn-ghost btn-sm">
					Retour à la page de connexion
				</a>
			</div>
		</div>

		<p class="mt-6 text-center text-xs text-base-content/40">
			© 2026 MyISTA — Développé par un étudiant de l'ISTA pour l'ISTA
		</p>
	</div>
</div>
