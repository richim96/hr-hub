<script lang="ts">
	import { page } from '$app/stores';
	import { ChevronLeft, ChevronRight } from 'lucide-svelte';

	export let collapsed = false;

	const navItems = [
		{ href: '/employees', label: 'Employees', img: '/employees.png' },
		{ href: '/tasks', label: 'IT Tasks', img: '/it_tasks.png' },
		{ href: '/tickets', label: 'Tickets', img: '/tickets.png' }
	];

	$: activeIndex = navItems.findIndex((item) => $page.url.pathname.startsWith(item.href));
</script>

<aside
	class="fixed top-0 left-0 h-full flex flex-col z-30 transition-all duration-200 ease-in-out
	       {collapsed ? 'w-[69px]' : 'w-60'}"
	style="background: var(--glass-bg); backdrop-filter: blur(24px) saturate(180%); -webkit-backdrop-filter: blur(24px) saturate(180%); border-right: 1px solid var(--glass-border); box-shadow: 2px 0 16px rgba(0,0,0,0.05);"
>
	<!-- Logo / Brand -->
	<div
		class="flex items-center h-16 shrink-0 px-4 gap-3"
		style="border-bottom: 1px solid var(--glass-border);"
	>
		<img
			src="/home.png" alt="HR Hub"
			class="{collapsed ? 'w-8 h-8' : 'w-10 h-10'} object-contain shrink-0 transition-all duration-200"
		/>
		{#if !collapsed}
			<span class="flex-1 font-semibold text-gray-800 text-lg whitespace-nowrap overflow-hidden tracking-tight">HR Hub</span>
		{/if}
	</div>

	<!-- Collapse toggle — centered on right border of sidebar, vertically in header -->
	<button
		on:click={() => (collapsed = !collapsed)}
		class="absolute p-1.5 rounded-xl transition-all text-gray-500 hover:text-gray-700"
		style="top: 2rem; right: 0; transform: translate(50%, -50%); z-index: 40; background: var(--glass-btn-bg); border: 1px solid var(--glass-btn-border); box-shadow: 0 2px 8px rgba(0,0,0,0.08);"
		aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
	>
		{#if collapsed}
			<ChevronRight size={14} />
		{:else}
			<ChevronLeft size={14} />
		{/if}
	</button>

	<!-- Navigation -->
	<nav class="relative flex-1 py-4 px-2 overflow-y-auto">
		<!-- Sliding active indicator -->
		{#if activeIndex >= 0}
			<div
				class="absolute left-2 right-2 rounded-2xl pointer-events-none"
				style="
					height: 48px;
					top: 16px;
					transform: translateY({activeIndex * 52}px);
					transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
					background: rgba(192,91,40,0.12);
					border: 1px solid rgba(192,91,40,0.2);
					backdrop-filter: blur(8px);
					-webkit-backdrop-filter: blur(8px);
				"
			/>
		{/if}

		{#each navItems as item}
			{@const active = $page.url.pathname.startsWith(item.href)}
			<a
				href={item.href}
				class="relative flex items-center gap-3 py-3 rounded-2xl mb-1 text-sm font-medium transition-colors
				       {collapsed ? 'justify-center' : 'px-3'}
				       {active ? 'text-[#9a3d1a]' : 'text-gray-600 hover:text-gray-900 hover:bg-white/50'}"
				style="z-index: 1;"
				title={collapsed ? item.label : undefined}
			>
				<img src={item.img} alt={item.label} class="w-6 h-6 object-contain shrink-0" />
				{#if !collapsed}
					<span class="whitespace-nowrap text-base">{item.label}</span>
				{/if}
			</a>
		{/each}
	</nav>

	<!-- Glass sheen + light spots overlay -->
	<div
		aria-hidden="true"
		class="absolute bottom-0 left-0 w-full pointer-events-none"
		style="height: calc((100% - 4rem) * 0.8); z-index: 1; opacity: {collapsed ? 0 : 1}; background:
			radial-gradient(circle 22px at 28% 22%, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0.1) 60%, transparent 100%),
			radial-gradient(circle 15px at 42% 15%, rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.08) 60%, transparent 100%),
			radial-gradient(circle 12px at 18% 32%, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0.06) 60%, transparent 100%),
			radial-gradient(circle 16px at 66% 30%, rgba(255,255,255,0.50) 0%, rgba(255,255,255,0.09) 60%, transparent 100%),
			radial-gradient(circle 9px  at 58% 40%, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.05) 60%, transparent 100%);"
	/>
	<!-- Mushroom decoration image -->
	<img
		src="/navbar_decoration.png"
		alt=""
		aria-hidden="true"
		class="absolute bottom-0 left-0 w-full pointer-events-none select-none transition-opacity duration-200"
		style="height: calc((100% - 4rem) * 0.8 - 12px); object-fit: cover; object-position: center bottom; z-index: 0; opacity: {collapsed ? 0.08 : 0.22}; filter: sepia(1) saturate(2.5) hue-rotate(330deg) brightness(0.85); mask-image: linear-gradient(to bottom, rgba(0,0,0,0.60) 0%, black 45%); -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,0.60) 0%, black 45%);"
	/>
</aside>
