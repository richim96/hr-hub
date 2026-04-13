<script lang="ts">
	import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-svelte';
	import { toasts, removeToast } from '$lib/stores/toast';

	const icons = {
		success: CheckCircle,
		error: XCircle,
		warning: AlertTriangle,
		info: Info
	};

	const styles = {
		success: 'bg-white border-l-4 border-green-500 text-green-800',
		error: 'bg-white border-l-4 border-red-500 text-red-800',
		warning: 'bg-white border-l-4 border-[#C05B28] text-[#C05B28]',
		info: 'bg-white border-l-4 border-blue-500 text-blue-800'
	};

	const iconColors = {
		success: 'text-green-500',
		error: 'text-red-500',
		warning: 'text-[#C05B28]',
		info: 'text-blue-500'
	};
</script>

<div class="fixed bottom-6 right-6 z-[100] flex flex-col gap-2 pointer-events-none">
	{#each $toasts as toast (toast.id)}
		<div
			class="pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-lg shadow-lg
				   border border-gray-100 max-w-sm w-full animate-slide-in {styles[toast.type]}"
			role="alert"
		>
			<svelte:component this={icons[toast.type]} size={18} class={iconColors[toast.type]} />
			<p class="flex-1 text-sm font-medium">{toast.message}</p>
			<button
				on:click={() => removeToast(toast.id)}
				class="p-0.5 rounded opacity-60 hover:opacity-100 transition-opacity"
				aria-label="Dismiss"
			>
				<X size={14} />
			</button>
		</div>
	{/each}
</div>
