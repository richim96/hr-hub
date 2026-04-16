<script lang="ts">
	import { page } from '$app/stores';
	import { X, User } from 'lucide-svelte';
	import { sendChatMessage, type ChatMessage } from '$lib/api/chat';
	import { modalOpen } from '$lib/stores/ui';

	const GOOMBA_LIGHT = '/goomba_light.png';
	const GOOMBA_DARK = '/goomba_dark.png';

	let open = false;
	let input = '';
	let loading = false;
	let messages: ChatMessage[] = [];
	let chatContainer: HTMLElement;

	$: context = { current_page: $page.url.pathname };

	async function scrollToBottom() {
		await new Promise((r) => requestAnimationFrame(r));
		chatContainer?.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
	}

	async function send() {
		const text = input.trim();
		if (!text || loading) return;

		messages = [...messages, { role: 'user', content: text }];
		input = '';
		loading = true;
		await scrollToBottom();

		try {
			const res = await sendChatMessage({ message: text, context });
			messages = [...messages, { role: 'assistant', content: res.reply }];
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
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			send();
		}
	}

	function toggleOpen() {
		open = !open;
		if (open && messages.length === 0) {
			messages = [
				{
					role: 'assistant',
					content: "Hi! I'm your personal Goomba 🍄‍🟫\nYou can ask me anything about any employee in our Hub.\n⭐️ Go ahead! ⭐️"
				}
			];
		}
	}
</script>

<!-- Floating button -->
<div class="fixed bottom-6 right-6 flex flex-col items-end gap-3 {$modalOpen ? 'z-40 pointer-events-none' : 'z-50'}">
	{#if open}
		<!-- Chat panel -->
		<div
			class="w-80 sm:w-96 bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden animate-slide-in"
			style="height: 480px;"
		>
			<!-- Chat header -->
			<div class="flex items-center justify-between px-4 py-3 bg-[#C05B28] text-white shrink-0">
				<div class="flex items-center gap-2">
					<img src={GOOMBA_DARK} alt="Goomba" class="w-5 h-5 rounded-full object-cover" />
					<span class="font-semibold text-sm">Goomba</span>
				</div>
				<button
					on:click={toggleOpen}
					class="p-1 rounded-lg hover:bg-[#9a3d1a] transition-colors"
					aria-label="Close chat"
				>
					<X size={16} />
				</button>
			</div>

			<!-- Messages -->
			<div bind:this={chatContainer} class="flex-1 overflow-y-auto p-4 space-y-3">
				{#each messages as msg}
					<div class="flex gap-2 {msg.role === 'user' ? 'justify-end' : 'justify-start'}">
						{#if msg.role === 'assistant'}
							<div class="w-6 h-6 rounded-full bg-[#f5ddd0] flex items-center justify-center shrink-0 mt-0.5 overflow-hidden">
								<img src={GOOMBA_LIGHT} alt="assistant" class="w-full h-full object-cover" />
							</div>
						{/if}
						<div
							class="max-w-[75%] px-3 py-2 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap
							       {msg.role === 'user'
								? 'bg-[#C05B28] text-white rounded-br-sm'
								: 'bg-gray-100 text-gray-800 rounded-bl-sm'}"
						>
							{msg.content}
						</div>
						{#if msg.role === 'user'}
							<div class="w-6 h-6 rounded-full bg-gray-200 text-gray-600 flex items-center justify-center shrink-0 mt-0.5">
								<User size={13} />
							</div>
						{/if}
					</div>
				{/each}

				{#if loading}
					<div class="flex gap-2 justify-start">
						<div class="w-6 h-6 rounded-full bg-[#f5ddd0] flex items-center justify-center shrink-0 overflow-hidden">
							<img src={GOOMBA_LIGHT} alt="assistant" class="w-full h-full object-cover" />
						</div>
						<div class="bg-gray-100 px-3 py-2 rounded-2xl rounded-bl-sm">
							<div class="flex gap-1">
								<span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms" />
								<span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms" />
								<span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms" />
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Input area -->
			<div class="px-3 pb-3 pt-2 border-t border-gray-100 shrink-0">
				<div class="flex gap-2 items-end">
					<textarea
						bind:value={input}
						on:keydown={handleKeydown}
						placeholder="Ask about employees, tasks, tickets…"
						rows={1}
						class="flex-1 px-3 py-2 text-sm bg-gray-50 border border-gray-200 rounded-xl resize-none
						       focus:outline-none focus:ring-2 focus:ring-[#C05B28] focus:bg-white
						       max-h-24 transition-colors"
						disabled={loading}
					/>
					<button
						on:click={send}
						disabled={loading || !input.trim()}
						class="p-2.5 bg-[#C05B28] text-white rounded-xl disabled:opacity-40 hover:bg-[#9a3d1a]
						       transition-colors shrink-0"
						aria-label="Send message"
					>
						<img src="/send_star.png" alt="send" class="w-5 h-5 object-contain" />
					</button>
				</div>
				<p class="text-xs text-gray-400 mt-1 text-center">
					Context: {$page.url.pathname}
				</p>
			</div>
		</div>
	{/if}

	<!-- Toggle button -->
	<button
		on:click={toggleOpen}
		class="w-14 h-14 bg-[#C05B28] text-white rounded-full shadow-lg
		       hover:bg-[#9a3d1a] hover:shadow-xl transition-all duration-200
		       flex items-center justify-center overflow-hidden"
		aria-label={open ? 'Close HR Assistant' : 'Open HR Assistant'}
	>
		{#if open}
			<img src={GOOMBA_DARK} alt="close" class="w-8 h-8 object-contain rotate-180" />
		{:else}
			<img src={GOOMBA_DARK} alt="assistant" class="w-8 h-8 object-contain" />
		{/if}
	</button>
</div>
