<script lang="ts">
	export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
	let extraClass = '';
	export { extraClass as class };
	const paddings = { none: '', sm: 'p-4', md: 'p-6', lg: 'p-8' };
</script>

<div class="glass rounded-3xl {paddings[padding]} {extraClass}">
	<slot />
</div>
