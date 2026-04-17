<script lang="ts">
	export let rows = 5;
	export let cols = 6;
</script>

<div class="animate-pulse">
	{#each Array(rows) as _, i}
		<div class="flex gap-4 py-3 {i === 0 ? 'opacity-80' : ''}" style="border-bottom: 1px solid rgba(255,255,255,0.3);">
			{#each Array(cols) as _, _j}
				<div
					class="h-4 rounded-full flex-1"
					style="background: rgba(255,255,255,0.5); width: {60 + Math.random() * 30}%"
				/>
			{/each}
		</div>
	{/each}
</div>
