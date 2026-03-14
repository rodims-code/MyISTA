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
		if (!token) {
			isAuthorized = false;
			return;
		}
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
		{ href: '/dashboard', label: 'Tableau de bord', Icon: LayoutGrid },
		{ href: '/dashboard/carte', label: 'Carte du campus', Icon: Map },
		{ href: '/dashboard/salles', label: 'Salles', Icon: DoorOpen },
		{ href: '/dashboard/affectations', label: 'Affectations', Icon: CalendarCheck },
		{ href: '/dashboard/documents', label: 'Documents', Icon: FileText },
		{ href: '/dashboard/infos', label: 'Infos', Icon: Info },
		{ href: '/dashboard/settings', label: 'Paramètres', Icon: Settings }
	];

	// Nom de la page courante
	function getPageLabel(path: string) {
		const item = navItems.find((n) => n.href === path);
		return item?.label ?? 'Dashboard';
	}
</script>

{#if isAuthorized === null}
	<!-- Loading guard -->
	<div class="flex min-h-screen items-center justify-center bg-base-200">
		<span class="loading loading-lg loading-spinner text-primary"></span>
	</div>
{:else if isAuthorized}
	<!-- ───────────────────────────────────────────────── -->
	<!--  DaisyUI Drawer layout                           -->
	<!-- ───────────────────────────────────────────────── -->
	<div class="drawer h-[100dvh] overflow-hidden bg-base-200 lg:drawer-open">
		<!-- Checkbox toggle (contrôle le drawer sur mobile) -->
		<input
			id="sidebar-drawer"
			type="checkbox"
			class="drawer-toggle"
			checked={sidebarOpen}
			onchange={(e) => {
				sidebarOpen = (e.target as HTMLInputElement).checked;
			}}
		/>

		<!-- ── Page content ── -->
		<div class="drawer-content flex h-full flex-col gap-4 overflow-y-auto py-4 pr-4 pl-4 lg:pl-0">
			<!-- Topbar -->
			<header
				class="navbar sticky top-0 z-30 shrink-0 gap-2 rounded-full border border-base-200/50 bg-base-100 px-4 shadow-sm"
			>
				<!-- Hamburger (mobile + desktop toggle) -->
				<label for="sidebar-drawer" class="drawer-button btn btn-ghost btn-sm lg:hidden">
					<Menu size={20} />
				</label>

				<!-- Desktop sidebar toggle -->
				<button
					class="btn hidden btn-ghost btn-sm lg:flex"
					onclick={() => {
						sidebarOpen = !sidebarOpen;
					}}
					aria-label="Basculer sidebar"
				>
					{#if sidebarOpen}
						<X size={20} />
					{:else}
						<Menu size={20} />
					{/if}
				</button>

				<!-- Breadcrumb / page title -->
				<div class="ml-1 flex flex-1 items-center gap-2">
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
					class="btn gap-2 text-error/80 btn-ghost btn-sm hover:bg-error/10 hover:text-error"
					onclick={logout}
				>
					<LogOut size={16} />
					<span class="hidden sm:inline">Déconnexion</span>
				</button>
			</header>

			<!-- Main content -->
			<main
				class="flex-1 shrink-0 rounded-[2rem] border border-base-200/50 bg-base-100 p-4 shadow-sm md:p-6"
			>
				{@render children()}
			</main>
		</div>

		<!-- ── Sidebar ── -->
		<aside class="drawer-side z-40">
			<!-- Overlay (mobile) -->
			<label for="sidebar-drawer" aria-label="Fermer" class="drawer-overlay"></label>

			<!-- Container padding pour Desktop et Mobile -->
			<div class="flex h-full w-72 flex-col p-4 lg:w-auto">
				<!--
          La sidebar change de largeur selon l'état :
          - is-drawer-close  → icon-only  (w-16 ou w-20 sur PC)
          - is-drawer-open   → expanded   (w-64)
        -->
				<nav
					class="flex h-full flex-col overflow-hidden rounded-[2rem] border border-base-200/50 bg-base-100 shadow-sm transition-all duration-300
                 {sidebarOpen ? 'is-drawer-open w-full lg:w-64' : 'is-drawer-close w-full lg:w-20'}"
				>
					<!-- Logo -->
					<div
						class="flex min-h-[64px] items-center gap-3 border-b border-base-200 p-4 {sidebarOpen
							? ''
							: 'w-full justify-center'}"
					>
						<div
							class="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-primary shadow shadow-primary/30"
						>
							<GraduationCap size={18} class="text-primary-content" />
						</div>
						{#if sidebarOpen}
							<span class="text-lg font-bold tracking-tight whitespace-nowrap text-base-content">
								My<span class="text-primary">ISTA</span>
							</span>
						{/if}
					</div>

					<!-- Nav links -->
					<ul class="menu w-full flex-1 gap-1 p-2">
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
										<span class="text-sm whitespace-nowrap">{label}</span>
									{/if}
								</a>
							</li>
						{/each}
					</ul>

					<!-- Bottom: logout shortcut -->
					<div class="border-t border-base-200 p-2">
						<button
							onclick={logout}
							class="flex w-full items-center gap-3 rounded-xl font-medium text-error/70 transition-colors hover:bg-error/10 hover:text-error
                   {sidebarOpen ? 'px-3 py-2.5' : 'justify-center px-2 py-3'}"
							title={!sidebarOpen ? 'Déconnexion' : undefined}
						>
							<LogOut size={20} class="shrink-0" />
							{#if sidebarOpen}
								<span class="text-sm whitespace-nowrap">Déconnexion</span>
							{/if}
						</button>
					</div>
				</nav>
			</div>
		</aside>
	</div>
{/if}
