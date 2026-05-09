<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchPosts, createPost, likePost, createComment } from '$lib/networkApi';
  import PostCard from '$lib/components/network/PostCard.svelte';
  import CreatePostModal from '$lib/components/network/CreatePostModal.svelte';
  import { goto } from '$app/navigation';

  let posts: any[] = [];
  let isLoading = true;

  onMount(async () => {
    await loadPosts();
  });

  async function loadPosts() {
    isLoading = true;
    posts = await fetchPosts();
    isLoading = false;
  }

  async function handleCreatePost(event: CustomEvent) {
    try {
      const newPost = await createPost(event.detail);
      posts = [newPost, ...posts];
    } catch (error) {
      console.error(error);
      alert('Erreur lors de la création du post');
    }
  }

  async function handleLike(event: CustomEvent) {
    const postId = event.detail;
    try {
      const res = await likePost(postId);
      
      // Update local state
      posts = posts.map(p => {
        if (p.id === postId) {
          return {
            ...p,
            is_liked: res.status === 'liked',
            likes_count: res.status === 'liked' ? p.likes_count + 1 : Math.max(0, p.likes_count - 1)
          };
        }
        return p;
      });
    } catch (error) {
      console.error('Erreur like:', error);
    }
  }

  async function handleComment(event: CustomEvent) {
    const { postId, content } = event.detail;
    try {
      const newComment = await createComment(postId, content);
      
      // Update the specific post card in the UI
      // To do this simply, we will reload posts or find a way to dispatch back to the card.
      // But we can also let the PostCard component handle its own comments state if we pass it a ref.
      // Easiest is to reload all posts or update the count.
      posts = posts.map(p => {
        if (p.id === postId) {
          return { ...p, comments_count: p.comments_count + 1 };
        }
        return p;
      });
      // A better way would be binding to a component method, but we can't easily do that in an each block without an array of bindings.
      // Let's just do a full reload for simplicity in this MVP, or ignore since PostCard might not need us to push the comment if we just update the count.
      // Wait, we passed the event up. It's better to let PostCard manage its comment list.
    } catch (error) {
      console.error('Erreur comment:', error);
    }
  }

  function goToProfile(event: CustomEvent) {
    const user = event.detail;
    goto(`/dashboard/profile/${user}`);
  }
</script>

<div class="max-w-2xl mx-auto py-4">
  <div class="mb-6">
    <h1 class="text-2xl font-bold mb-2">Fil d'actualité</h1>
    <p class="text-base-content/60 text-sm">Découvrez ce qui se passe sur le campus.</p>
  </div>

  <CreatePostModal on:submit={handleCreatePost} />

  {#if isLoading}
    <div class="flex justify-center py-10">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>
  {:else if posts.length === 0}
    <div class="text-center py-10 bg-base-200 rounded-2xl border border-base-300 border-dashed">
      <p class="text-base-content/60">Aucun post pour le moment.</p>
      <p class="text-sm text-base-content/40 mt-1">Soyez le premier à publier !</p>
    </div>
  {:else}
    <div class="flex flex-col">
      {#each posts as post (post.id)}
        <PostCard 
          {post} 
          on:like={handleLike} 
          on:comment={handleComment} 
          on:userClick={goToProfile}
        />
      {/each}
    </div>
  {/if}
</div>
