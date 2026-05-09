<script lang="ts">
  import { goto } from '$app/navigation';
  import api from '$lib/index';
  import { ACCESS_TOKEN, REFRESH_TOKEN } from '$lib/constants';
  import { User, Lock, AlertCircle, Loader2, Home } from 'lucide-svelte';
	import { fetchCurrentUser } from '$lib/userApi';


	import logoIstaIcon from '$lib/assets/myIstaIcon.png'


  let matricule = $state('');
  let password = $state('');
  let loading = $state(false);
  let error = $state('');

 async function handleLogin(e: SubmitEvent) {
    e.preventDefault();
    loading = true;
    error = '';

    try {
      // 1. Récupération des tokens
      const res = await api.post('/api/token/', { matricule, password });
      
      // 2. Stockage immédiat (nécessaire pour que fetchCurrentUser fonctionne car il utilise le token)
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh);

      // 3. Récupérer l'utilisateur pour connaître son rôle
      const user = await fetchCurrentUser();

      // 4. Redirection conditionnelle
      if (user?.role === 'admin') {
        goto('/dashboard'); // URL pour l'admin
      } else {
        goto('/dashboard/home'); // URL pour student/delegate
      }

    } catch (err: any) {
      console.error(err);
      if (err.response?.status === 401) {
        error = 'Nom d\'utilisateur ou mot de passe incorrect.';
      } else {
        error = 'Une erreur est survenue lors de la connexion.';
      }
      // Optionnel : nettoyer le localStorage en cas d'échec
      localStorage.removeItem(ACCESS_TOKEN);
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Connexion — MyISTA</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-base-200 via-base-100 to-base-200 flex items-center justify-center px-4">

  <!-- Blobs décoratifs -->
  <div class="fixed inset-0 overflow-hidden pointer-events-none">
    <div class="absolute -top-[15%] -left-[10%] w-[45%] h-[45%] bg-primary/10 blur-[140px] rounded-full"></div>
    <div class="absolute -bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-secondary/10 blur-[120px] rounded-full"></div>
  </div>

  <div class="relative z-10 w-full max-w-md">
    <!-- Bouton retour accueil -->
    <a href="/" class="btn btn-ghost btn-sm mb-4 gap-2 text-base-content/60 hover:text-base-content">
      <Home size={16} />
      Retour à l'accueil
    </a>
    <!-- Logo -->
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-40 h-40 bg-primary rounded-2xl shadow-lg shadow-primary/30 mb-4">
        <img src={logoIstaIcon} alt="Logo ISTA" class="h-35 w-35 object-cover" />
      </div>
      <h1 class="text-3xl font-extrabold tracking-tight text-base-content">
        My<span class="text-primary">ISTA</span>
      </h1>
      <p class="text-base-content/50 mt-1 text-sm">Plateforme académique de l'ISTA</p>
    </div>

    <!-- Card -->
    <div class="card bg-base-100 shadow-2xl border border-base-200">
      <div class="card-body p-8 gap-6">

        <div class="text-center">
          <h2 class="text-xl font-bold text-base-content">Connexion</h2>
          <p class="text-base-content/50 text-sm mt-1">Entrez vos identifiants pour accéder à votre espace.</p>
        </div>

        <!-- Erreur -->
        {#if error}
          <div class="alert alert-error text-sm py-3 px-4">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        {/if}

        <form onsubmit={handleLogin} class="flex flex-col gap-4">

          <!-- Username -->
          <label class="form-control w-full">
            <div class="label pb-1">
              <span class="label-text font-medium">Entrez votre matricule</span>
            </div>
            <label class="input input-bordered w-full flex items-center gap-3 focus-within:input-primary transition-colors">
              <User size={16} class="text-base-content/40 shrink-0" />
              <input
                type="text"
                placeholder="00/00001234"
                class="grow min-w-0"
                bind:value={matricule}
                required
                autocomplete="username"
              />
            </label>
          </label>

          <!-- Password -->
          <label class="form-control w-full">
            <div class="label pb-1">
              <span class="label-text font-medium">Mot de passe</span>
            </div>
            <label class="input input-bordered flex w-full items-center gap-3 focus-within:input-primary transition-colors">
              <Lock size={16} class="text-base-content/40 shrink-0" />
              <input
                type="password"
                placeholder="••••••••"
                class="grow min-w-0"
                bind:value={password}
                required
                autocomplete="current-password"
              />
            </label>
          </label>

          <!-- Submit -->
          <button
            type="submit"
            class="btn btn-primary w-full mt-2 shadow-lg shadow-primary/20"
            disabled={loading}
          >
            {#if loading}
              <Loader2 size={18} class="animate-spin" />
              Connexion en cours...
            {:else}
              Se connecter
            {/if}
          </button>

        </form>
        <div class="divider text-xs text-base-content/30">OU</div>
        <a href="/auth/register" class="btn btn-ghost btn-sm no-underline font-normal">Vous n'avez pas de compte ? <span>Creez un compte </span></a>
      </div>
    </div>

    <p class="text-center text-xs text-base-content/40 mt-6">
      © 2026 MyISTA — Développé par un étudiant de l'ISTA pour l'ISTA
    </p>
  </div>
</div>