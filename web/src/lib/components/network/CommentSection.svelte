<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Send } from 'lucide-svelte';
  
  export let comments: any[] = [];
  export let postId: number;
  
  let newComment = '';
  let isSubmitting = false;

  const dispatch = createEventDispatcher();

  function submitComment() {
    if (!newComment.trim()) return;
    
    isSubmitting = true;
    dispatch('submit', { postId, content: newComment });
    newComment = '';
    isSubmitting = false;
  }
</script>

<div class="mt-4 pt-4 border-t border-base-200">
  <!-- Liste des commentaires -->
  {#if comments.length > 0}
    <div class="flex flex-col gap-3 mb-4 max-h-60 overflow-y-auto">
      {#each comments as comment}
        <div class="flex gap-3">
          <div class="avatar placeholder">
            <div class="bg-neutral text-neutral-content rounded-full w-8 h-8">
              <span class="text-xs">{comment.author_details?.username?.charAt(0).toUpperCase() || 'U'}</span>
            </div>
          </div>
          <div class="flex-1 bg-base-200 rounded-2xl px-4 py-2 text-sm">
            <p class="font-bold">{comment.author_details?.username}</p>
            <p>{comment.content}</p>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <p class="text-sm text-base-content/50 mb-4">Aucun commentaire pour le moment. Soyez le premier !</p>
  {/if}

  <!-- Formulaire d'ajout -->
  <div class="flex gap-2 items-center">
    <div class="avatar placeholder">
      <div class="bg-primary text-primary-content rounded-full w-8 h-8">
        <span class="text-xs">M</span>
      </div>
    </div>
    <div class="relative flex-1">
      <input
        type="text"
        bind:value={newComment}
        placeholder="Ajouter un commentaire..."
        class="input input-bordered input-sm w-full rounded-full pr-10"
        onkeydown={(e) => e.key === 'Enter' && submitComment()}
      />
      <button 
        class="absolute right-1 top-1/2 -translate-y-1/2 btn btn-ghost btn-xs btn-circle text-primary"
        onclick={submitComment}
        disabled={isSubmitting || !newComment.trim()}
      >
        <Send size={14} />
      </button>
    </div>
  </div>
</div>
