<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { fetchPosts, toggleFollow, likePost, createComment } from '$lib/networkApi';
  import api from '$lib/index';
  import PostCard from '$lib/components/network/PostCard.svelte';
  import { UserPlus, UserMinus, FileText, Image as ImageIcon } from 'lucide-svelte';

  let userId = $page.params.id;
  
  let profileUser: any = null;
  let userPosts: any[] = [];
  let isLoading = true;
  let isFollowing = false; // We would ideally get this from the API if we fetch the profile
  let followersCount = 0;
  let followingCount = 0;
  
  // We need to fetch the user profile. Let's add a quick mock/api call for user info
  async function loadProfile() {
    isLoading = true;
    try {
      // In a real app, you'd have an endpoint like /api/network/users/ID/
      // For Phase 1 MVP, we will try to get the user details from their posts
      const allPosts = await fetchPosts();
      userPosts = allPosts.filter((p: any) => p.author.toString() === userId);
      
      if (userPosts.length > 0) {
        profileUser = userPosts[0].author_details;
      } else {
        // Fallback if no posts
        profileUser = { username: 'Utilisateur', filiere: 'ISTA' };
      }
      
      // Fetch follows to calculate counts and check if following
      try {
        const resFollows = await api.get('api/network/follows/');
        const allFollows = resFollows.data;
        
        followersCount = allFollows.filter((f: any) => f.following.toString() === userId).length;
        followingCount = allFollows.filter((f: any) => f.follower.toString() === userId).length;
        
        // Check if current user is following this profile
        const currentUserRes = await api.get('api/user/me/');
        const currentUserId = currentUserRes.data.id;
        
        isFollowing = allFollows.some((f: any) => f.follower === currentUserId && f.following.toString() === userId);
      } catch (e) {
        console.error("Erreur follows:", e);
      }
      
    } catch (error) {
      console.error(error);
    }
    isLoading = false;
  }

  onMount(() => {
    loadProfile();
  });

  async function handleToggleFollow() {
    try {
      const res = await toggleFollow(userId);
      isFollowing = res.status === 'followed';
      followersCount += isFollowing ? 1 : -1;
    } catch (error) {
      console.error("Erreur toggle follow:", error);
    }
  }

  async function handleLike(event: CustomEvent) {
    const postId = event.detail;
    try {
      const res = await likePost(postId);
      userPosts = userPosts.map(p => {
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

  // React to URL changes (if we click on a profile from within a profile)
  $: {
    if ($page.params.id && $page.params.id !== userId) {
      userId = $page.params.id;
      loadProfile();
    }
  }
</script>

{#if isLoading}
  <div class="flex justify-center py-20">
    <span class="loading loading-spinner loading-lg text-primary"></span>
  </div>
{:else}
  <div class="max-w-3xl mx-auto">
    <!-- Header Profil -->
    <div class="card bg-base-100 shadow-sm border border-base-200 mb-6 overflow-hidden">
      <div class="h-32 bg-gradient-to-r from-primary/30 to-secondary/30"></div>
      <div class="px-6 pb-6 relative">
        <div class="flex justify-between items-end -mt-12 mb-4">
          <div class="avatar">
            <div class="w-24 rounded-full ring ring-base-100 ring-offset-base-100 ring-offset-2 bg-primary text-primary-content flex items-center justify-center text-4xl font-bold">
              <span>{profileUser?.username?.charAt(0).toUpperCase() || 'U'}</span>
            </div>
          </div>
          <button 
            class="btn {isFollowing ? 'btn-outline' : 'btn-primary'} btn-sm rounded-full px-6"
            onclick={handleToggleFollow}
          >
            {#if isFollowing}
              <UserMinus size={16} /> Ne plus suivre
            {:else}
              <UserPlus size={16} /> Suivre
            {/if}
          </button>
        </div>
        
        <div>
          <h1 class="text-2xl font-bold">{profileUser?.username || 'Utilisateur inconnu'}</h1>
          <p class="text-base-content/70">{profileUser?.filiere || 'Étudiant'} • {profileUser?.niveau || ''}</p>
        </div>
        
        <div class="flex gap-6 mt-4 pt-4 border-t border-base-200">
          <div class="flex flex-col">
            <span class="text-xl font-bold">{userPosts.length}</span>
            <span class="text-sm text-base-content/60">Posts</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xl font-bold">{followersCount}</span>
            <span class="text-sm text-base-content/60">Followers</span>
          </div>
          <div class="flex flex-col">
            <span class="text-xl font-bold">{followingCount}</span>
            <span class="text-sm text-base-content/60">Suivis</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Publications -->
    <h2 class="text-xl font-bold mb-4 px-2">Publications</h2>
    
    {#if userPosts.length === 0}
      <div class="text-center py-10 bg-base-200 rounded-2xl border border-base-300 border-dashed">
        <p class="text-base-content/60">Cet utilisateur n'a pas encore publié de post.</p>
      </div>
    {:else}
      <div class="flex flex-col gap-2">
        {#each userPosts as post (post.id)}
          <PostCard 
            {post} 
            on:like={handleLike} 
          />
        {/each}
      </div>
    {/if}
  </div>
{/if}
