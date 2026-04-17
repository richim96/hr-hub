<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { ChevronsLeft, ChevronLeft, ChevronRight, ChevronsRight } from 'lucide-svelte';

	export let page: number;
	export let totalPages: number;
	export let totalItems: number;
	export let pageSize: number;
	export let position: 'top' | 'bottom' = 'bottom';

	const dispatch = createEventDispatcher<{ first: void; prev: void; next: void; last: void }>();

	$: rangeStart = (page - 1) * pageSize + 1;
	$: rangeEnd = Math.min(page * pageSize, totalItems);
</script>

<div
	class="flex items-center justify-between px-4 py-2.5 text-sm text-gray-600"
	style="{position === 'top' ? 'border-bottom' : 'border-top'}: 1px solid rgba(255,255,255,0.4);"
>
	<span class="text-gray-500">{rangeStart}–{rangeEnd} of {totalItems}</span>

	<div class="flex items-center gap-0.5">
		<button
			class="p-1.5 rounded-xl disabled:opacity-30 disabled:cursor-not-allowed transition-all hover:bg-white/50"
			disabled={page <= 1}
			on:click={() => dispatch('first')}
			aria-label="First page"
		>
			<ChevronsLeft size={15} />
		</button>
		<button
			class="p-1.5 rounded-xl disabled:opacity-30 disabled:cursor-not-allowed transition-all hover:bg-white/50"
			disabled={page <= 1}
			on:click={() => dispatch('prev')}
			aria-label="Previous page"
		>
			<ChevronLeft size={15} />
		</button>
		<span class="px-2 tabular-nums text-gray-700 font-medium">{page}/{totalPages}</span>
		<button
			class="p-1.5 rounded-xl disabled:opacity-30 disabled:cursor-not-allowed transition-all hover:bg-white/50"
			disabled={page >= totalPages}
			on:click={() => dispatch('next')}
			aria-label="Next page"
		>
			<ChevronRight size={15} />
		</button>
		<button
			class="p-1.5 rounded-xl disabled:opacity-30 disabled:cursor-not-allowed transition-all hover:bg-white/50"
			disabled={page >= totalPages}
			on:click={() => dispatch('last')}
			aria-label="Last page"
		>
			<ChevronsRight size={15} />
		</button>
	</div>
</div>
