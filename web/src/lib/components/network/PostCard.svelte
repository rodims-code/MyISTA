<script lang="ts">
  import { Heart, MessageCircle, FileText, Download, Share2 } from 'lucide-svelte';
  import CommentSection from './CommentSection.svelte';
  import { createEventDispatcher, onMount } from 'svelte';
  import { fetchComments } from '$lib/networkApi';
  
  export let post: any;
  
  const dispatch = createEventDispatcher();
  
  let showComments = false;
  let comments: any[] = [];
  let isLoadingComments = false;

  async function loadComments() {
    if (showComments && comments.length === 0 && post.comments_count > 0) {
      isLoadingComments = true;
      comments = await fetchComments(post.id);
      isLoadingComments = false;
    }
  }

  function toggleComments() {
    showComments = !showComments;
    loadComments();
  }

  function handleLike() {
    dispatch('like', post.id);
  }

  async function handleCommentSubmit(event: CustomEvent) {
    const { postId, content } = event.detail;
    try {
      const newComment = await import('$lib/networkApi').then(m => m.createComment(postId, content));
      comments = [...comments, newComment];
      post.comments_count++;
      dispatch('comment', { postId, content }); // Notify parent if it wants to know
    } catch (error) {
      console.error('Erreur lors de la création du commentaire', error);
    }
  }

  // Permet au parent de mettre à jour la liste des commentaires (optionnel)
  export function updateComments(newComment: any) {
    comments = [...comments, newComment];
    post.comments_count++;
  }

  function formatDate(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
</script>

<div class="card bg-base-100 shadow-sm border border-base-200 mb-6 overflow-hidden">
  <!-- Header: User Info -->
  <div class="p-4 flex justify-between items-center">
    <div class="flex items-center gap-3">
      <div class="avatar placeholder cursor-pointer" onclick={() => dispatch('userClick', post.author)}>
        <div class="bg-primary text-primary-content rounded-full w-10">
          <span class="text-lg">{post.author_details?.username?.charAt(0).toUpperCase() || 'U'}</span>
        </div>
      </div>
      <div>
        <h3 class="font-bold text-sm cursor-pointer hover:underline" onclick={() => dispatch('userClick', post.author)}>
          {post.author_details?.username}
        </h3>
        <p class="text-xs text-base-content/50">{formatDate(post.created_at)} • {post.author_details?.filiere || 'Étudiant'}</p>
      </div>
    </div>
  </div>

  <!-- Content -->
  {#if post.content}
    <div class="px-4 pb-3">
      <p class="text-sm whitespace-pre-wrap">{post.content}</p>
    </div>
  {/if}

  <!-- Media: Image -->
  {#if post.image}
    <figure>
      <img src={post.image} alt="Post media" class="w-full object-cover max-h-96" />
    </figure>
  {/if}

  <!-- Media: Fichier -->
  {#if post.fichier}
    <div class="px-4 pb-3 pt-2">
      <div class="flex items-center justify-between p-3 rounded-xl border border-base-200 bg-base-50 hover:bg-base-200 transition-colors">
        <div class="flex items-center gap-3 overflow-hidden">
          <div class="p-2 bg-secondary/10 text-secondary rounded-lg">
            <FileText size={20} />
          </div>
          <span class="text-sm font-medium truncate">{post.fichier.split('/').pop() || 'Document joint'}</span>
        </div>
        <a href={post.fichier} target="_blank" class="btn btn-ghost btn-sm btn-circle" download>
          <Download size={16} />
        </a>
      </div>
    </div>
  {/if}

  <!-- Actions -->
  <div class="px-4 py-3 border-t border-base-200 flex items-center justify-between">
    <div class="flex gap-4">
      <button 
        class="flex items-center gap-1.5 transition-colors {post.is_liked ? 'text-error' : 'text-base-content/70 hover:text-error'}"
        onclick={handleLike}
      >
        <Heart size={20} fill={post.is_liked ? "currentColor" : "none"} />
        <span class="text-sm font-medium">{post.likes_count || 0}</span>
      </button>
      
      <button 
        class="flex items-center gap-1.5 text-base-content/70 hover:text-primary transition-colors"
        onclick={toggleComments}
      >
        <MessageCircle size={20} />
        <span class="text-sm font-medium">{post.comments_count || 0}</span>
      </button>
    </div>
    
    <button class="btn btn-ghost btn-sm btn-circle text-base-content/70">
      <Share2 size={18} />
    </button>
  </div>

  <!-- Comments Section -->
  {#if showComments}
    <div class="px-4 pb-4">
      {#if isLoadingComments}
        <div class="flex justify-center py-4">
          <span class="loading loading-spinner loading-md text-primary"></span>
        </div>
      {:else}
        <CommentSection {comments} postId={post.id} on:submit={handleCommentSubmit} />
      {/if}
    </div>
  {/if}
</div>
