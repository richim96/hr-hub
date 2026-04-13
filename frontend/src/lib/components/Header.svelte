<script lang="ts">
	import { Menu } from 'lucide-svelte';
	export let sidebarWidth = 240;
	export let onMenuToggle: () => void = () => {};
	export let sidebarOpen = false;
</script>

<!-- Mobile hamburger (shown only on mobile) -->
<button
	on:click={onMenuToggle}
	class="fixed top-0 left-0 z-30 h-14 px-4 flex items-center md:hidden text-white bg-[#C05B28]
	       {sidebarOpen ? 'hidden' : ''}"
	aria-label="Toggle menu"
>
	<Menu size={20} />
</button>

<!-- Header bar -->
<header
	class="layout-header fixed top-0 right-0 h-14 bg-[#C05B28] z-20"
	style="--sidebar-w: {sidebarWidth}px;"
></header>
