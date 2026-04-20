import { writable } from 'svelte/store';
import type { Toast, ToastType } from '$lib/types';
import { randomUUID } from '$lib/utils';

const MAX_TOASTS = 5;
const AUTO_DISMISS_MS = 4000;

export const toasts = writable<Toast[]>([]);

export function addToast(type: ToastType, message: string): void {
	const id = randomUUID();
	toasts.update((current) => {
		const updated = [...current, { id, type, message }];
		return updated.length > MAX_TOASTS ? updated.slice(updated.length - MAX_TOASTS) : updated;
	});
	setTimeout(() => removeToast(id), AUTO_DISMISS_MS);
}

export function removeToast(id: string): void {
	toasts.update((current) => current.filter((t) => t.id !== id));
}
