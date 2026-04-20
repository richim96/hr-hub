import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const stored = browser ? localStorage.getItem('darkMode') === 'true' : false;
export const darkMode = writable<boolean>(stored);

if (browser) {
	darkMode.subscribe((val) => {
		localStorage.setItem('darkMode', String(val));
		document.documentElement.classList.toggle('dark', val);
	});
}
