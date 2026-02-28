<h1>Register</h1><script lang="ts">
  import { goto } from '$app/navigation';
  import api from '$lib/index';
  import { GraduationCap, User, Lock, AlertCircle, Loader2, UserPlus } from 'lucide-svelte';

  let username = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let loading = $state(false);
  let error = $state('');

  async function handleRegister(e: SubmitEvent) {
    e.preventDefault();
    loading = true;
    error = '';

    // Vérification locale du mot de passe
    if (password !== confirmPassword) {
      error = "Les mots de passe ne correspondent pas.";
      loading = false;
      return;
    }

    try {
      // Ajuste l'URL '/api/user/register/' selon ton backend Django
      await api.post('/api/user/register/', { username, password });
      
      // Après inscription, on redirige vers le login
      // Optionnel : tu peux aussi connecter l'utilisateur directement ici
      goto('/auth/login?registered=true');
    } catch (err: any) {
      if (err.response?.status === 400) {
        error = "Ce nom d'utilisateur est déjà utilisé.";
      } else {
        error = "Une erreur est survenue lors de l'inscription.";
      }
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Inscription — MyISTA</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-base-200 via-base-100 to-base-200 flex items-center justify-center px-4">

  <div class="fixed inset-0 overflow-hidden pointer-events-none">
    <div class="absolute -top-[15%] -left-[10%] w-[45%] h-[45%] bg-secondary/10 blur-[140px] rounded-full"></div>
    <div class="absolute -bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-primary/10 blur-[120px] rounded-full"></div>
  </div>

  <div class="relative z-10 w-full max-w-md">
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 bg-secondary rounded-2xl shadow-lg shadow-secondary/30 mb-4">
        <UserPlus size={36} class="text-secondary-content" />
      </div>
      <h1 class="text-3xl font-extrabold tracking-tight text-base-content">
        My<span class="text-primary">ISTA</span>
      </h1>
      <p class="text-base-content/50 mt-1 text-sm">Créez votre compte académique</p>
    </div>

    <div class="card bg-base-100 shadow-2xl border border-base-200">
      <div class="card-body p-8 gap-6">

        <div>
          <h2 class="text-xl font-bold text-base-content">Inscription</h2>
          <p class="text-base-content/50 text-sm mt-1">Remplissez les informations pour rejoindre la plateforme.</p>
        </div>

        {#if error}
          <div class="alert alert-error text-sm py-3 px-4">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        {/if}

        <form onsubmit={handleRegister} class="flex flex-col gap-4">

          <label class="form-control w-full">
            <div class="label pb-1">
              <span class="label-text font-medium">Nom d'utilisateur</span>
            </div>
            <label class="input input-bordered flex items-center gap-3 focus-within:input-secondary transition-colors">
              <User size={16} class="text-base-content/40 shrink-0" />
              <input
                type="text"
                placeholder="ex: ahmed_24"
                class="grow min-w-0"
                bind:value={username}
                required
              />
            </label>
          </label>

          <label class="form-control w-full">
            <div class="label pb-1">
              <span class="label-text font-medium">Mot de passe</span>
            </div>
            <label class="input input-bordered flex items-center gap-3 focus-within:input-secondary transition-colors">
              <Lock size={16} class="text-base-content/40 shrink-0" />
              <input
                type="password"
                placeholder="••••••••"
                class="grow min-w-0"
                bind:value={password}
                required
              />
            </label>
          </label>

          <label class="form-control w-full">
            <div class="label pb-1">
              <span class="label-text font-medium">Confirmer le mot de passe</span>
            </div>
            <label class="input input-bordered flex items-center gap-3 focus-within:input-secondary transition-colors">
              <Lock size={16} class="text-base-content/40 shrink-0" />
              <input
                type="password"
                placeholder="••••••••"
                class="grow min-w-0"
                bind:value={confirmPassword}
                required
              />
            </label>
          </label>

          <button
            type="submit"
            class="btn btn-secondary w-full mt-2 shadow-lg shadow-secondary/20"
            disabled={loading}
          >
            {#if loading}
              <Loader2 size={18} class="animate-spin" />
              Création du compte...
            {:else}
              S'inscrire
            {/if}
          </button>

          <div class="divider text-xs text-base-content/30">OU</div>

          <a href="/auth/login" class="btn btn-ghost btn-sm no-underline font-normal">
            Déjà un compte ? Se connecter
          </a>

        </form>

      </div>
    </div>

    <p class="text-center text-xs text-base-content/40 mt-6">
      © 2026 MyISTA — Plateforme Étudiante
    </p>
  </div>
</div>