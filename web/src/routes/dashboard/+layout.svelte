<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { jwtDecode } from 'jwt-decode';
  import api from '$lib/index';
  import { ACCESS_TOKEN, REFRESH_TOKEN } from '$lib/constants';
  import {
    LayoutGrid,
    Map,
    DoorOpen,
    FileText,
    Settings,
    GraduationCap,
    LogOut,
    Menu,
    X,
    ChevronRight,
    Info,
    CalendarCheck
  } from 'lucide-svelte';

  let { children } = $props();

  // Auth guard
  let isAuthorized = $state<boolean | null>(null);

  onMount(async () => {
    try {
      await auth();
    } catch {
      isAuthorized = false;
    }
  });

  async function refreshToken() {
    const refresh = localStorage.getItem(REFRESH_TOKEN);
    try {
      const res = await api.post('/api/token/refresh/', { refresh });
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        isAuthorized = true;
      } else {
        isAuthorized = false;
      }
    } catch {
      isAuthorized = false;
    }
  }

  async function auth() {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) { isAuthorized = false; return; }
    const decoded: any = jwtDecode(token);
    const now = Date.now() / 1000;
    if (!decoded.exp || decoded.exp < now) {
      await refreshToken();
    } else {
      isAuthorized = true;
    }
  }

  $effect(() => {
    if (isAuthorized === false) goto('/auth/login');
  });

  function logout() {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
    goto('/auth/login');
  }

  // Sidebar state
  let sidebarOpen = $state(false);

  const navItems = [
    { href: '/dashboard',           label: 'Tableau de bord', Icon: LayoutGrid },
    { href: '/dashboard/carte',     label: 'Carte du campus', Icon: Map         },
    { href: '/dashboard/salles',    label: 'Salles',           Icon: DoorOpen    },
    { href: '/dashboard/affectations', label: 'Affectations',      Icon: CalendarCheck },
    { href: '/dashboard/documents', label: 'Documents',        Icon: FileText    },
    { href: '/dashboard/infos',     label: 'Infos',            Icon: Info        },
    { href: '/dashboard/settings',  label: 'Paramètres',       Icon: Settings    },
  ];

  // Nom de la page courante
  function getPageLabel(path: string) {
    const item = navItems.find(n => n.href === path);
    return item?.label ?? 'Dashboard';
  }
</script>

{#if isAuthorized === null}
  <!-- Loading guard -->
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <span class="loading loading-spinner loading-lg text-primary"></span>
  </div>

{:else if isAuthorized}

  <!-- ───────────────────────────────────────────────── -->
  <!--  DaisyUI Drawer layout                           -->
  <!-- ───────────────────────────────────────────────── -->
  <div class="drawer lg:drawer-open min-h-screen bg-base-200">

    <!-- Checkbox toggle (contrôle le drawer sur mobile) -->
    <input
      id="sidebar-drawer"
      type="checkbox"
      class="drawer-toggle"
      checked={sidebarOpen}
      onchange={(e) => { sidebarOpen = (e.target as HTMLInputElement).checked; }}
    />

    <!-- ── Page content ── -->
    <div class="drawer-content flex flex-col">

      <!-- Topbar -->
      <header class="navbar bg-base-100 border-b border-base-200 sticky top-0 z-30 shadow-sm px-4 gap-2">

        <!-- Hamburger (mobile + desktop toggle) -->
        <label
          for="sidebar-drawer"
          class="btn btn-ghost btn-sm drawer-button lg:hidden"
          aria-label="Ouvrir menu"
        >
          <Menu size={20} />
        </label>

        <!-- Desktop sidebar toggle -->
        <button
          class="btn btn-ghost btn-sm hidden lg:flex"
          onclick={() => { sidebarOpen = !sidebarOpen; }}
          aria-label="Basculer sidebar"
        >
          {#if sidebarOpen}
            <X size={20} />
          {:else}
            <Menu size={20} />
          {/if}
        </button>

        <!-- Breadcrumb / page title -->
        <div class="flex-1 flex items-center gap-2 ml-1">
          <div class="flex items-center gap-1 text-sm text-base-content/50">
            <span>MyISTA</span>
            <ChevronRight size={14} />
          </div>
          <span class="font-semibold text-base-content">
            {getPageLabel($page.url.pathname)}
          </span>
        </div>

        <!-- Logout -->
        <button
          class="btn btn-ghost btn-sm gap-2 text-error/80 hover:text-error hover:bg-error/10"
          onclick={logout}
        >
          <LogOut size={16} />
          <span class="hidden sm:inline">Déconnexion</span>
        </button>

      </header>

      <!-- Main content -->
      <main class="flex-1 p-4 md:p-6 lg:p-8 overflow-auto">
        {@render children()}
      </main>

    </div>

    <!-- ── Sidebar ── -->
    <aside class="drawer-side z-40">

      <!-- Overlay (mobile) -->
      <label for="sidebar-drawer" aria-label="Fermer" class="drawer-overlay"></label>

      <!--
        La sidebar change de largeur selon l'état :
        - is-drawer-close  → icon-only  (w-16)
        - is-drawer-open   → expanded   (w-64)
        On utilise les classes DaisyUI + Tailwind conditionnellement.
      -->
      <nav
        class="h-full bg-base-100 border-r border-base-200 flex flex-col transition-all duration-300 overflow-hidden
               {sidebarOpen ? 'is-drawer-open w-64' : 'is-drawer-close w-16'}"
      >

        <!-- Logo -->
        <div class="flex items-center gap-3 p-4 border-b border-base-200 min-h-[64px]">
          <div class="shrink-0 w-8 h-8 bg-primary rounded-xl flex items-center justify-center shadow shadow-primary/30">
            <GraduationCap size={18} class="text-primary-content" />
          </div>
          {#if sidebarOpen}
            <span class="font-bold text-lg tracking-tight text-base-content whitespace-nowrap">
              My<span class="text-primary">ISTA</span>
            </span>
          {/if}
        </div>

        <!-- Nav links -->
        <ul class="menu p-2 gap-1 flex-1">
          {#each navItems as { href, label, Icon }}
            <li>
              <a
                {href}
                class="flex items-center gap-3 rounded-xl font-medium
                       {$page.url.pathname === href
                          ? 'bg-primary text-primary-content shadow shadow-primary/20'
                          : 'text-base-content/70 hover:bg-base-200'}
                       {sidebarOpen ? 'px-3 py-2.5' : 'justify-center px-2 py-3'}"
                title={!sidebarOpen ? label : undefined}
              >
                <Icon size={20} class="shrink-0" />
                {#if sidebarOpen}
                  <span class="whitespace-nowrap text-sm">{label}</span>
                {/if}
              </a>
            </li>
          {/each}
        </ul>

        <!-- Bottom: logout shortcut -->
        <div class="p-2 border-t border-base-200">
          <button
            onclick={logout}
            class="flex items-center gap-3 w-full rounded-xl font-medium text-error/70 hover:bg-error/10 hover:text-error transition-colors
                   {sidebarOpen ? 'px-3 py-2.5' : 'justify-center px-2 py-3'}"
            title={!sidebarOpen ? 'Déconnexion' : undefined}
          >
            <LogOut size={20} class="shrink-0" />
            {#if sidebarOpen}
              <span class="whitespace-nowrap text-sm">Déconnexion</span>
            {/if}
          </button>
        </div>

      </nav>
    </aside>

  </div>
{/if}
