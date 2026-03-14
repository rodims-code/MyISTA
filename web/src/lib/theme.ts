import { browser } from '$app/environment';
import { writable } from 'svelte/store';

const initialTheme = browser ? window.localStorage.getItem('theme') || 'cupcake' : 'cupcake';

export const theme = writable(initialTheme);

if (browser) {
	theme.subscribe((value) => {
		window.localStorage.setItem('theme', value);
		document.documentElement.setAttribute('data-theme', value);
	});
}
