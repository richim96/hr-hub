<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from './Modal.svelte';
	import Button from './Button.svelte';

	export let open = false;
	export let title = 'Confirm';
	export let message = 'Are you sure? This action cannot be undone.';
	export let confirmLabel = 'Delete';
	export let loading = false;

	const dispatch = createEventDispatcher<{ confirm: void; cancel: void }>();
</script>

<Modal {open} {title} maxWidth="sm" on:close={() => dispatch('cancel')}>
	<p class="text-gray-700">{message}</p>

	<svelte:fragment slot="footer">
		<Button variant="secondary" on:click={() => dispatch('cancel')} disabled={loading}>
			Cancel
		</Button>
		<Button variant="danger" on:click={() => dispatch('confirm')} {loading}>
			{confirmLabel}
		</Button>
	</svelte:fragment>
</Modal>
