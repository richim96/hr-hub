<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Header from '$lib/components/Header.svelte';
	import Toast from '$lib/components/Toast.svelte';
	import ChatWidget from '$lib/components/ChatWidget.svelte';

	let sidebarCollapsed = false;
	let mobileSidebarOpen = false;

	$: sidebarWidth = sidebarCollapsed ? 64 : 240;
	$: $page.url.pathname, (mobileSidebarOpen = false);
</script>

<!-- Mobile overlay -->
{#if mobileSidebarOpen}
	<div
		class="fixed inset-0 bg-black/30 z-20 md:hidden"
		on:click={() => (mobileSidebarOpen = false)}
		role="presentation"
	/>
{/if}

<!-- Sidebar: drawer on mobile, always-on on md+ -->
<div class="{mobileSidebarOpen ? 'block' : 'hidden'} md:block">
	<Sidebar bind:collapsed={sidebarCollapsed} />
</div>

<!-- Header -->
<Header
	onMenuToggle={() => (mobileSidebarOpen = !mobileSidebarOpen)}
	sidebarWidth={sidebarWidth}
	sidebarOpen={mobileSidebarOpen}
/>

<!-- Main content -->
<main
	class="layout-main pt-14 min-h-screen transition-all duration-200"
	style="--sidebar-w: {sidebarWidth}px;"
>
	<div class="p-4 md:p-6">
		<slot />
	</div>
</main>

<!-- Floating chat widget -->
<ChatWidget />

<!-- Toast notifications -->
<Toast />
