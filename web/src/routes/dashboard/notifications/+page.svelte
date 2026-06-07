<script lang="ts">
	import { onMount } from 'svelte';
	import {
		fetchNotifications,
		markNotificationRead,
		markAllNotificationsRead
	} from '$lib/networkApi';
	import { goto } from '$app/navigation';
	import { Bell, Heart, MessageCircle, UserPlus, Bookmark, CheckCheck } from 'lucide-svelte';

	let notifications: any[] = [];
	let isLoading = true;
	let activeFilter: 'all' | 'unread' = 'all';

	$: unreadCount = notifications.filter((notification) => !notification.is_read).length;
	$: visibleNotifications =
		activeFilter === 'unread'
			? notifications.filter((notification) => !notification.is_read)
			: notifications;

	onMount(async () => {
		notifications = await fetchNotifications();
		isLoading = false;
	});

	function iconFor(type: string) {
		if (type === 'like') return Heart;
		if (type === 'comment' || type === 'message') return MessageCircle;
		if (type === 'follow') return UserPlus;
		if (type === 'favorite') return Bookmark;
		return Bell;
	}

	function toneFor(type: string) {
		if (type === 'like') return 'text-error bg-error/10';
		if (type === 'comment') return 'text-primary bg-primary/10';
		if (type === 'message') return 'text-info bg-info/10';
		if (type === 'follow') return 'text-success bg-success/10';
		if (type === 'favorite') return 'text-warning bg-warning/10';
		return 'text-base-content bg-base-200';
	}

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString('fr-FR', {
			day: 'numeric',
			month: 'short',
			hour: '2-digit',
			minute: '2-digit'
		});
	}

	async function openNotification(notification: any) {
		if (!notification.is_read) {
			try {
				await markNotificationRead(notification.id);
				notifications = notifications.map((item) =>
					item.id === notification.id ? { ...item, is_read: true } : item
				);
			} catch (error) {
				console.error('Erreur lecture notification:', error);
			}
		}

		if (notification.type === 'message' && notification.conversation) {
			goto('/dashboard/messages');
			return;
		}

		if (notification.post) {
			goto('/dashboard/home');
			return;
		}

		if (notification.sender) {
			goto(`/dashboard/profile/${notification.sender}`);
		}
	}

	async function markAllRead() {
		try {
			await markAllNotificationsRead();
			notifications = notifications.map((notification) => ({ ...notification, is_read: true }));
		} catch (error) {
			console.error('Erreur lecture notifications:', error);
		}
	}
</script>

<div class="mx-auto max-w-3xl py-4">
	<div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
		<div>
			<h1 class="text-2xl font-bold">Notifications</h1>
			<p class="text-sm text-base-content/60">{unreadCount} notification(s) non lue(s).</p>
		</div>

		<div class="flex items-center gap-2">
			<div class="join">
				<button
					class="btn join-item btn-sm {activeFilter === 'all' ? 'btn-primary' : 'btn-ghost'}"
					onclick={() => (activeFilter = 'all')}
				>
					Toutes
				</button>
				<button
					class="btn join-item btn-sm {activeFilter === 'unread' ? 'btn-primary' : 'btn-ghost'}"
					onclick={() => (activeFilter = 'unread')}
				>
					Non lues
				</button>
			</div>
			<button
				class="btn gap-2 btn-outline btn-sm"
				onclick={markAllRead}
				disabled={unreadCount === 0}
			>
				<CheckCheck size={16} />
				Tout lire
			</button>
		</div>
	</div>

	{#if isLoading}
		<div class="flex justify-center py-16">
			<span class="loading loading-lg loading-spinner text-primary"></span>
		</div>
	{:else if visibleNotifications.length === 0}
		<div class="rounded-2xl border border-dashed border-base-300 bg-base-200 py-14 text-center">
			<Bell class="mx-auto mb-3 text-base-content/30" size={40} />
			<p class="text-base-content/60">Aucune notification.</p>
		</div>
	{:else}
		<div class="space-y-3">
			{#each visibleNotifications as notification}
				{@const Icon = iconFor(notification.type)}
				<button
					class="flex w-full items-center gap-4 rounded-2xl border border-base-200 bg-base-100 p-4 text-left shadow-sm transition hover:bg-base-200/60 {notification.is_read
						? 'opacity-75'
						: 'ring-1 ring-primary/20'}"
					onclick={() => openNotification(notification)}
				>
					<div
						class="grid h-12 w-12 shrink-0 place-items-center rounded-full {toneFor(
							notification.type
						)}"
					>
						<Icon size={22} />
					</div>
					<div class="min-w-0 flex-1">
						<div class="flex items-center gap-2">
							<p class="truncate font-semibold">
								{notification.text || 'Nouvelle notification'}
							</p>
							{#if !notification.is_read}
								<span class="badge badge-xs badge-primary"></span>
							{/if}
						</div>
						<p class="text-sm text-base-content/50">
							{notification.sender_details?.username || 'MyISTA'} · {formatDate(
								notification.created_at
							)}
						</p>
					</div>
				</button>
			{/each}
		</div>
	{/if}
</div>
