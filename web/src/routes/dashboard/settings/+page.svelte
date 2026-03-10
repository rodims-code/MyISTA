<script lang="ts">
	import { Settings, User, Save, Loader2, CheckCircle2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { ACCESS_TOKEN } from '$lib/constants';
	import { fetchCurrentUser, updateCurrentUser } from '$lib/userApi';

	let userData = $state<any>({});
	let loading = $state(true);
	let saving = $state(false);
	let successMsg = $state('');
	let errorMsg = $state('');

	onMount(async () => {
		try {
			userData = await fetchCurrentUser();
			if (!userData) {
				errorMsg = 'Impossible de charger votre profil.';
			}
		} catch (err) {
			console.error('Erreur chargement profil:', err);
			errorMsg = 'Impossible de charger votre profil.';
		} finally {
			loading = false;
		}
	});

	async function handleSave() {
		saving = true;
		successMsg = '';
		errorMsg = '';
		try {
			const { matricule, date_inscription, role, ...updateData } = userData;
			userData = await updateCurrentUser(updateData);
			successMsg = 'Profil mis à jour avec succès !';
			setTimeout(() => (successMsg = ''), 3000);
		} catch (err) {
			errorMsg = 'Une erreur est survenue lors de la sauvegarde.';
		} finally {
			saving = false;
		}
	}
</script>

<svelte:head>
	<title>Paramètres — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-6">
	<div>
		<h2 class="text-2xl font-bold text-base-content">Paramètres</h2>
		<p class="mt-1 text-sm text-base-content/50">
			Gérez vos préférences et informations personnelles
		</p>
	</div>

	<div class="flex flex-col gap-6 lg:flex-row">
		<div class="card w-full max-w-2xl border border-base-200 bg-base-100 shadow-sm">
			<div class="card-body gap-5 p-6">
				<div class="mb-2 flex items-center justify-between">
					<div class="flex items-center gap-3">
						<div
							class="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary"
						>
							<User size={20} />
						</div>
						<div>
							<h3 class="text-sm font-bold text-base-content">Profil utilisateur</h3>
							<p class="text-xs text-base-content/40">Informations de votre compte</p>
						</div>
					</div>
					{#if successMsg}
						<div class="badge animate-bounce gap-2 badge-success">
							<CheckCircle2 size={14} />
							{successMsg}
						</div>
					{/if}
				</div>

				{#if loading}
					<div class="flex justify-center py-10">
						<Loader2 size={32} class="animate-spin text-primary" />
					</div>
				{:else}
					<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
						<div class="form-control">
							<label class="label pb-1"><span class="label-text font-medium">Matricule</span></label
							>
							<input type="text" class="input-bordered input" value={userData.matricule} disabled />
							<label class="label"
								><span class="label-text-alt text-base-content/40 italic">Non modifiable</span
								></label
							>
						</div>

						<div class="form-control">
							<label class="label pb-1"
								><span class="label-text font-medium">Nom d'utilisateur</span></label
							>
							<input
								type="text"
								class="input-bordered input focus:input-primary"
								bind:value={userData.username}
							/>
						</div>

						<div class="form-control">
							<label class="label pb-1"><span class="label-text font-medium">Rôle</span></label>
							<input type="text" class="input-bordered input" value={userData.role} disabled />
						</div>

						<div class="form-control">
							<label class="label pb-1"><span class="label-text font-medium">Niveau</span></label>
							<input
								type="text"
								class="input-bordered input"
								value={userData.niveau || 'Non défini'}
								disabled
							/>
						</div>

						<div class="form-control col-span-full">
							<label class="label pb-1"><span class="label-text font-medium">Filière</span></label>
							<input
								type="text"
								class="input-bordered input"
								value={userData.filiere || 'Non défini'}
								disabled
							/>
						</div>
					</div>

					{#if errorMsg}
						<div class="alert py-2 text-sm alert-error">{errorMsg}</div>
					{/if}

					<button class="btn mt-2 gap-2 btn-primary" onclick={handleSave} disabled={saving}>
						{#if saving}
							<Loader2 size={16} class="animate-spin" />
						{:else}
							<Save size={16} />
						{/if}
						Sauvegarder les modifications
					</button>
				{/if}
			</div>
		</div>

		<div class="card max-w-lg border border-base-200 bg-base-100 shadow-sm">
			<div class="card-body gap-4 p-6">
				<div class="flex items-center gap-3">
					<div
						class="flex h-10 w-10 items-center justify-center rounded-xl bg-base-200 text-base-content/50"
					>
						<Settings size={20} />
					</div>
					<div>
						<h3 class="text-sm font-bold text-base-content">Apparence</h3>
						<p class="text-xs text-base-content/40">Personnalisez l'interface</p>
					</div>
				</div>
				<div class="form-control">
					<label class="swap swap-rotate">
						<!-- this hidden checkbox controls the state -->
						<input type="checkbox" class="theme-controller" value="synthwave" />

						<!-- sun icon -->
						<svg
							class="swap-off h-10 w-10 fill-current"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
						>
							<path
								d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"
							/>
						</svg>

						<!-- moon icon -->
						<svg
							class="swap-on h-10 w-10 fill-current"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 24 24"
						>
							<path
								d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"
							/>
						</svg>
					</label>
					<div class="dropdown mb-72">
						<div tabindex="0" role="button" class="btn m-1">
							Theme
							<svg
								width="12px"
								height="12px"
								class="inline-block h-2 w-2 fill-current opacity-60"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 2048 2048"
							>
								<path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path>
							</svg>
						</div>
						<ul
							tabindex="-1"
							class="dropdown-content z-1 w-52 rounded-box bg-base-300 p-2 shadow-2xl"
						>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="Default"
									value="default"
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="Retro"
									value="retro"
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="Cyberpunk"
									value="cyberpunk"
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="Valentine"
									value="valentine"
								/>
							</li>
							<li>
								<input
									type="radio"
									name="theme-dropdown"
									class="theme-controller btn btn-block w-full justify-start btn-ghost btn-sm"
									aria-label="Aqua"
									value="aqua"
								/>
							</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
