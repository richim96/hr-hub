<script lang="ts">
	export let variant: 'completed' | 'pending' | 'failed' | 'canceled' | 'info' | 'default' =
		'default';

	const base = 'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium';

	const variants = {
		completed: 'badge-completed',
		pending: 'badge-pending',
		failed: 'badge-failed',
		canceled: 'badge-canceled',
		info: 'badge-info',
		default: 'bg-gray-100 text-gray-700 border border-gray-200'
	};
</script>

<span class={`${base} ${variants[variant]}`}>
	<slot />
</span>
