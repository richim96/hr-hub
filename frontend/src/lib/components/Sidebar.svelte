<script lang="ts">
	import { page } from '$app/stores';
	import { ChevronLeft, ChevronRight } from 'lucide-svelte';

	export let collapsed = false;

	const navItems = [
		{ href: '/employees', label: 'Employees', img: '/employees.png' },
		{ href: '/tasks', label: 'IT Tasks', img: '/it_tasks.png' },
		{ href: '/tickets', label: 'Tickets', img: '/tickets.png' }
	];
</script>

<aside
	class="fixed top-0 left-0 h-full bg-white border-r border-gray-200 flex flex-col z-30 transition-all duration-200 ease-in-out
	       {collapsed ? 'w-16' : 'w-60'}"
>
	<!-- Logo / Brand + collapse toggle -->
	<div class="flex items-center gap-2 px-3 h-14 border-b border-gray-100 shrink-0">
		<div class="w-8 h-8 rounded-lg shrink-0 overflow-hidden">
			<img src="/home.png" alt="HR Hub" class="w-full h-full object-cover" />
		</div>
		{#if !collapsed}
			<span class="flex-1 font-semibold text-gray-900 text-sm whitespace-nowrap overflow-hidden">HR Hub</span>
		{/if}
		<button
			on:click={() => (collapsed = !collapsed)}
			class="ml-auto p-1.5 rounded-lg transition-colors shrink-0
			       {collapsed
					? 'bg-gray-100 text-gray-600 hover:bg-gray-200'
					: 'text-gray-500 hover:text-gray-600 hover:bg-gray-100'}"
			aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
		>
			{#if collapsed}
				<ChevronRight size={16} />
			{:else}
				<ChevronLeft size={16} />
			{/if}
		</button>
	</div>

	<!-- Navigation -->
	<nav class="flex-1 py-4 px-2 overflow-y-auto">
		{#each navItems as item}
			{@const active = $page.url.pathname.startsWith(item.href)}
			<a
				href={item.href}
				class="flex items-center gap-3 px-3 py-2.5 rounded-lg mb-1 text-sm font-medium transition-colors
				       {active
					? 'bg-[#fdf4ef] text-[#9a3d1a]'
					: collapsed
						? 'text-gray-400 hover:bg-[#C05B28] hover:text-white'
						: 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'}"
				title={collapsed ? item.label : undefined}
			>
				<img src={item.img} alt={item.label} class="w-5 h-5 object-contain shrink-0" />
				{#if !collapsed}
					<span class="whitespace-nowrap">{item.label}</span>
				{/if}
			</a>
		{/each}
	</nav>
</aside>
