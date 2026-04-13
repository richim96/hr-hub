<script lang="ts">
	export let rows = 5;
	export let cols = 6;
</script>

<div class="animate-pulse">
	<!-- Table skeleton -->
	{#each Array(rows) as _, i}
		<div class="flex gap-4 py-3 border-b border-gray-100 {i === 0 ? 'opacity-80' : ''}">
			{#each Array(cols) as _, j}
				<div
					class="h-4 bg-gray-200 rounded flex-1"
					style="width: {60 + Math.random() * 30}%"
				/>
			{/each}
		</div>
	{/each}
</div>
