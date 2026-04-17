<script lang="ts">
	import { CheckCircle, XCircle, AlertTriangle, Info, X } from 'lucide-svelte';
	import { toasts, removeToast } from '$lib/stores/toast';

	const icons = {
		success: CheckCircle,
		error: XCircle,
		warning: AlertTriangle,
		info: Info
	};

	const borderColors = {
		success: 'rgba(22,163,74,0.7)',
		error: 'rgba(220,38,38,0.7)',
		warning: 'rgba(192,91,40,0.7)',
		info: 'rgba(59,130,246,0.7)'
	};

	const iconColors = {
		success: 'text-green-600',
		error: 'text-red-600',
		warning: 'text-[#C05B28]',
		info: 'text-blue-600'
	};

	const textColors = {
		success: 'text-green-900',
		error: 'text-red-900',
		warning: 'text-[#7a2e0e]',
		info: 'text-blue-900'
	};
</script>

<div class="fixed bottom-6 right-6 z-[100] flex flex-col gap-2 pointer-events-none">
	{#each $toasts as toast (toast.id)}
		<div
			class="pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-2xl max-w-sm w-full animate-slide-in {textColors[toast.type]}"
			style="background: rgba(255,255,255,0.75); backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); border: 1px solid rgba(255,255,255,0.6); border-left: 3px solid {borderColors[toast.type]}; box-shadow: 0 8px 24px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.9);"
			role="alert"
		>
			<svelte:component this={icons[toast.type]} size={18} class={iconColors[toast.type]} />
			<p class="flex-1 text-sm font-medium">{toast.message}</p>
			<button
				on:click={() => removeToast(toast.id)}
				class="p-0.5 rounded-lg opacity-60 hover:opacity-100 transition-opacity"
				aria-label="Dismiss"
			>
				<X size={14} />
			</button>
		</div>
	{/each}
</div>
