<script lang="ts">
	export let variant: 'primary' | 'secondary' | 'danger' | 'ghost' = 'primary';
	export let size: 'sm' | 'md' | 'lg' = 'md';
	export let type: 'button' | 'submit' | 'reset' = 'button';
	export let disabled = false;
	export let loading = false;

	const base =
		'inline-flex items-center justify-center gap-2 font-medium rounded-2xl transition-all focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed';

	const variants = {
		primary:
			'text-white focus:ring-[#C05B28] shadow-sm hover:brightness-110 active:scale-[0.98]',
		secondary:
			'glass text-gray-700 hover:bg-white/70 focus:ring-[#C05B28]',
		danger:
			'text-white focus:ring-red-400 shadow-sm hover:brightness-110 active:scale-[0.98]',
		ghost:
			'text-gray-600 hover:bg-white/50 focus:ring-gray-400 backdrop-blur-sm'
	};

	const sizes = {
		sm: 'px-3 py-1.5 text-sm',
		md: 'px-4 py-2 text-sm',
		lg: 'px-5 py-2.5 text-base'
	};

	const inlineStyles = {
		primary: 'background: var(--btn-primary-bg); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.25); box-shadow: var(--btn-primary-shadow);',
		secondary: '',
		danger: 'background: var(--btn-danger-bg); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.2); box-shadow: var(--btn-danger-shadow);',
		ghost: ''
	};

	$: cls = `${base} ${variants[variant]} ${sizes[size]}`;
</script>

<button
	{type}
	{disabled}
	class={`${cls} ${$$restProps.class ?? ''}`}
	style={inlineStyles[variant]}
	on:click
	{...$$restProps}
>
	{#if loading}
		<svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
			<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
			/>
		</svg>
	{/if}
	<slot />
</button>
