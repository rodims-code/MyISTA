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

  let isImageModalOpen = false;

  function openImage() {
    isImageModalOpen = true;
  }

  function closeImage() {
    isImageModalOpen = false;
  }
</script>

<div class="mb-8 relative rounded-[2rem] shadow-xl shadow-base-200/50 border border-base-200/50 bg-base-100 overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-base-200">
  
  {#if post.image}
    <!-- IMAGE LAYOUT AVEC OVERLAY GLASSMORPHISM -->
    <div class="relative w-full group">
      <!-- L'image en fond -->
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <img 
        src={post.image} 
        alt="Post media" 
        class="w-full object-cover min-h-[400px] max-h-[600px] cursor-pointer" 
        onclick={openImage}
      />
      
      <!-- Bouton d'expansion en haut à droite pour bien montrer qu'on peut cliquer -->
      <button class="absolute top-4 right-4 btn btn-circle btn-sm bg-black/30 hover:bg-black/50 text-white border-0 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity" onclick={openImage}>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg>
      </button>

      <!-- Fading Blur Background Overlay -->
      <div 
        class="absolute bottom-0 left-0 right-0 h-64 pointer-events-none" 
        style="backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); mask-image: linear-gradient(to top, black 60%, transparent 100%); -webkit-mask-image: linear-gradient(to top, black 60%, transparent 100%);"
      >
        <div class="absolute inset-0 bg-gradient-to-t from-base-100/90 via-base-100/40 to-transparent"></div>
      </div>

      <!-- Contenu textuel par dessus le blur -->
      <div class="absolute bottom-0 left-0 right-0 p-5 pt-12">
        <!-- Author Info -->
        <div class="flex justify-between items-center mb-3">
          <div class="flex items-center gap-3">
            <div class="avatar placeholder cursor-pointer" onclick={() => dispatch('userClick', post.author)}>
              <div class="bg-gradient-to-tr from-primary to-secondary text-primary-content rounded-full w-10 shadow-md flex items-center justify-center">
                <span class="text-base font-bold">{post.author_details?.username?.charAt(0).toUpperCase() || 'U'}</span>
              </div>
            </div>
            <div>
              <h3 class="font-bold text-sm cursor-pointer hover:text-primary transition-colors drop-shadow-sm" onclick={() => dispatch('userClick', post.author)}>
                {post.author_details?.username}
              </h3>
              <p class="text-[10px] opacity-80 font-medium tracking-wide uppercase">{formatDate(post.created_at)} • {post.author_details?.filiere || 'Étudiant'}</p>
            </div>
          </div>
        </div>

        <!-- Text Content -->
        {#if post.content}
          <p class="text-sm font-medium leading-relaxed whitespace-pre-wrap mb-4 drop-shadow-sm line-clamp-3">{post.content}</p>
        {/if}

        <!-- Actions -->
        <div class="flex items-center justify-between">
          <div class="flex gap-2">
            <button 
              class="btn btn-sm rounded-full gap-2 px-4 border-0 {post.is_liked ? 'text-error bg-white/70 hover:bg-white/90 dark:bg-black/50 dark:hover:bg-black/70' : 'bg-white/50 hover:bg-white/70 dark:bg-black/40 dark:hover:bg-black/60 shadow-sm'}"
              onclick={handleLike}
            >
              <Heart size={18} fill={post.is_liked ? "currentColor" : "none"} />
              <span class="font-bold drop-shadow-sm">{post.likes_count || 0}</span>
            </button>
            
            <button 
              class="btn btn-sm rounded-full gap-2 px-4 border-0 bg-white/50 hover:bg-white/70 dark:bg-black/40 dark:hover:bg-black/60 shadow-sm"
              onclick={toggleComments}
            >
              <MessageCircle size={18} />
              <span class="font-bold drop-shadow-sm">{post.comments_count || 0}</span>
            </button>
          </div>
          
          <button class="btn btn-sm btn-circle border-0 bg-white/50 hover:bg-white/70 dark:bg-black/40 dark:hover:bg-black/60 shadow-sm">
            <Share2 size={16} />
          </button>
        </div>
      </div>
    </div>
  {:else}
    <!-- TEXT/FILE ONLY LAYOUT (NO IMAGE) -->
    <div class="p-5">
      <!-- Header: User Info -->
      <div class="flex justify-between items-center mb-4">
        <div class="flex items-center gap-4">
          <div class="avatar placeholder cursor-pointer" onclick={() => dispatch('userClick', post.author)}>
            <div class="bg-gradient-to-tr from-primary to-secondary text-primary-content rounded-full w-12 shadow-md flex items-center justify-center">
              <span class="text-xl font-bold">{post.author_details?.username?.charAt(0).toUpperCase() || 'U'}</span>
            </div>
          </div>
          <div>
            <h3 class="font-bold text-base cursor-pointer hover:text-primary transition-colors" onclick={() => dispatch('userClick', post.author)}>
              {post.author_details?.username}
            </h3>
            <p class="text-xs text-base-content/50 font-medium tracking-wide uppercase mt-0.5">{formatDate(post.created_at)} • {post.author_details?.filiere || 'Étudiant'}</p>
          </div>
        </div>
      </div>

      <!-- Content -->
      {#if post.content}
        <div class="pb-4">
          <p class="text-base-content/90 text-[15px] leading-relaxed whitespace-pre-wrap">{post.content}</p>
        </div>
      {/if}

      <!-- Actions -->
      <div class="pt-2 flex items-center justify-between border-t border-base-200/50 mt-2">
        <div class="flex gap-2">
          <button 
            class="btn btn-ghost btn-sm rounded-full gap-2 px-4 {post.is_liked ? 'text-error bg-error/10' : 'text-base-content/70 hover:text-error hover:bg-error/10'}"
            onclick={handleLike}
          >
            <Heart size={20} fill={post.is_liked ? "currentColor" : "none"} />
            <span class="font-bold">{post.likes_count || 0}</span>
          </button>
          
          <button 
            class="btn btn-ghost btn-sm rounded-full gap-2 px-4 text-base-content/70 hover:text-primary hover:bg-primary/10"
            onclick={toggleComments}
          >
            <MessageCircle size={20} />
            <span class="font-bold">{post.comments_count || 0}</span>
          </button>
        </div>
        
        <button class="btn btn-ghost btn-sm btn-circle text-base-content/70 hover:bg-base-200">
          <Share2 size={18} />
        </button>
      </div>
    </div>
  {/if}

  <!-- Media: Fichier (s'affiche toujours en dessous si présent) -->
  {#if post.fichier}
    <div class="px-5 pb-5 pt-2 {post.image ? 'bg-base-100' : ''}">
      <div class="flex items-center justify-between p-4 rounded-2xl border border-base-200 bg-base-50 hover:bg-base-200/50 transition-colors group cursor-pointer shadow-sm">
        <div class="flex items-center gap-4 overflow-hidden">
          <div class="p-3 bg-secondary/10 text-secondary rounded-xl group-hover:scale-110 transition-transform">
            <FileText size={24} />
          </div>
          <div>
            <span class="text-sm font-bold block truncate">{post.fichier.split('/').pop() || 'Document joint'}</span>
            <span class="text-xs text-base-content/50">Fichier attaché</span>
          </div>
        </div>
        <a href={post.fichier} target="_blank" class="btn btn-primary btn-sm btn-circle shadow-md" download onclick={(e) => e.stopPropagation()}>
          <Download size={16} />
        </a>
      </div>
    </div>
  {/if}

  <!-- Comments Section (S'affiche en dessous du blur si ouvert) -->
  {#if showComments}
    <div class="px-5 pb-5 bg-base-100 border-t border-base-200/50 pt-4">
      {#if isLoadingComments}
        <div class="flex justify-center py-6">
          <span class="loading loading-spinner loading-md text-primary"></span>
        </div>
      {:else}
        <CommentSection {comments} postId={post.id} on:submit={handleCommentSubmit} />
      {/if}
    </div>
  {/if}
</div>

<!-- Image Modal (Vue sans blur) -->
{#if isImageModalOpen && post.image}
  <div class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 backdrop-blur-sm p-4" onclick={closeImage}>
    <button class="absolute top-4 right-4 btn btn-ghost btn-circle text-white hover:bg-white/20" onclick={closeImage}>
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
    </button>
    <!-- Image en entier SANS BLUR OVERLAY -->
    <img src={post.image} alt="Post media full" class="max-w-full max-h-full object-contain rounded-xl shadow-2xl" onclick={(e) => e.stopPropagation()} />
  </div>
{/if}
