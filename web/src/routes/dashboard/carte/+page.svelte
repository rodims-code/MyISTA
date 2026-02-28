<script lang="ts">
  import { Map } from 'lucide-svelte';
</script>

<svelte:head>
  <title>Carte du campus — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-6">
  <div>
    <h2 class="text-2xl font-bold text-base-content">Carte du campus</h2>
    <p class="text-base-content/50 text-sm mt-1">Localisez les bâtiments et services de l'ISTA</p>
  </div>

  <div class="card bg-base-100 border border-base-200 shadow-sm">
    <div class="card-body items-center py-20 gap-4 text-center">
      <div class="w-16 h-16 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
        <Map size={32} />
      </div>
      <h3 class="font-bold text-lg text-base-content">Carte interactive</h3>
      <p class="text-base-content/50 text-sm max-w-sm">
        La carte interactive du campus sera disponible prochainement. Elle permettra de localiser rapidement les salles, bibliothèques et services.
      </p>
      <div class="badge badge-primary badge-outline mt-2">En développement</div>
    </div>
  </div>
</div>
