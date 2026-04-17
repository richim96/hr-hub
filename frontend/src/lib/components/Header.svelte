<script lang="ts">
	import { Menu } from 'lucide-svelte';
	export let sidebarWidth = 240;
	export let onMenuToggle: () => void = () => {};
	export let sidebarOpen = false;
</script>

<!-- Mobile hamburger -->
<button
	on:click={onMenuToggle}
	class="fixed top-0 left-0 z-30 h-14 px-4 flex items-center md:hidden text-gray-700 transition-colors hover:bg-white/30"
	style="background: rgba(255,255,255,0.5); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.5);"
	class:hidden={sidebarOpen}
	aria-label="Toggle menu"
>
	<Menu size={20} />
</button>

<!-- Header bar -->
<header
	class="layout-header fixed top-0 right-0 h-14 z-20"
	style="--sidebar-w: {sidebarWidth}px; background: rgba(255,255,255,0.5); backdrop-filter: blur(24px) saturate(180%); -webkit-backdrop-filter: blur(24px) saturate(180%); border-bottom: 1px solid rgba(255,255,255,0.55); box-shadow: 0 2px 16px rgba(0,0,0,0.06), inset 0 -1px 0 rgba(255,255,255,0.3);"
></header>
