<script lang="ts">
	import { Menu, Sun, Moon } from 'lucide-svelte';
	import { darkMode } from '$lib/stores/darkMode';
	export let sidebarWidth = 240;
	export let onMenuToggle: () => void = () => {};
	export let sidebarOpen = false;
</script>

<!-- Mobile hamburger -->
<button
	on:click={onMenuToggle}
	class="fixed top-0 left-0 z-30 h-14 px-4 flex items-center md:hidden text-gray-700 transition-colors"
	style="background: var(--glass-bg); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-right: 1px solid var(--glass-border);"
	class:hidden={sidebarOpen}
	aria-label="Toggle menu"
>
	<Menu size={20} />
</button>

<!-- Header bar -->
<header
	class="layout-header fixed top-0 right-0 h-14 z-20 flex items-center justify-end px-4"
	style="--sidebar-w: {sidebarWidth}px; background: var(--glass-bg); backdrop-filter: blur(24px) saturate(180%); -webkit-backdrop-filter: blur(24px) saturate(180%); border-bottom: 1px solid var(--glass-border); box-shadow: 0 2px 16px rgba(0,0,0,0.06);"
>
	<button
		on:click={() => darkMode.update((v) => !v)}
		on:mousedown|stopPropagation
		class="p-2 rounded-xl text-gray-600 transition-all hover:text-gray-900"
		style="background: var(--glass-btn-bg); border: 1px solid var(--glass-btn-border);"
		aria-label="Toggle dark mode"
	>
		{#if $darkMode}
			<Sun size={18} />
		{:else}
			<Moon size={18} />
		{/if}
	</button>
</header>
