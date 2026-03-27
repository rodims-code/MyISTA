<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { jwtDecode } from 'jwt-decode';
	import api from '$lib/index';
	import { ACCESS_TOKEN, REFRESH_TOKEN } from '$lib/constants';
	import { theme } from '$lib/theme';
	import { fetchCurrentUser } from '$lib/userApi';
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
		CalendarCheck,
		LifeBuoy,
		Home
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

	// 1. Déclare l'utilisateur comme un état réactif
	let currentUser = $state<any>(null);
	let sidebarOpen = $state(false);

	onMount(async () => {
		// L'UI se mettra à jour dès que cette ligne sera exécutée
		currentUser = await fetchCurrentUser();
	});

	// 2. Utilise $derived pour que le tableau se recalcule
	// automatiquement quand currentUser change
	const navItems = $derived([
		{
			href: currentUser?.role === 'admin' ? '/dashboard/' : '/dashboard/home',
			label: currentUser?.role === 'admin' ? 'Tableau de bord' : 'Home',
			Icon: currentUser?.role === 'admin' ? LayoutGrid : Home
		},
		{ href: '/dashboard/carte', label: 'Carte du campus', Icon: Map },
		{ href: '/dashboard/salles', label: 'Salles', Icon: DoorOpen },
		{ href: '/dashboard/affectations', label: 'Affectations', Icon: CalendarCheck },
		{ href: '/dashboard/documents', label: 'Documents', Icon: FileText },
		{ href: '/dashboard/infos', label: 'Infos', Icon: Info }
	]);

	const bottomNavItems = [
		{ href: '/dashboard/feedbacks', label: 'Feedbacks', Icon: LifeBuoy },
		{ href: '/dashboard/settings', label: 'Paramètres', Icon: Settings },
		{ action: 'logout', label: 'Déconnexion', Icon: LogOut }
	];

	// Nom de la page courante
	function getPageLabel(path: string) {
		const item = navItems.find((n) => n.href === path);
		return item?.label ?? '';
	}

	function getPageLabel2(path: string) {
		const item = bottomNavItems.find((n) => n.href === path);
		return item?.label ?? '';
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
						{getPageLabel2($page.url.pathname)}
					</span>
				</div>

				<!-- change theme -->
				<label class="swap swap-rotate">
					<!-- this hidden checkbox controls the state -->
					<input
						type="checkbox"
						class="theme-controller"
						value="synthwave"
						checked={$theme === 'synthwave'}
						onchange={(e) => ($theme = e.currentTarget.checked ? 'synthwave' : 'cupcake')}
					/>

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

					<!-- Bottom: settings, feedback and logout shortcuts -->
					<div class="space-y-1 border-t border-base-200 p-2">
						{#each bottomNavItems as item}
							<button
								onclick={() => {
									if (item.action === 'logout') {
										logout();
									} else if (item.href) {
										goto(item.href);
									}
								}}
								class="flex w-full items-center gap-3 rounded-xl font-medium transition-colors
                   {item.action === 'logout'
									? 'text-error/70 hover:bg-error/10 hover:text-error'
									: 'text-base-content/70 hover:bg-base-200'}
                   {sidebarOpen ? 'px-3 py-2.5' : 'justify-center px-2 py-3'}"
								title={!sidebarOpen ? item.label : undefined}
							>
								<item.Icon size={20} class="shrink-0" />
								{#if sidebarOpen}
									<span class="text-sm whitespace-nowrap">{item.label}</span>
								{/if}
							</button>
						{/each}
					</div>
				</nav>
			</div>
		</aside>
	</div>
{/if}
