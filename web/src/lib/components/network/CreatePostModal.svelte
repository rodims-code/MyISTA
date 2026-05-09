<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Image, FileText, Send, X } from 'lucide-svelte';
  
  let content = '';
  let imageFile: File | null = null;
  let docFile: File | null = null;
  let isSubmitting = false;

  const dispatch = createEventDispatcher();

  function handleImageChange(e: Event) {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      imageFile = target.files[0];
    }
  }

  function handleDocChange(e: Event) {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      docFile = target.files[0];
    }
  }

  function submitPost() {
    if (!content.trim() && !imageFile && !docFile) return;
    
    isSubmitting = true;
    const formData = new FormData();
    if (content) formData.append('content', content);
    if (imageFile) formData.append('image', imageFile);
    if (docFile) formData.append('fichier', docFile);
    
    dispatch('submit', formData);
    
    // Reset form
    content = '';
    imageFile = null;
    docFile = null;
    isSubmitting = false;
  }
</script>

<div class="card bg-base-100 shadow-sm border border-base-200 mb-6">
  <div class="card-body p-4">
    <div class="flex gap-4">
      <div class="avatar placeholder">
        <div class="bg-neutral text-neutral-content rounded-full w-10">
          <span>U</span>
        </div>
      </div>
      <textarea
        bind:value={content}
        class="textarea textarea-ghost w-full resize-none text-base"
        placeholder="Quoi de neuf ?"
        rows="2"
      ></textarea>
    </div>
    
    {#if imageFile || docFile}
      <div class="flex flex-col gap-2 mt-2 px-14">
        {#if imageFile}
          <div class="badge badge-primary gap-2 p-3">
            <Image size={14} />
            {imageFile.name}
            <button class="btn btn-ghost btn-xs rounded-full p-0 h-4 min-h-0" onclick={() => imageFile = null}>
              <X size={12} />
            </button>
          </div>
        {/if}
        {#if docFile}
          <div class="badge badge-secondary gap-2 p-3">
            <FileText size={14} />
            {docFile.name}
            <button class="btn btn-ghost btn-xs rounded-full p-0 h-4 min-h-0" onclick={() => docFile = null}>
              <X size={12} />
            </button>
          </div>
        {/if}
      </div>
    {/if}

    <div class="flex justify-between items-center mt-2 pl-14">
      <div class="flex gap-2">
        <label class="btn btn-ghost btn-sm btn-circle text-base-content/70">
          <Image size={20} />
          <input type="file" accept="image/*" class="hidden" onchange={handleImageChange} />
        </label>
        <label class="btn btn-ghost btn-sm btn-circle text-base-content/70">
          <FileText size={20} />
          <input type="file" accept=".pdf,.doc,.docx" class="hidden" onchange={handleDocChange} />
        </label>
      </div>
      <button 
        class="btn btn-primary btn-sm rounded-full px-6" 
        onclick={submitPost} 
        disabled={isSubmitting || (!content.trim() && !imageFile && !docFile)}
      >
        {#if isSubmitting}
          <span class="loading loading-spinner loading-xs"></span>
        {:else}
          Publier <Send size={16} />
        {/if}
      </button>
    </div>
  </div>
</div>
