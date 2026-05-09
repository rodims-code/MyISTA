<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Image, FileText, Send, X, PencilLine } from 'lucide-svelte';
  
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

<div class="card bg-base-100 shadow-lg shadow-base-200/50 border border-base-200/50 mb-8 rounded-[2rem] overflow-hidden transition-all duration-300 hover:shadow-xl hover:shadow-base-200">
  <div class="card-body p-6">
    <div class="flex gap-4">
      <div class="avatar placeholder">
        <div class="bg-gradient-to-tr from-primary to-secondary text-primary-content rounded-full w-12 h-12 shadow-md flex items-center justify-center">
          <span class="text-xl flex items-center justify-center"><PencilLine /></span>
        </div>
      </div>
      <textarea
        bind:value={content}
        class="textarea w-full resize-none text-base border-0 focus:outline-none focus:ring-0 bg-transparent px-2 py-3 placeholder:text-base-content/40 leading-relaxed"
        placeholder="Quoi de neuf sur le campus ?"
        rows="2"
      ></textarea>
    </div>
    
    {#if imageFile || docFile}
      <div class="flex flex-col gap-2 mt-4 pl-[4rem]">
        {#if imageFile}
          <div class="badge badge-primary gap-2 p-3 py-4 rounded-xl shadow-sm">
            <Image size={16} />
            <span class="font-medium">{imageFile.name}</span>
            <button class="btn btn-ghost btn-xs rounded-full p-1 h-auto min-h-0 ml-1 hover:bg-black/10" onclick={() => imageFile = null}>
              <X size={14} />
            </button>
          </div>
        {/if}
        {#if docFile}
          <div class="badge badge-secondary gap-2 p-3 py-4 rounded-xl shadow-sm">
            <FileText size={16} />
            <span class="font-medium">{docFile.name}</span>
            <button class="btn btn-ghost btn-xs rounded-full p-1 h-auto min-h-0 ml-1 hover:bg-black/10" onclick={() => docFile = null}>
              <X size={14} />
            </button>
          </div>
        {/if}
      </div>
    {/if}

    <div class="flex justify-between items-center mt-4 pl-[4rem] border-t border-base-200/50 pt-4">
      <div class="flex gap-2">
        <label class="btn btn-ghost btn-sm btn-circle text-primary hover:bg-primary/10 transition-colors cursor-pointer tooltip tooltip-bottom" data-tip="Ajouter une photo">
          <Image size={20} />
          <input type="file" accept="image/*" class="hidden" onchange={handleImageChange} />
        </label>
        <label class="btn btn-ghost btn-sm btn-circle text-secondary hover:bg-secondary/10 transition-colors cursor-pointer tooltip tooltip-bottom" data-tip="Ajouter un document">
          <FileText size={20} />
          <input type="file" accept=".pdf,.doc,.docx" class="hidden" onchange={handleDocChange} />
        </label>
      </div>
      <button 
        class="btn btn-primary btn-sm rounded-full px-8 shadow-md hover:shadow-lg transition-all" 
        onclick={submitPost} 
        disabled={isSubmitting || (!content.trim() && !imageFile && !docFile)}
      >
        {#if isSubmitting}
          <span class="loading loading-spinner loading-xs"></span>
        {:else}
          <span class="font-bold">Publier</span> <Send size={16} class="ml-1" />
        {/if}
      </button>
    </div>
  </div>
</div>
