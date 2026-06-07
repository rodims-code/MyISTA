<script lang="ts">
	import { onMount } from 'svelte';
	import {
		fetchConversations,
		fetchMessages,
		sendMessage,
		markConversationSeen,
		searchNetworkUsers,
		createConversation
	} from '$lib/networkApi';
	import { fetchCurrentUser } from '$lib/userApi';
	import { Paperclip, Search, Send, MessageCircle, X } from 'lucide-svelte';

	let currentUser: any = null;
	let conversations: any[] = [];
	let messages: any[] = [];
	let selectedConversation: any = null;
	let isLoading = true;
	let isLoadingMessages = false;
	let isSending = false;
	let content = '';
	let searchQuery = '';
	let userResults: any[] = [];
	let isSearching = false;
	let searchTimer: ReturnType<typeof setTimeout>;
	let fileInput: HTMLInputElement | null = null;
	let selectedFile: File | null = null;

	$: otherParticipant = selectedConversation?.participants_details?.find(
		(user: any) => String(user.id) !== String(currentUser?.id)
	);

	onMount(async () => {
		currentUser = await fetchCurrentUser();
		conversations = await fetchConversations();
		selectedConversation = conversations[0] || null;

		if (selectedConversation) {
			await loadMessages(selectedConversation);
		}

		isLoading = false;
	});

	async function loadMessages(conversation: any) {
		selectedConversation = conversation;
		isLoadingMessages = true;
		messages = await fetchMessages(conversation.id);
		isLoadingMessages = false;

		try {
			await markConversationSeen(conversation.id);
			conversations = conversations.map((item) =>
				item.id === conversation.id ? { ...item, unread_count: 0 } : item
			);
		} catch (error) {
			console.error('Erreur lecture conversation:', error);
		}
	}

	function handleFileChange(event: Event) {
		const target = event.target as HTMLInputElement;
		selectedFile = target.files?.[0] || null;
	}

	async function handleSendMessage() {
		if (!selectedConversation || (!content.trim() && !selectedFile)) return;

		const formData = new FormData();
		formData.append('content', content.trim());
		if (selectedFile) formData.append('fichier', selectedFile);

		isSending = true;
		try {
			const newMessage = await sendMessage(selectedConversation.id, formData);
			messages = [...messages, newMessage];
			content = '';
			selectedFile = null;
			if (fileInput) fileInput.value = '';
			conversations = await fetchConversations();
		} catch (error) {
			console.error('Erreur envoi message:', error);
		}
		isSending = false;
	}

	function handleSearchInput() {
		clearTimeout(searchTimer);

		if (searchQuery.trim().length < 2) {
			userResults = [];
			isSearching = false;
			return;
		}

		isSearching = true;
		searchTimer = setTimeout(async () => {
			userResults = await searchNetworkUsers(searchQuery);
			isSearching = false;
		}, 250);
	}

	async function startConversation(userId: string | number) {
		try {
			const conversation = await createConversation(userId);
			const exists = conversations.some((item) => item.id === conversation.id);
			conversations = exists ? conversations : [conversation, ...conversations];
			searchQuery = '';
			userResults = [];
			await loadMessages(conversation);
		} catch (error) {
			console.error('Erreur création conversation:', error);
		}
	}

	function formatTime(dateString: string) {
		return new Date(dateString).toLocaleTimeString('fr-FR', {
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<div class="grid h-full min-h-[620px] gap-4 lg:grid-cols-[320px_1fr]">
	<section class="flex min-h-0 flex-col rounded-2xl border border-base-200 bg-base-100">
		<div class="border-b border-base-200 p-4">
			<h1 class="text-2xl font-bold">Messages</h1>
			<p class="text-sm text-base-content/60">Discussions privées du campus.</p>

			<label class="input-bordered input mt-4 w-full rounded-full">
				<Search size={18} class="opacity-50" />
				<input
					type="search"
					class="grow"
					placeholder="Chercher un étudiant..."
					bind:value={searchQuery}
					oninput={handleSearchInput}
				/>
				{#if searchQuery}
					<button
						class="btn btn-circle btn-ghost btn-xs"
						onclick={() => {
							searchQuery = '';
							userResults = [];
						}}
						aria-label="Effacer"
					>
						<X size={14} />
					</button>
				{/if}
			</label>
		</div>

		{#if searchQuery}
			<div class="border-b border-base-200 p-2">
				{#if isSearching}
					<div class="flex justify-center py-4">
						<span class="loading loading-sm loading-spinner text-primary"></span>
					</div>
				{:else if userResults.length === 0}
					<p class="px-3 py-4 text-sm text-base-content/50">Aucun profil trouvé.</p>
				{:else}
					{#each userResults as user}
						<button
							class="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left hover:bg-base-200"
							onclick={() => startConversation(user.id)}
						>
							<div class="placeholder avatar">
								<div class="h-10 w-10 rounded-full bg-primary text-primary-content">
									<span>{user.username?.charAt(0).toUpperCase() || 'U'}</span>
								</div>
							</div>
							<div class="min-w-0 flex-1">
								<p class="truncate text-sm font-bold">{user.username}</p>
								<p class="truncate text-xs text-base-content/50">{user.filiere || 'ISTA'}</p>
							</div>
						</button>
					{/each}
				{/if}
			</div>
		{/if}

		<div class="min-h-0 flex-1 overflow-y-auto p-2">
			{#if isLoading}
				<div class="flex justify-center py-10">
					<span class="loading loading-spinner text-primary"></span>
				</div>
			{:else if conversations.length === 0}
				<div class="grid h-full place-items-center px-6 text-center text-base-content/50">
					<div>
						<MessageCircle class="mx-auto mb-3" size={36} />
						<p>Aucune conversation.</p>
					</div>
				</div>
			{:else}
				{#each conversations as conversation}
					{@const participant = conversation.participants_details?.find(
						(user: any) => String(user.id) !== String(currentUser?.id)
					)}
					<button
						class="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left hover:bg-base-200 {selectedConversation?.id ===
						conversation.id
							? 'bg-primary/10'
							: ''}"
						onclick={() => loadMessages(conversation)}
					>
						<div class="placeholder avatar">
							<div class="h-11 w-11 rounded-full bg-secondary text-secondary-content">
								<span>{participant?.username?.charAt(0).toUpperCase() || 'M'}</span>
							</div>
						</div>
						<div class="min-w-0 flex-1">
							<div class="flex items-center justify-between gap-2">
								<p class="truncate text-sm font-bold">{participant?.username || 'Conversation'}</p>
								{#if conversation.unread_count > 0}
									<span class="badge badge-sm badge-primary">{conversation.unread_count}</span>
								{/if}
							</div>
							<p class="truncate text-xs text-base-content/50">
								{conversation.last_message?.content || 'Nouveau fil de discussion'}
							</p>
						</div>
					</button>
				{/each}
			{/if}
		</div>
	</section>

	<section class="flex min-h-0 flex-col rounded-2xl border border-base-200 bg-base-100">
		{#if selectedConversation}
			<div class="flex items-center gap-3 border-b border-base-200 p-4">
				<div class="placeholder avatar">
					<div class="h-11 w-11 rounded-full bg-primary text-primary-content">
						<span>{otherParticipant?.username?.charAt(0).toUpperCase() || 'M'}</span>
					</div>
				</div>
				<div>
					<h2 class="font-bold">{otherParticipant?.username || 'Conversation'}</h2>
					<p class="text-xs text-base-content/50">{otherParticipant?.filiere || 'MyISTA'}</p>
				</div>
			</div>

			<div class="min-h-0 flex-1 space-y-3 overflow-y-auto bg-base-200/40 p-4">
				{#if isLoadingMessages}
					<div class="flex justify-center py-10">
						<span class="loading loading-spinner text-primary"></span>
					</div>
				{:else if messages.length === 0}
					<div class="grid h-full place-items-center text-center text-base-content/50">
						<p>Démarrez la conversation.</p>
					</div>
				{:else}
					{#each messages as message}
						{@const mine = String(message.sender) === String(currentUser?.id)}
						<div class="chat {mine ? 'chat-end' : 'chat-start'}">
							<div
								class="chat-bubble {mine ? 'chat-bubble-primary' : 'bg-base-100 text-base-content'}"
							>
								{#if message.content}
									<p class="whitespace-pre-wrap">{message.content}</p>
								{/if}
								{#if message.fichier}
									<a class="mt-2 block link text-xs" href={message.fichier} target="_blank"
										>Pièce jointe</a
									>
								{/if}
							</div>
							<div class="chat-footer opacity-60">{formatTime(message.created_at)}</div>
						</div>
					{/each}
				{/if}
			</div>

			<div class="border-t border-base-200 p-4">
				{#if selectedFile}
					<div
						class="mb-2 flex items-center justify-between rounded-xl bg-base-200 px-3 py-2 text-sm"
					>
						<span class="truncate">{selectedFile.name}</span>
						<button class="btn btn-circle btn-ghost btn-xs" onclick={() => (selectedFile = null)}>
							<X size={14} />
						</button>
					</div>
				{/if}

				<div class="flex items-end gap-2">
					<input type="file" class="hidden" bind:this={fileInput} onchange={handleFileChange} />
					<button
						class="btn btn-circle btn-ghost"
						onclick={() => fileInput?.click()}
						aria-label="Joindre"
					>
						<Paperclip size={20} />
					</button>
					<textarea
						class="textarea-bordered textarea min-h-12 flex-1 resize-none rounded-2xl"
						rows="1"
						placeholder="Message..."
						bind:value={content}
						onkeydown={(event) => {
							if (event.key === 'Enter' && !event.shiftKey) {
								event.preventDefault();
								handleSendMessage();
							}
						}}
					></textarea>
					<button
						class="btn btn-circle btn-primary"
						onclick={handleSendMessage}
						disabled={isSending || (!content.trim() && !selectedFile)}
						aria-label="Envoyer"
					>
						{#if isSending}
							<span class="loading loading-xs loading-spinner"></span>
						{:else}
							<Send size={18} />
						{/if}
					</button>
				</div>
			</div>
		{:else}
			<div class="grid h-full place-items-center px-6 text-center text-base-content/50">
				<div>
					<MessageCircle class="mx-auto mb-3" size={44} />
					<h2 class="text-lg font-bold text-base-content">Vos messages</h2>
					<p>Choisissez une conversation ou cherchez un étudiant.</p>
				</div>
			</div>
		{/if}
	</section>
</div>
