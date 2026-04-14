<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { X } from 'lucide-svelte';

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

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') close();
	}
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
	<!-- Overlay -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fade-in"
		on:click|self={close}
		role="presentation"
	>
		<!-- Panel -->
		<div
			class="relative w-full {widths[maxWidth]} bg-white rounded-xl shadow-2xl animate-slide-in max-h-[90vh] flex flex-col"
			role="dialog"
			aria-modal="true"
			aria-labelledby="modal-title"
		>
			<!-- Header -->
			<div class="flex items-center justify-between px-6 py-4 border-b border-gray-100 shrink-0">
				<h2 id="modal-title" class="text-lg font-semibold text-gray-900">{title}</h2>
				<button
					on:click={close}
					class="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
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
				<div class="px-6 py-4 border-t border-gray-100 shrink-0 flex justify-end gap-3">
					<slot name="footer" />
				</div>
			{/if}
		</div>
	</div>
{/if}
