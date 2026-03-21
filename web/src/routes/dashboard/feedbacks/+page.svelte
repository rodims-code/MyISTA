<script lang="ts">
	import { onMount } from 'svelte';
	import api from '$lib/index';
	import { fetchCurrentUser } from '$lib/userApi';
	import { Send, Trash2, CheckCircle, XCircle, Eye, MessageSquare, Plus } from 'lucide-svelte';

	let feedbacks = $state<any[]>([]);
	let loading = $state(true);
	let currentUser = $state<any>(null);
	let showReplyModal = $state(false);
	let selectedFeedback = $state<any>(null);
	let replyText = $state('');

	let showNewFeedbackModal = $state(false);
	let newFeedbackSujet = $state('');
	let newFeedbackMessage = $state('');

	onMount(async () => {
		try {
			currentUser = await fetchCurrentUser();
			const res = await api.get('/api/feedbacks/');
			feedbacks = res.data;
		} catch (error) {
			console.error('Error fetching feedbacks:', error);
		} finally {
			loading = false;
		}
	});

	let isSubmitting = $state(false);
	let submitError = $state('');

	async function submitFeedback() {
		if (!newFeedbackSujet.trim() || !newFeedbackMessage.trim()) return;
		isSubmitting = true;
		submitError = '';

		try {
			await api.post('/api/feedbacks/', {
				sujet: newFeedbackSujet,
				message: newFeedbackMessage
			});
			const res = await api.get('/api/feedbacks/');
			feedbacks = res.data;
			showNewFeedbackModal = false;
			newFeedbackSujet = '';
			newFeedbackMessage = '';
		} catch (error: any) {
			console.error('Error submitting feedback:', error);
			if (error.response?.data) {
				const errorMsgs = [];
				for (const [key, value] of Object.entries(error.response.data)) {
					errorMsgs.push(`${key}: ${Array.isArray(value) ? value.join(', ') : value}`);
				}
				submitError = errorMsgs.join(' | ');
			} else {
				submitError = "Une erreur est survenue lors de l'envoi.";
			}
		} finally {
			isSubmitting = false;
		}
	}

	async function handleReply(feedback: any) {
		selectedFeedback = feedback;
		replyText = '';
		showReplyModal = true;
	}

	async function sendReply() {
		if (!selectedFeedback || !replyText.trim()) return;

		try {
			await api.post(`/api/feedbacks/${selectedFeedback.id}/reply/`, {
				reponse: replyText
			});
			// Refresh feedbacks
			const res = await api.get('/api/feedbacks/');
			feedbacks = res.data;
			showReplyModal = false;
			selectedFeedback = null;
		} catch (error) {
			console.error('Error sending reply:', error);
		}
	}

	async function deleteFeedback(id: number) {
		if (confirm('Êtes-vous sûr de vouloir supprimer ce feedback ?')) {
			try {
				await api.delete(`/api/feedbacks/${id}/`);
				feedbacks = feedbacks.filter((f) => f.id !== id);
			} catch (error) {
				console.error('Error deleting feedback:', error);
			}
		}
	}

	function getStatusClass(status: string) {
		switch (status) {
			case 'repondu':
			case 'approuve':
				return 'badge-success';
			case 'en_attente':
				return 'badge-warning';
			case 'rejete':
				return 'badge-error';
			default:
				return 'badge-info';
		}
	}

	function getStatusText(status: string) {
		switch (status) {
			case 'repondu':
				return 'Répondu';
			case 'approuve':
				return 'Approuvé';
			case 'en_attente':
				return 'En attente';
			case 'rejete':
				return 'Rejeté';
			default:
				return status;
		}
	}
</script>

<div class="flex flex-col gap-6">
	<div class="flex justify-between items-end">
		<div class="flex flex-col gap-2">
			<h1 class="text-3xl font-bold text-base-content">Feedbacks & Aide</h1>
			<p class="text-base-content/60">Gérez les feedbacks et demandes d'aide de myISTA</p>
		</div>
		{#if currentUser?.role === 'student'}
			<button class="btn btn-primary" onclick={() => showNewFeedbackModal = true}>
				<Plus size={18} class="mr-2" />
				Nouveau Feedback
			</button>
		{/if}
	</div>

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<span class="loading loading-spinner loading-lg text-primary"></span>
		</div>
	{:else if feedbacks.length === 0}
		<div class="card bg-base-100 shadow-sm border border-base-200">
			<div class="card-body items-center text-center">
				<div class="p-4 bg-base-200 rounded-full">
					<MessageSquare size={40} class="text-base-content/30" />
				</div>
				<h2 class="card-title">Aucun feedback</h2>
				<p class="text-base-content/60">
					{#if currentUser?.role === 'student'}
						Vous n'avez soumis aucun feedback.
					{:else}
						Aucun feedback n'a été reçu pour le moment.
					{/if}
				</p>
			</div>
		</div>
	{:else}
		<div class="overflow-x-auto bg-base-100 rounded-box shadow-sm border border-base-200">
			<table class="table table-zebra">
				<thead>
					<tr>
						<th>Sujet</th>
						<th>Message</th>
						<th>Statut</th>
						<th>Date</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each feedbacks as feedback}
						<tr class="hover:bg-base-200/50">
							<td class="font-semibold">{feedback.sujet}</td>
							<td class="max-w-xs">
								<div class="truncate">{feedback.message}</div>
							</td>
							<td>
								<span class="badge {getStatusClass(feedback.statut)}">
									{getStatusText(feedback.statut)}
								</span>
							</td>
							<td>{new Date(feedback.date_soumission).toLocaleDateString()}</td>
							<td class="flex gap-2">
								{#if currentUser && currentUser.role !== 'student'}
									<button
										class="btn btn-sm btn-ghost btn-circle"
										onclick={() => handleReply(feedback)}
										title="Répondre"
									>
										<Send size={16} />
									</button>
									<button
										class="btn btn-sm btn-ghost btn-circle text-error"
										onclick={() => deleteFeedback(feedback.id)}
										title="Supprimer"
									>
										<Trash2 size={16} />
									</button>
								{:else if currentUser && currentUser.role === 'student' && feedback.statut === 'repondu'}
                                    <button
                                        class="btn btn-sm btn-ghost btn-circle text-info"
                                        onclick={() => { selectedFeedback = feedback; showReplyModal = true; }}
                                        title="Voir la réponse"
                                    >
                                        <Eye size={16} />
                                    </button>
								{/if}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>

<!-- Modal Réponse / Détail -->
{#if showReplyModal && selectedFeedback}
	<div class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg mb-4">
				{#if currentUser?.role !== 'student'}
					Répondre au feedback
				{:else}
					Détails du feedback
				{/if}
			</h3>
			
			<div class="mb-4 bg-base-200 p-4 rounded-lg">
				<p class="font-semibold text-sm opacity-70 mb-1">Sujet :</p>
				<p class="mb-3">{selectedFeedback.sujet}</p>
				
				<p class="font-semibold text-sm opacity-70 mb-1">Message :</p>
				<p>{selectedFeedback.message}</p>
			</div>

			{#if currentUser?.role !== 'student' && selectedFeedback.statut !== 'repondu'}
				<div class="form-control">
					<label class="label">
						<span class="label-text">Votre réponse :</span>
					</label>
					<textarea
						class="textarea textarea-bordered h-24 w-full focus:outline-none focus:ring-2 focus:ring-primary/50"
						placeholder="Écrivez votre réponse ici..."
						bind:value={replyText}
					></textarea>
				</div>
			{:else if selectedFeedback.reponse}
				<div class="mb-4 bg-success/10 p-4 rounded-lg border border-success/20">
                    <p class="font-semibold text-sm text-success mb-1">Réponse de l'administration :</p>
                    <p>{selectedFeedback.reponse}</p>
                </div>
			{/if}

			<div class="modal-action">
				<button class="btn btn-ghost" onclick={() => { showReplyModal = false; selectedFeedback = null; }}>Fermer</button>
				{#if currentUser?.role !== 'student'}
					<button class="btn btn-primary" onclick={sendReply} disabled={!replyText.trim() || selectedFeedback.statut === 'repondu'}>
						<Send size={18} class="mr-2" />
						Envoyer la réponse
					</button>
				{/if}
			</div>
		</div>
		<div class="modal-backdrop" onclick={() => { showReplyModal = false; selectedFeedback = null; }}>
			<button class="cursor-default">close</button>
		</div>
	</div>
{/if}

<!-- Modal Nouveau Feedback -->
{#if showNewFeedbackModal}
	<div class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg mb-4">Envoyer un nouveau feedback</h3>
			
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Sujet :</span>
				</label>
				<input
					type="text"
					class="input input-bordered w-full focus:outline-none focus:ring-2 focus:ring-primary/50"
					placeholder="Sujet de votre message..."
					bind:value={newFeedbackSujet}
				/>
			</div>

			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Message :</span>
				</label>
				<textarea
					class="textarea textarea-bordered h-32 w-full focus:outline-none focus:ring-2 focus:ring-primary/50"
					placeholder="Décrivez votre problème ou suggestion..."
					bind:value={newFeedbackMessage}
				></textarea>
			</div>
			
			{#if submitError}
				<div class="alert alert-error text-sm mb-4">
					<XCircle size={16} />
					<span>{submitError}</span>
				</div>
			{/if}

			<div class="modal-action">
				<button class="btn btn-ghost" onclick={() => showNewFeedbackModal = false} disabled={isSubmitting}>Annuler</button>
				<button class="btn btn-primary" onclick={submitFeedback} disabled={!newFeedbackSujet.trim() || !newFeedbackMessage.trim() || isSubmitting}>
					{#if isSubmitting}
						<span class="loading loading-spinner loading-xs mr-2"></span>
					{:else}
						<Send size={18} class="mr-2" />
					{/if}
					Envoyer
				</button>
			</div>
		</div>
		<div class="modal-backdrop" onclick={() => !isSubmitting && (showNewFeedbackModal = false)}>
			<button class="cursor-default">close</button>
		</div>
	</div>
{/if}
