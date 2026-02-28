<script lang="ts">
  import { 
    Map, 
    LayoutGrid, 
    FileText, 
    ShieldCheck, 
    Search, 
    Users, 
    ArrowRight, 
    ChevronRight,
    GraduationCap,
    Lightbulb,
    Target
  } from 'lucide-svelte';
  import { onMount } from 'svelte';

  // Animation simple au chargement
  let mounted = false;
  onMount(() => {
    mounted = true;
  });
</script>

<div class="min-h-screen bg-slate-50 font-sans text-slate-900 selection:bg-primary selection:text-white">
  
  <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
    <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-primary/5 blur-[120px] rounded-full animate-pulse"></div>
    <div class="absolute top-[20%] -right-[5%] w-[30%] h-[30%] bg-blue-400/10 blur-[100px] rounded-full"></div>
  </div>

  <nav class="navbar sticky top-0 z-50 backdrop-blur-md bg-white/80 border-b border-slate-200 px-4 md:px-12">
    <div class="navbar-start">
      <div class="flex items-center gap-2 group cursor-pointer">
        <div class="bg-primary text-primary-content p-2 rounded-xl shadow-lg shadow-primary/20 group-hover:scale-110 transition-transform">
          <GraduationCap size={24} />
        </div>
        <span class="font-bold text-xl tracking-tight text-slate-800">My<span class="text-primary">ISTA</span></span>
      </div>
    </div>
    
    <div class="navbar-center hidden lg:flex">
      <ul class="menu menu-horizontal gap-2 px-1 font-medium text-slate-600">
        <li><a href="#problemes" class="hover:text-primary transition-colors">Enjeux</a></li>
        <li><a href="#solutions" class="hover:text-primary transition-colors">Solutions</a></li>
        <li><a href="#pitch" class="hover:text-primary transition-colors">Institutionnel</a></li>
      </ul>
    </div>
    
    <div class="navbar-end gap-3">
      <a href="/login" class="btn btn-ghost btn-sm hidden md:flex">Se connecter</a>
      <a href="/register" class="btn btn-primary btn-sm shadow-md shadow-primary/30 px-6">Rejoindre</a>
    </div>
  </nav>

  <main class="relative z-10">
    
    <section class="hero min-h-[85vh] flex flex-col items-center justify-center px-6 overflow-hidden">
      <div class="max-w-4xl text-center">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 border border-blue-100 mb-8 animate-bounce-slow shadow-sm">
          <span class="flex h-2 w-2 rounded-full bg-primary"></span>
          <span class="text-xs font-bold uppercase tracking-wider text-primary">Développé par un étudiant de l'ISTA</span>
        </div>
        
        <h1 class="text-5xl md:text-7xl font-extrabold text-slate-900 leading-[1.1] mb-8">
          Une plateforme académique <br />
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-500 italic">intelligente et évolutive.</span>
        </h1>
        
        <p class="text-lg md:text-xl text-slate-600 mb-12 max-w-2xl mx-auto leading-relaxed">
          MyISTA centralise l'écosystème de l'institut pour offrir aux étudiants une navigation fluide, sécurisée et structurée au sein du campus.
        </p>
        
        <div class="flex flex-wrap justify-center gap-4">
          <button class="btn btn-primary btn-lg px-10 shadow-xl shadow-primary/25 group">
            Commencer l'expérience <ArrowRight size={18} class="ml-2 group-hover:translate-x-1 transition-transform" />
          </button>
          <button class="btn btn-outline btn-lg px-10 border-slate-200 hover:bg-slate-50 hover:text-primary">
            Découvrir le projet
          </button>
        </div>
      </div>

      <div class="mt-16 w-full max-w-5xl px-4 relative">
        <div class="aspect-video bg-gradient-to-br from-white to-slate-100 rounded-3xl border border-slate-200 shadow-2xl overflow-hidden relative group">
           <div class="absolute inset-0 bg-grid-slate-200/50 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]"></div>
           <div class="absolute inset-0 flex items-center justify-center">
              <div class="flex flex-col items-center opacity-40 group-hover:opacity-100 transition-opacity">
                <LayoutGrid size={64} class="text-primary mb-4" />
                <p class="font-mono text-sm tracking-widest uppercase">Dashboard Aperçu</p>
              </div>
           </div>
        </div>
        <div class="absolute -bottom-6 left-1/2 -translate-x-1/2 w-3/4 h-12 bg-primary/10 blur-3xl rounded-full"></div>
      </div>
    </section>

    <section id="problemes" class="py-24 bg-white px-6">
      <div class="max-w-6xl mx-auto">
        <div class="flex flex-col md:flex-row justify-between items-end gap-6 mb-16">
          <div class="max-w-xl">
            <h2 class="text-sm font-bold text-primary uppercase tracking-[0.2em] mb-4">L'Origine du Projet</h2>
            <h3 class="text-3xl md:text-4xl font-bold text-slate-900">Pourquoi MyISTA ?</h3>
            <p class="text-slate-500 mt-4">Né d'un constat réel sur le campus, MyISTA répond aux difficultés quotidiennes de la vie estudiantine.</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {@render problemCard(Search, "Désorientation", "Difficultés majeures pour les nouveaux étudiants à s'orienter lors des premiers jours.")}
          {@render problemCard(Map, "Salles Introuvables", "Perte de temps systématique à chercher les affectations de salles par niveau.")}
          {@render problemCard(FileText, "Dispersion des Infos", "Informations académiques critiques perdues dans le flux des messageries sociales.")}
          {@render problemCard(ShieldCheck, "Manque de Structure", "Besoin d'un espace numérique centralisé pour la sécurité des documents.")}
        </div>
      </div>
    </section>

    <section id="solutions" class="py-24 bg-slate-900 text-white px-6 relative overflow-hidden">
      <div class="absolute top-0 right-0 w-[50%] h-[50%] bg-primary/10 blur-[150px] rounded-full"></div>
      
      <div class="max-w-6xl mx-auto relative z-10">
        <div class="text-center max-w-3xl mx-auto mb-20">
          <h2 class="text-3xl md:text-5xl font-bold mb-6">Une réponse concrète, locale et évolutive</h2>
          <p class="text-slate-400">Plus qu'une application, un compagnon numérique pour chaque étudiant de l'ISTA.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="space-y-4">
            {@render solutionItem(Map, "Carte interactive du campus", "Localisez vos bâtiments et services en un clin d'œil.")}
            {@render solutionItem(LayoutGrid, "Affectation des salles", "Filtrez par niveau et filière pour trouver votre salle instantanément.")}
            {@render solutionItem(FileText, "Espace centralisé", "Accédez à vos documents académiques sans risque de perte.")}
            {@render solutionItem(ShieldCheck, "Accès sécurisé étudiant", "Un environnement propre et protégé pour vos données.")}
          </div>
          <div class="bg-white/5 border border-white/10 p-8 rounded-[2.5rem] backdrop-blur-sm">
            <div class="space-y-6">
                <div class="h-4 w-3/4 bg-white/10 rounded-full animate-pulse"></div>
                <div class="h-4 w-1/2 bg-white/10 rounded-full animate-pulse"></div>
                <div class="grid grid-cols-2 gap-4 pt-4">
                    <div class="h-32 bg-primary/20 rounded-2xl border border-primary/30"></div>
                    <div class="h-32 bg-white/5 rounded-2xl border border-white/10"></div>
                </div>
                <div class="h-4 w-full bg-white/10 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="pitch" class="py-24 px-6 relative">
      <div class="max-w-4xl mx-auto">
        <div class="card bg-white shadow-2xl border border-slate-100 overflow-hidden">
          <div class="flex flex-col md:flex-row">
            <div class="bg-primary p-12 text-primary-content md:w-1/3 flex flex-col justify-center items-center text-center">
              <GraduationCap size={64} class="mb-4 opacity-50" />
              <h4 class="text-2xl font-bold italic tracking-tight leading-tight">Le Message du Développeur</h4>
            </div>
            <div class="p-10 md:p-14 md:w-2/3 relative">
              <div class="absolute top-8 right-8 text-slate-100">
                <Lightbulb size={120} />
              </div>
              <div class="relative z-10 prose prose-slate max-w-none italic text-slate-600 leading-[1.8]">
                <p class="not-italic font-bold text-slate-900 mb-6 text-xl">Monsieur / Madame,</p>
                <p>
                  <strong>MyISTA</strong> est une application web et mobile conçue pour améliorer l’orientation, la sécurité et l’accès aux ressources académiques des étudiants de l’ISTA.
                </p>
                <p>Elle permet :</p>
                <ul class="list-disc pl-5 my-4 not-italic font-medium text-slate-800 space-y-2">
                  <li>Une carte claire du campus</li>
                  <li>L’affectation des salles par niveau et filière</li>
                  <li>Un espace centralisé de documents académiques afin d’éviter la perte d’informations dans les groupes de messagerie</li>
                </ul>
                <p>
                  MyISTA ne remplace pas les services officiels de l’ISTA, elle les complète. Elle a été développée par un étudiant de l’ISTA pour répondre à des problèmes concrets rencontrés sur le campus.
                </p>
                <p class="mt-6">
                  À terme, elle pourra évoluer vers une solution intégrée au réseau interne de l’institut.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <footer class="bg-slate-50 border-t border-slate-200 py-16 px-6">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12">
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center gap-2 mb-6">
            <div class="bg-primary text-white p-1.5 rounded-lg">
                <GraduationCap size={20} />
            </div>
            <span class="font-bold text-xl tracking-tight">MyISTA</span>
          </div>
          <p class="text-slate-500 max-w-sm">
            Une plateforme académique intelligente au service de l'excellence de l'Institut Supérieur des Techniques Appliquées.
          </p>
        </div>
        <div>
          <h5 class="font-bold mb-4">Navigation</h5>
          <ul class="space-y-2 text-slate-600">
            <li><a href="#problemes" class="hover:text-primary">Enjeux</a></li>
            <li><a href="#solutions" class="hover:text-primary">Fonctionnalités</a></li>
            <li><a href="#pitch" class="hover:text-primary">Pitch Officiel</a></li>
          </ul>
        </div>
        <div>
          <h5 class="font-bold mb-4">Contact</h5>
          <ul class="space-y-2 text-slate-600">
            <li>Support étudiant</li>
            <li>Administration ISTA</li>
            <li>Portail de sécurité</li>
          </ul>
        </div>
      </div>
      <div class="max-w-6xl mx-auto border-t border-slate-200 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-slate-400">
        <p>© 2026 MyISTA. Conçu et développé avec passion pour l'ISTA.</p>
        <div class="flex gap-6 italic">
            <span>Solution locale & évolutive</span>
        </div>
      </div>
    </footer>
  </main>
</div>

{#snippet problemCard(Icon, title, desc)}
  <div class="group p-8 rounded-3xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-xl hover:shadow-slate-200/50 hover:-translate-y-2 transition-all duration-300">
    <div class="w-12 h-12 rounded-2xl bg-white shadow-sm flex items-center justify-center text-primary mb-6 group-hover:bg-primary group-hover:text-white transition-colors">
      <Icon size={24} />
    </div>
    <h4 class="font-bold text-xl mb-3">{title}</h4>
    <p class="text-slate-500 text-sm leading-relaxed">{desc}</p>
  </div>
{/snippet}

{#snippet solutionItem(Icon, title, desc)}
  <div class="flex gap-6 p-6 rounded-2xl hover:bg-white/5 transition-colors border border-transparent hover:border-white/10">
    <div class="shrink-0 w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center text-primary">
      <Icon size={24} />
    </div>
    <div>
      <h4 class="font-bold text-lg text-white mb-1">{title}</h4>
      <p class="text-slate-400 text-sm">{desc}</p>
    </div>
  </div>
{/snippet}

<style>
  :global(html) {
    scroll-behavior: smooth;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  .animate-bounce-slow {
    animation: float 4s ease-in-out infinite;
  }
</style>