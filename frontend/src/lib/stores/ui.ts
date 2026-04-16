import { writable } from 'svelte/store';

/** True when any modal is mounted and open. Used to suppress the chat widget. */
export const modalOpen = writable(false);
