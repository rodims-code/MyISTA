<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import api from '$lib/index';
	import { jwtDecode } from 'jwt-decode';
	import { ACCESS_TOKEN, REFRESH_TOKEN } from '$lib/constants';

	let { children } = $props();

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
		} catch (error) {
			console.error('Refresh token failed', error);
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
		const tokenExpiration = decoded.exp;
		const now = Date.now() / 1000;

		if (!tokenExpiration || tokenExpiration < now) {
			await refreshToken();
		} else {
			isAuthorized = true;
		}
	}

	$effect(() => {
		if (isAuthorized === false) goto('/auth/login');
	});
</script>

{#if isAuthorized === null}
	<div class="flex min-h-screen items-center justify-center bg-base-200">
		<span class="loading loading-lg loading-spinner text-primary"></span>
	</div>
{:else if isAuthorized}
	{@render children()}
{/if}
