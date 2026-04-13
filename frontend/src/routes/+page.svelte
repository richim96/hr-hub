<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		goto('/employees');
	});
</script>

<!-- Redirecting to /employees -->
<div class="flex items-center justify-center h-full text-gray-500 text-sm">
	Redirecting…
</div>
