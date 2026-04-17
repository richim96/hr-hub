<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { X } from 'lucide-svelte';
	import { modalOpen } from '$lib/stores/ui';

	export let open = false;
	export let title = '';
	export let maxWidth: 'sm' | 'md' | 'lg' | 'xl' | '2xl' = 'lg';

	const dispatch = createEventDispatcher<{ close: void }>();

	const widths = {
		sm: 'max-w-sm',
		md: 'max-w-md',
		lg: 'max-w-lg',
		xl: 'max-w-xl',
		'2xl': 'max-w-2xl'
	};

	function close() {
		dispatch('close');
	}

	$: if (typeof document !== 'undefined') {
		document.body.style.overflow = open ? 'hidden' : '';
		modalOpen.set(open);
	}
</script>

{#if open}
	<!-- Overlay -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in"
		style="background: rgba(0,0,0,0.25); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);"
		role="presentation"
	>
		<!-- Panel -->
		<div
			class="relative w-full {widths[maxWidth]} rounded-3xl animate-slide-in max-h-[90vh] flex flex-col"
			style="background: rgba(255,255,255,0.65); backdrop-filter: blur(32px) saturate(200%); -webkit-backdrop-filter: blur(32px) saturate(200%); border: 1px solid rgba(255,255,255,0.7); box-shadow: 0 24px 64px rgba(0,0,0,0.15), 0 8px 24px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.95);"
			role="dialog"
			aria-modal="true"
			aria-labelledby="modal-title"
		>
			<!-- Header -->
			<div class="flex items-center justify-between px-6 py-4 shrink-0" style="border-bottom: 1px solid rgba(255,255,255,0.4);">
				<h2 id="modal-title" class="text-lg font-medium text-gray-900 tracking-tight flex items-center gap-2">
					{#if $$slots.title}<slot name="title" />{:else}{title}{/if}
				</h2>
				<button
					on:click={close}
					class="p-1.5 rounded-xl text-gray-400 hover:text-gray-600 transition-colors"
					style="background: rgba(0,0,0,0.05); border: 1px solid rgba(255,255,255,0.4);"
					aria-label="Close modal"
				>
					<X size={18} />
				</button>
			</div>

			<!-- Body -->
			<div class="overflow-y-auto flex-1 px-6 py-5">
				<slot />
			</div>

			<!-- Footer -->
			{#if $$slots.footer}
				<div class="px-6 py-4 shrink-0 flex justify-end gap-3" style="border-top: 1px solid rgba(255,255,255,0.4);">
					<slot name="footer" />
				</div>
			{/if}
		</div>
	</div>
{/if}
