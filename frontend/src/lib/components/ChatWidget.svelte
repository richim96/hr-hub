<script lang="ts">
	import { page } from '$app/state';
	import { tick } from 'svelte';
	import { X, User, Maximize2, Minimize2 } from 'lucide-svelte';
	import { marked } from 'marked';
	import { sendChatMessage, type ChatMessage } from '$lib/api/chat';
	import { modalOpen } from '$lib/stores/ui';
	import { randomUUID } from '$lib/utils';
	import { darkMode } from '$lib/stores/darkMode';

	$: panelBg = $darkMode
		? 'background: rgba(32,38,68,0.88); backdrop-filter: blur(32px) saturate(160%); -webkit-backdrop-filter: blur(32px) saturate(160%); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 24px 64px rgba(0,0,0,0.5), 0 8px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.08);'
		: 'background: rgba(255,255,255,0.6); backdrop-filter: blur(32px) saturate(200%); -webkit-backdrop-filter: blur(32px) saturate(200%); border: 1px solid rgba(255,255,255,0.7); box-shadow: 0 24px 64px rgba(0,0,0,0.14), 0 8px 24px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.95);';

	$: assistantBubbleBg = $darkMode
		? 'background: rgba(30,35,60,0.8); backdrop-filter: blur(24px) saturate(160%); -webkit-backdrop-filter: blur(24px) saturate(160%); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 16px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.06);'
		: 'background: rgba(245,224,210,0.55); backdrop-filter: blur(24px) saturate(180%); -webkit-backdrop-filter: blur(24px) saturate(180%); border: 1px solid rgba(255,255,255,0.35); box-shadow: 0 8px 32px rgba(192,91,40,0.35), 0 2px 8px rgba(192,91,40,0.25), inset 0 1px 0 rgba(255,255,255,0.4), inset 0 -1px 0 rgba(0,0,0,0.04);';

	$: inputBg = $darkMode
		? 'background: rgba(20,25,50,0.75); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); color: #e2e8f0;'
		: 'background: rgba(255,255,255,0.45); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.5);';

	$: inputAreaBg = $darkMode
		? 'border-top: 1px solid rgba(255,255,255,0.08);'
		: 'border-top: 1px solid rgba(255,255,255,0.4);';

	$: loadingBubbleBg = $darkMode
		? 'background: rgba(30,35,60,0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1);'
		: 'background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.6);';

	$: avatarBg = $darkMode
		? 'background: rgba(30,35,60,0.8); border: 1px solid rgba(255,255,255,0.1);'
		: 'background: rgba(245,221,208,0.8); border: 1px solid rgba(255,255,255,0.6);';

	$: userAvatarBg = $darkMode
		? 'background: rgba(30,35,60,0.8); border: 1px solid rgba(255,255,255,0.1);'
		: 'background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.6);';

	$: brandSurface = $darkMode
		? 'rgba(155,68,24,0.72)'
		: 'rgba(192,91,40,0.85)';

	$: brandGlow = $darkMode
		? '0 8px 24px rgba(0,0,0,0.35)'
		: '0 8px 24px rgba(192,91,40,0.4)';

	$: chatHeaderStyle = $darkMode
		? 'background: rgba(155,68,24,0.72); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.1); box-shadow: inset 0 1px 0 rgba(255,255,255,0.1);'
		: 'background: rgba(192,91,40,0.75); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,0.3); box-shadow: inset 0 1px 0 rgba(255,255,255,0.25);';

	$: userBubbleStyle = $darkMode
		? 'background: rgba(155,68,24,0.72); backdrop-filter: blur(24px) saturate(160%); -webkit-backdrop-filter: blur(24px) saturate(160%); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 4px 16px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);'
		: 'background: rgba(192,91,40,0.85); backdrop-filter: blur(24px) saturate(180%); -webkit-backdrop-filter: blur(24px) saturate(180%); border: 1px solid rgba(255,255,255,0.35); box-shadow: 0 8px 32px rgba(192,91,40,0.2), 0 2px 8px rgba(192,91,40,0.15), inset 0 1px 0 rgba(255,255,255,0.4), inset 0 -1px 0 rgba(0,0,0,0.08);';

	$: sendBtnStyle = $darkMode
		? 'background: rgba(155,68,24,0.72); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 4px 12px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);'
		: 'background: rgba(192,91,40,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 4px 12px rgba(192,91,40,0.3), inset 0 1px 0 rgba(255,255,255,0.25);';

	$: tooltipStyle = $darkMode
		? 'background: rgba(130,55,18,0.88); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.12); box-shadow: 0 4px 12px rgba(0,0,0,0.3);'
		: 'background: rgba(192,91,40,0.95); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 4px 12px rgba(0,0,0,0.2);';

	const GOOMBA = '/goomba.png';

	let open = false;
	let expanded = false;
	let input = '';
	let loading = false;
	let messages: ChatMessage[] = [];
	let chatContainer: HTMLElement;
	let textarea: HTMLTextAreaElement;
	let widgetRoot: HTMLElement;

	$: context = { current_page: page.url.pathname };

	async function scrollToBottom() {
		await new Promise((r) => requestAnimationFrame(r));
		chatContainer?.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
	}

	async function send() {
		const text = input.trim();
		if (!text || loading) return;

		// Capture history before pushing the current message
		const history = messages
			.slice(1)
			.filter((_, i, arr) => !(arr[i].role === 'assistant' && (i === 0 || arr[i - 1].role === 'assistant')))
			.map(({ role, content }) => ({ role, content }));

		messages = [...messages, { role: 'user', content: text }];
		input = '';
		if (textarea) { textarea.style.height = 'auto'; }
		loading = true;
		await scrollToBottom();

		try {
			const request_id = `req_${randomUUID()}`;
			const res = await sendChatMessage({ message: text, history, context, request_id });
			messages = [...messages, { role: 'assistant', content: res.answer }];
		} catch (err) {
			const msg =
				err instanceof Error && err.message.includes('404')
					? 'The chat endpoint is not yet available on the backend. Please check back later.'
					: err instanceof Error
						? err.message
						: 'Something went wrong. Please try again.';
			messages = [...messages, { role: 'assistant', content: msg }];
		}

		loading = false;
		await scrollToBottom();
		if (!expanded) await checkOverflow();
	}

	async function checkOverflow() {
		await tick();
		if (chatContainer && chatContainer.scrollWidth > chatContainer.clientWidth) {
			expanded = true;
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			send();
		}
	}

	function handleDocumentMouseDown(e: MouseEvent) {
		if (open && widgetRoot && !widgetRoot.contains(e.target as Node)) open = false;
	}

	function toggleOpen() {
		open = !open;
		if (open && messages.length === 0) {
			messages = [
				{
					role: 'assistant',
					content: "Goomba reporting for duty.\nYou can ask me anything about the employees in my Hub.\nGo ahead ⭐️"
				}
			];
		}
	}
</script>

<!-- Floating button -->
<svelte:window on:mousedown={handleDocumentMouseDown} />
<div
	bind:this={widgetRoot}
	class="fixed bottom-6 right-6 flex flex-col items-end gap-3 {$modalOpen ? 'z-40 pointer-events-none' : 'z-50'}"
>
	{#if open}
		<!-- Chat panel -->
		<div
			class="flex flex-col overflow-hidden animate-slide-in rounded-3xl transition-all duration-300 {expanded ? 'w-[620px] sm:w-[684px]' : 'w-80 sm:w-96'}"
			style="height: {expanded ? 580 : 480}px; {panelBg}"
		>
			<!-- Chat header -->
			<div
				class="flex items-center justify-between px-4 py-3 shrink-0"
				style="{chatHeaderStyle}"
			>
				<div class="flex items-center gap-2">
					<span class="font-bold text-sm text-white tracking-tight">Ask Goomba</span>
				</div>
				<div class="flex items-center gap-1">
					<button
						on:click={() => (expanded = !expanded)}
						class="p-1 rounded-xl transition-colors text-white/80 hover:text-white hover:bg-white/20"
						aria-label={expanded ? 'Collapse chat' : 'Expand chat'}
					>
						{#if expanded}
							<Minimize2 size={16} />
						{:else}
							<Maximize2 size={16} />
						{/if}
					</button>
					<button
						on:click={toggleOpen}
						class="p-1 rounded-xl transition-colors text-white/80 hover:text-white hover:bg-white/20"
						aria-label="Close chat"
					>
						<X size={16} />
					</button>
				</div>
			</div>

			<!-- Messages -->
			<div bind:this={chatContainer} class="flex-1 overflow-y-auto p-4 space-y-3">
				{#each messages as msg}
					<div class="flex gap-2 {msg.role === 'user' ? 'justify-end' : 'justify-start'}">
						{#if msg.role === 'assistant'}
							<div class="w-12 h-12 rounded-full shrink-0 overflow-hidden self-end" style="{avatarBg}">
								<img src={GOOMBA} alt="assistant" class="w-full h-full object-cover" style="transform: translate(-0.2px, -1.5px);" />
							</div>
						{/if}
						<div
							class="max-w-[75%] px-3 py-2 rounded-2xl text-sm leading-relaxed
							       {msg.role === 'user'
								? 'text-white rounded-br-sm whitespace-pre-wrap'
								: 'text-gray-800 rounded-bl-sm prose prose-sm prose-neutral max-w-none'}"
							style={msg.role === 'user' ? userBubbleStyle : assistantBubbleBg}
						>
							{#if msg.role === 'assistant'}
									<!-- eslint-disable-next-line svelte/no-at-html-tags -->
								{@html marked(msg.content)}
							{:else}
								{msg.content}
							{/if}
						</div>
						{#if msg.role === 'user'}
							<div class="w-12 h-12 rounded-full text-gray-600 flex items-center justify-center shrink-0 mt-0.5" style="{userAvatarBg}">
								<User size={20} />
							</div>
						{/if}
					</div>
				{/each}

				{#if loading}
					<div class="flex gap-2 justify-start">
						<div class="w-12 h-12 rounded-full shrink-0 overflow-hidden" style="{avatarBg}">
							<img src={GOOMBA} alt="assistant" class="w-full h-full object-cover" />
						</div>
						<div class="px-3 py-2 rounded-2xl rounded-bl-sm" style="{loadingBubbleBg}">
							<div class="flex gap-1">
								<span class="w-1.5 h-1.5 rounded-full animate-bounce" style="background: rgba(0,0,0,0.25); animation-delay: 0ms" />
								<span class="w-1.5 h-1.5 rounded-full animate-bounce" style="background: rgba(0,0,0,0.25); animation-delay: 150ms" />
								<span class="w-1.5 h-1.5 rounded-full animate-bounce" style="background: rgba(0,0,0,0.25); animation-delay: 300ms" />
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Input area -->
			<div class="px-3 pb-3 pt-2 shrink-0" style="{inputAreaBg}">
				<div class="flex gap-2 items-end">
					<textarea
						bind:this={textarea}
						bind:value={input}
						on:keydown={handleKeydown}
						on:input={(e) => { const t = e.currentTarget; t.style.height = 'auto'; t.style.height = t.scrollHeight + 'px'; }}
						placeholder="Ask about employees, tasks, tickets…"
						rows={1}
						class="flex-1 px-3 py-2 text-sm rounded-2xl resize-none
						       focus:outline-none focus:ring-2 focus:ring-[#C05B28]/50
						       max-h-48 transition-all overflow-y-auto"
						style="{inputBg}"
						disabled={loading}
					/>
					<button
						on:click={send}
						disabled={loading || !input.trim()}
						class="p-2.5 rounded-2xl disabled:opacity-40 transition-all shrink-0 hover:brightness-110 active:scale-95"
						style="{sendBtnStyle}"
						aria-label="Send message"
					>
						<img src="/send_star.png" alt="send" class="w-5 h-5 object-contain" />
					</button>
				</div>
				<p class="text-xs text-gray-400 mt-1 text-center">
					Context: {page.url.pathname}
				</p>
			</div>
		</div>
	{/if}

	<!-- Toggle button -->
	<button
		on:click={toggleOpen}
		class="group relative w-16 h-16 rounded-full transition-all duration-200 flex items-center justify-center overflow-visible hover:brightness-110 hover:scale-105 active:scale-95"
		style="background: {brandSurface}; backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.25); box-shadow: {brandGlow}, inset 0 1px 0 rgba(255,255,255,0.2);"
		aria-label={open ? 'Close HR Assistant' : 'Open HR Assistant'}
	>
		<div class="w-full h-full rounded-full overflow-hidden flex items-center justify-center">
			<img src={GOOMBA} alt="assistant" class="w-16 h-16 object-contain pointer-events-none" style="margin-bottom: 5px; margin-right: 2px;" />
		</div>
		{#if !open}
			<span
				class="absolute -top-1 -left-1 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold leading-none text-white"
				style="background: rgba(255,255,255,0.55); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1.5px solid rgba(255,255,255,0.85); box-shadow: 0 2px 8px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.6); color: rgba(192,91,40,1);"
			>?</span>
		{/if}
		<span
			class="pointer-events-none absolute bottom-full right-0 mb-2 px-2 py-1 rounded-lg text-xs font-medium text-white whitespace-nowrap transition-opacity duration-150 {open ? 'opacity-0' : 'opacity-0 group-hover:opacity-100'}"
			style="{tooltipStyle}"
		>Ask, and I shall answer</span>
	</button>
</div>
