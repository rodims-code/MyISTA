<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import api from '$lib/index';
  import { jwtDecode } from 'jwt-decode';
  import { ACCESS_TOKEN, REFRESH_TOKEN } from '$lib/constants';

  export let children; // Similaire à React children

  let isAuthorized: boolean | null = null;

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
      console.error("Refresh token failed", error);
      isAuthorized = false;
    }
  }

  async function auth() {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) {
      isAuthorized = false;
      return;
    }

    const decode = jwtDecode(token);
    const tokenExpiration = decode.exp;
    const now = Date.now() / 1000;

    if (!tokenExpiration || tokenExpiration < now) {
      await refreshToken();
    } else {
      isAuthorized = true;
    }
  }

  // Gestion de la redirection
  $: if (isAuthorized === false) {
    goto('/auth/login');
  }
</script>

{#if isAuthorized === null}
  <div>Loading...</div>
{:else if isAuthorized}
  <slot />
{/if}