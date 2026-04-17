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
		default: 'rounded-full text-gray-600'
	};

	const defaultStyle =
		'background: rgba(100,116,139,0.12); border: 1px solid rgba(100,116,139,0.25); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);';
</script>

<span class={`${base} ${variants[variant]}`} style={variant === 'default' ? defaultStyle : ''}>
	<slot />
</span>
