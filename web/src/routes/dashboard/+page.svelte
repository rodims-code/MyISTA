<script lang="ts">
  import { LayoutGrid, Users, DoorOpen, FileText, TrendingUp, BookOpen, Clock } from 'lucide-svelte';
  //import  fetchCurrentUser from "$lib/userApi"

  const stats = [
    { label: 'Étudiants',  value: '342',  sub: '+12 ce mois',     Icon: Users,      color: 'text-primary',   bg: 'bg-primary/10'   },
    { label: 'Filières',   value: '8',    sub: '4 actives',       Icon: BookOpen,   color: 'text-secondary', bg: 'bg-secondary/10' },
    { label: 'Salles',     value: '24',   sub: '18 disponibles',  Icon: DoorOpen,   color: 'text-accent',    bg: 'bg-accent/10'    },
    { label: 'Documents',  value: '137',  sub: 'Cette semaine',   Icon: FileText,   color: 'text-success',   bg: 'bg-success/10'   },
  ];

  const recentActivity = [
    { text: 'Salle B-204 affectée au groupe TSDI-2',       time: 'Il y a 5 min',   type: 'room'  },
    { text: 'Nouveau document ajouté : Programme S4',       time: 'Il y a 22 min',  type: 'doc'   },
    { text: 'Étudiant Youssef El Fassi inscrit en TSDI-3', time: 'Il y a 1h',      type: 'user'  },
    { text: 'Affectation salle TD-101 modifiée',           time: 'Hier, 16:30',    type: 'room'  },
    { text: 'Document "Planning S3" mis à jour',           time: 'Hier, 14:12',    type: 'doc'   },
  ];

  const activityIcon: Record<string, typeof Users> = {
    room: DoorOpen,
    doc:  FileText,
    user: Users,
  };

  const activityColor: Record<string, string> = {
    room: 'text-accent bg-accent/10',
    doc:  'text-success bg-success/10',
    user: 'text-primary bg-primary/10',
  };
</script>

<svelte:head>
  <title>Tableau de bord — MyISTA</title>
</svelte:head>

<div class="flex flex-col gap-8">

  <!-- Header -->
  <div>
    <h2 class="text-2xl font-bold text-base-content">Tableau de bord</h2>
    <p class="text-base-content/50 text-sm mt-1">Vue d'ensemble de la plateforme MyISTA</p>
  </div>

  <!-- Stat cards -->
  <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
    {#each stats as { label, value, sub, Icon, color, bg }}
      <div class="card bg-base-100 border border-base-200 shadow-sm hover:shadow-md transition-shadow">
        <div class="card-body p-5 flex-row items-center gap-4">
          <div class="rounded-2xl p-3 {bg} {color} shrink-0">
            <Icon size={24} />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-3xl font-extrabold text-base-content leading-none">{value}</p>
            <p class="text-xs font-semibold text-base-content/60 mt-1">{label}</p>
            <p class="text-xs text-base-content/40 mt-0.5 flex items-center gap-1">
              <TrendingUp size={11} />
              {sub}
            </p>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <!-- Activity + Quick links -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

    <!-- Activité récente (2/3) -->
    <div class="card bg-base-100 border border-base-200 shadow-sm lg:col-span-2">
      <div class="card-body p-6">
        <div class="flex items-center gap-2 mb-4">
          <Clock size={18} class="text-primary" />
          <h3 class="font-bold text-base-content">Activité récente</h3>
        </div>
        <ul class="flex flex-col gap-3">
          {#each recentActivity as { text, time, type }}
            {@const AI = activityIcon[type]}
            <li class="flex items-start gap-3">
              <div class="shrink-0 mt-0.5 w-8 h-8 rounded-xl flex items-center justify-center {activityColor[type]}">
                <AI size={15} />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-base-content leading-snug">{text}</p>
                <p class="text-xs text-base-content/40 mt-0.5">{time}</p>
              </div>
            </li>
          {/each}
        </ul>
      </div>
    </div>

    <!-- Accès rapides (1/3) -->
    <div class="card bg-base-100 border border-base-200 shadow-sm">
      <div class="card-body p-6">
        <div class="flex items-center gap-2 mb-4">
          <LayoutGrid size={18} class="text-primary" />
          <h3 class="font-bold text-base-content">Accès rapides</h3>
        </div>
        <div class="flex flex-col gap-2">
          <a href="/dashboard/salles"    class="btn btn-outline btn-sm justify-start gap-2"><DoorOpen size={15} />Voir les salles</a>
          <a href="/dashboard/documents" class="btn btn-outline btn-sm justify-start gap-2"><FileText size={15} />Documents</a>
          <a href="/dashboard/carte"     class="btn btn-outline btn-sm justify-start gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" x2="9" y1="3" y2="18"/><line x1="15" x2="15" y1="6" y2="21"/></svg>
            Carte du campus
          </a>
        </div>
      </div>
    </div>

  </div>
</div>
