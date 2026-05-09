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
		Target,
		Github,
		MessageSquare,
		Send,
		Sparkles,
		Linkedin,
		User,
		Globe,
		Mail
	} from 'lucide-svelte';
	import { onMount } from 'svelte';
	import api from '$lib/index';

  	import logoRodim from '$lib/assets/rodims-code.png';
  	import apercuImage from '$lib/assets/Screenshot (44).png';
	import logoIsta from '$lib/assets/myIsta.png';
	import logoIstaIcon from '$lib/assets/myIstaIcon.png'



	// Animation simple au chargement
	let mounted = false;

	let feedbackNom = $state('');
	let feedbackMessage = $state('');
	let isSubmitting = $state(false);
	let submitSuccess = $state(false);
	let submitError = $state('');

	onMount(() => {
		mounted = true;
	});

	async function submitFeedback() {
		if (!feedbackMessage.trim()) return;
		isSubmitting = true;
		submitError = '';
		submitSuccess = false;
		
		try {
			const sujet = feedbackNom.trim() ? `Feedback Public: ${feedbackNom}` : 'Feedback Anonyme';
			await api.post('/api/feedbacks/', {
				sujet: sujet,
				message: feedbackMessage
			});
			submitSuccess = true;
			feedbackNom = '';
			feedbackMessage = '';
		} catch (error) {
			submitError = "Une erreur est survenue lors de l'envoi.";
		} finally {
			isSubmitting = false;
		}
	}
</script>

<div
	class="min-h-screen bg-slate-50 font-sans text-slate-900 selection:bg-primary selection:text-white"
>
	<div class="pointer-events-none fixed inset-0 z-0 overflow-hidden">
		<div
			class="absolute -top-[10%] -left-[10%] h-[50%] w-[50%] animate-pulse rounded-full bg-primary/20 blur-[120px]"
		></div>
		<div
			class="absolute top-[20%] -right-[5%] h-[40%] w-[40%] animate-pulse rounded-full bg-blue-400/20 blur-[100px]"
		></div>
		<div
			class="absolute bottom-[10%] left-[20%] h-[30%] w-[30%] animate-pulse rounded-full bg-indigo-500/10 blur-[120px]"
		></div>
	</div>

	<nav
		class="navbar sticky top-0 z-50 rounded-full border-b border-slate-200 bg-white/80 px-4 backdrop-blur-md md:px-12"
	>
		<div class="navbar-start">
			<div class="group flex cursor-pointer items-center gap-2">
				<div
					class="h-10 w-10 overflow-hidden rounded-xl bg-primary text-primary-content shadow-lg shadow-primary/20 transition-transform group-hover:scale-110"
				>
					<img src={logoIstaIcon} alt="Logo ISTA" class="h-full w-full object-cover" />
				</div>
				<span class="text-xl font-bold tracking-tight text-slate-800"
					>My<span class="text-primary">ISTA</span></span
				>
			</div>
		</div>

		<div class="navbar-center hidden lg:flex">
			<ul class="menu menu-horizontal gap-2 px-1 font-medium text-slate-600">
				<li><a href="#problemes" class="transition-colors hover:text-primary">Enjeux</a></li>
				<li><a href="#solutions" class="transition-colors hover:text-primary">Solutions</a></li>
				<li><a href="#pitch" class="transition-colors hover:text-primary">Institutionnel</a></li>
				<li>
					<a href="#feedback" class="animate-pulse transition-colors hover:text-primary">Feedback</a
					>
				</li>
			</ul>
		</div>

		<div class="navbar-end gap-3">
			<a
				href="/auth/login"
				class="btn hidden btn-ghost transition-all btn-sm hover:text-primary md:flex"
				>Se connecter</a
			>
			<a
				href="/auth/register"
				class="btn px-6 shadow-lg shadow-primary/40 transition-all btn-sm btn-primary hover:scale-105 hover:shadow-primary/70"
				>Rejoindre</a
			>
		</div>
	</nav>

	<main class="relative z-10">
		<section
			class="hero flex min-h-[85vh] flex-col items-center justify-center overflow-hidden px-6"
		>
			<div class="max-w-4xl text-center">
				<div
					class="animate-bounce-slow mb-8 inline-flex items-center gap-2 rounded-full border border-blue-100 bg-blue-50 px-4 py-2 shadow-sm"
				>
					<span class="flex h-2 w-2 rounded-full bg-primary"></span>
					<span class="text-xs font-bold tracking-wider text-primary uppercase"
						>Développé par un étudiant de l'ISTA pour l'ISTA</span
					>
				</div>

				<h1 class="mb-8 text-5xl leading-[1.1] font-extrabold text-slate-900 md:text-7xl">
					Une plateforme académique <br />
					<span
						class="bg-linear-to-r from-primary to-blue-500 bg-clip-text text-transparent italic drop-shadow-[0_0_15px_rgba(59,130,246,0.3)]"
						>intelligente et évolutive.</span
					>
				</h1>

				<div class="flex justify-center">
					<img src={logoIsta} alt="Logo ISTA" class="h-100 w-100 object-cover" />
				</div>

				<p class="mx-auto mb-12 max-w-2xl text-lg leading-relaxed text-slate-600 md:text-xl">
					MyISTA est un projet open source qui centralise l'écosystème de l'institut pour offrir aux
					étudiants une navigation fluide, sécurisée et structurée au sein du campus.
				</p>

				<div class="flex flex-wrap justify-center gap-4">
					<a
						href="/auth/register"
						class="group btn px-10 shadow-xl shadow-primary/40 transition-all btn-lg btn-primary hover:-translate-y-1 hover:shadow-2xl hover:shadow-primary/70"
					>
						Commencer l'expérience <ArrowRight
							size={18}
							class="ml-2 transition-transform group-hover:translate-x-1"
						/>
					</a>

					<a
						href="#problemes"
						class="btn border-slate-200 px-10 btn-outline btn-lg hover:bg-slate-50 hover:text-primary"
					>
						Découvrir le projet
					</a>
					<a
						href="https://github.com/rodims-code/MyISTA"
						target="_blank"
						rel="noopener noreferrer"
						class="btn rounded-full border-slate-200 px-10 btn-outline btn-lg hover:bg-slate-50 hover:text-primary"
					>
						<Github />
					</a>
				</div>
			</div>

			<div class="relative mt-16 w-full max-w-5xl px-4">
				<div
					class="group relative aspect-video overflow-hidden rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-slate-100 shadow-2xl"
				>
					<div
						class="bg-grid-slate-200/50 absolute inset-0 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]"
					></div>
					<div class="absolute inset-0 flex items-center justify-center">
						<div
							class="flex w-full flex-col items-center opacity-40 transition-opacity group-hover:opacity-100"
						>
							<!-- 							<LayoutGrid size={64} class="mb-4 text-primary" />
							<p class="font-mono text-sm tracking-widest uppercase">Dashboard Aperçu</p> -->
							<!-- svelte-ignore a11y_img_redundant_alt -->
							<img
								src={apercuImage}
								alt="Image not found"
								class="h-full w-[95%] rounded-xl"
							/>
						</div>
					</div>
				</div>
				<div
					class="absolute -bottom-6 left-1/2 h-12 w-3/4 -translate-x-1/2 rounded-full bg-primary/10 blur-3xl"
				></div>
			</div>
		</section>

		<section id="problemes" class="bg-white px-6 py-24">
			<div class="mx-auto max-w-6xl">
				<div class="mb-16 flex flex-col items-end justify-between gap-6 md:flex-row">
					<div class="max-w-xl">
						<h2 class="mb-4 text-sm font-bold tracking-[0.2em] text-primary uppercase">
							L'Origine du Projet
						</h2>
						<h3 class="text-3xl font-bold text-slate-900 md:text-4xl">Pourquoi MyISTA ?</h3>
						<p class="mt-4 text-slate-500">
							Né d'un constat réel sur le campus, MyISTA répond aux difficultés quotidiennes de la
							vie des etudiants.
						</p>
					</div>
				</div>

				<div class="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
					{@render problemCard(
						Search,
						'Désorientation',
						"Difficultés majeures pour les nouveaux étudiants à s'orienter lors des premiers jours."
					)}
					{@render problemCard(
						Map,
						'Salles Introuvables',
						'Perte de temps systématique à chercher les affectations de salles par niveau.'
					)}
					{@render problemCard(
						FileText,
						'Dispersion des Infos',
						'Informations académiques critiques perdues dans le flux des messageries sociales.'
					)}
					{@render problemCard(
						ShieldCheck,
						'Manque de Structure',
						"Besoin d'un espace numérique centralisé pour la sécurité des documents."
					)}
				</div>
			</div>
		</section>

		<section id="solutions" class="relative overflow-hidden bg-slate-900 px-6 py-24 text-white">
			<div
				class="absolute top-0 right-0 h-[50%] w-[50%] rounded-full bg-primary/10 blur-[150px]"
			></div>

			<div class="relative z-10 mx-auto max-w-6xl">
				<div class="mx-auto mb-20 max-w-3xl text-center">
					<h2 class="mb-6 text-3xl font-bold md:text-5xl">
						Une réponse concrète, locale et évolutive
					</h2>
					<p class="text-slate-400">
						Plus qu'une application, un compagnon numérique pour chaque étudiant de l'ISTA.
					</p>
				</div>

				<div class="grid grid-cols-1 items-center gap-12 lg:grid-cols-2">
					<div class="space-y-4">
						{@render solutionItem(
							Map,
							'Carte interactive du campus',
							"Localisez vos bâtiments et services en un clin d'œil."
						)}
						{@render solutionItem(
							LayoutGrid,
							'Affectation des salles',
							'Filtrez par niveau et filière pour trouver votre salle instantanément.'
						)}
						{@render solutionItem(
							FileText,
							'Espace centralisé',
							'Accédez à vos documents académiques sans risque de perte.'
						)}
						{@render solutionItem(
							ShieldCheck,
							'Accès sécurisé étudiant',
							'Un environnement propre et protégé pour vos données.'
						)}
					</div>
					<div
						class="relative rounded-[2.5rem] border border-white/10 bg-white/5 p-8 shadow-[0_0_30px_rgba(59,130,246,0.15)] backdrop-blur-md transition-all hover:shadow-[0_0_50px_rgba(59,130,246,0.3)]"
					>
						<div
							class="pointer-events-none absolute inset-0 rounded-[2.5rem] bg-gradient-to-br from-primary/20 to-transparent opacity-50"
						></div>
						<div class="relative space-y-6">
							<div class="h-4 w-3/4 animate-pulse rounded-full bg-white/10"></div>
							<div class="h-4 w-1/2 animate-pulse rounded-full bg-white/10"></div>
							<div class="grid grid-cols-2 gap-4 pt-4">
								<div
									class="h-32 rounded-2xl border border-primary/30 bg-primary/20 shadow-[0_0_15px_rgba(var(--color-primary),0.2)]"
								></div>
								<div
									class="h-32 rounded-2xl border border-white/10 bg-white/5 transition-colors hover:bg-white/10"
								></div>
							</div>
							<div class="h-4 w-full animate-pulse rounded-full bg-white/10"></div>
						</div>
					</div>
				</div>
			</div>
		</section>

		<section id="pitch" class="relative px-6 py-24">
			<div class="mx-auto max-w-4xl">
				<div class="card overflow-hidden border border-slate-100 bg-white shadow-2xl">
					<div class="flex flex-col md:flex-row">
						<div
							class="flex flex-col items-center justify-center bg-primary p-12 text-center text-primary-content md:w-1/3"
						>
							<img src={logoIstaIcon} alt="Logo ISTA" class="h-42 w-42 object-cover" />
							<h4 class="text-2xl leading-tight font-bold tracking-tight italic">
								Le Message du Développeur
							</h4>
						</div>
						<div class="relative p-10 md:w-2/3 md:p-14">
							<div class="absolute top-8 right-8 text-slate-100">
								<Lightbulb size={120} />
							</div>
							<div
								class="prose-slate relative z-10 prose max-w-none leading-[1.8] text-slate-600 italic"
							>
								<p class="mb-6 text-xl font-bold text-slate-900 not-italic">Monsieur / Madame,</p>
								<p>
									<strong>MyISTA</strong> est une application web et mobile conçue pour améliorer l’orientation,
									la sécurité et l’accès aux ressources académiques des étudiants de l’ISTA.
								</p>
								<p>Elle permet :</p>
								<ul class="my-4 list-disc space-y-2 pl-5 font-medium text-slate-800 not-italic">
									<li>Une carte claire du campus</li>
									<li>L’affectation des salles par niveau et filière</li>
									<li>
										Un espace centralisé de documents académiques afin d’éviter la perte
										d’informations dans les groupes de messagerie
									</li>
								</ul>
								<p>
									MyISTA ne remplace pas les services officiels de l’ISTA, elle les complète. Elle a
									été développée par un étudiant de l’ISTA pour répondre à des problèmes concrets
									rencontrés sur le campus.
								</p>
								<p class="mt-6">
									À terme, elle pourra évoluer vers une solution intégrée au réseau interne de
									l’institut.
								</p>
							</div>

							<!-- Section Contact Profil Pro -->
							<div class="mt-10 pt-8 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-6">
								<div class="flex items-stretch gap-4 rounded-xl bg-slate-50 p-2 pr-6 border border-slate-100 shadow-sm transition-all hover:shadow-md">
									<div class="h-[72px] w-[72px] shrink-0 rounded-lg overflow-hidden bg-[#111] shadow-inner flex items-center justify-center">
										<img src={logoRodim} alt="Logo RODIMS-CODE" class="h-full w-full object-cover" />
									</div>
									<div class="flex flex-col justify-center py-1">
										<h5 class="font-extrabold text-slate-900 text-lg leading-none mb-1">RODIM'S Dieuveil</h5>
										<p class="text-[10px] sm:text-xs font-black tracking-widest text-[#0077b5] uppercase mb-1.5">RODIMS-CODE</p>
										<p class="text-xs font-semibold text-slate-500">Concepteur & Développeur Full-Stack</p>
									</div>
								</div>
								<div class="flex gap-3">
									<a href="https://www.linkedin.com/in/dieuveil-rodim-s-777a5b354/" target="_blank" rel="noopener noreferrer" class="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-slate-600 transition-all hover:-translate-y-1 hover:border-[#0A66C2] hover:bg-[#0A66C2] hover:text-white hover:shadow-lg hover:shadow-[#0A66C2]/30" title="LinkedIn">
										<Linkedin size={18} />
									</a>
									<a href="https://github.com/rodims-code" target="_blank" rel="noopener noreferrer" class="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-slate-600 transition-all hover:-translate-y-1 hover:border-slate-900 hover:bg-slate-900 hover:text-white hover:shadow-lg hover:shadow-slate-900/30" title="GitHub">
										<Github size={18} />
									</a>
									<a href="https://rodims.dev" target="_blank" rel="noopener noreferrer" class="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-slate-600 transition-all hover:-translate-y-1 hover:border-primary hover:bg-primary hover:text-white hover:shadow-lg hover:shadow-primary/30" title="Portfolio">
										<Globe size={18} />
									</a>
									<a href="ridrodims@gmail.com" class="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-slate-600 transition-all hover:-translate-y-1 hover:border-red-500 hover:bg-red-500 hover:text-white hover:shadow-lg hover:shadow-red-500/30" title="Email">
										<Mail size={18} />
									</a>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>

		<!-- Section Feedback avec effets lumineux -->
		<section id="feedback" class="relative overflow-hidden bg-slate-900 px-6 py-24 text-white">
			<!-- Glow effects background -->
			<div
				class="pointer-events-none absolute top-0 left-1/2 h-[60%] w-[60%] -translate-x-1/2 rounded-full bg-primary/20 blur-[150px]"
			></div>
			<div
				class="pointer-events-none absolute right-0 bottom-0 h-[40%] w-[40%] rounded-full bg-blue-500/10 blur-[120px]"
			></div>

			<div class="relative z-10 mx-auto max-w-3xl text-center">
				<div
					class="mb-6 inline-flex items-center justify-center rounded-2xl border border-white/10 bg-white/5 p-3 shadow-[0_0_15px_rgba(255,255,255,0.1)] backdrop-blur-sm"
				>
					<Sparkles size={28} class="animate-pulse text-primary" />
				</div>
				<h2 class="mb-6 text-3xl font-bold drop-shadow-md md:text-5xl">Votre avis compte !</h2>
				<p class="mb-12 text-lg text-slate-300">
					Un encouragement, une idée ou un retour ? Laissez-nous un message pour nous aider à
					améliorer <span class="font-semibold text-primary">MyISTA</span>.
				</p>

				<form
					class="mx-auto max-w-xl rounded-3xl border border-white/10 bg-white/5 p-8 text-left shadow-2xl shadow-primary/20 backdrop-blur-xl transition-all hover:shadow-primary/30"
				>
					{#if submitSuccess}
						<div class="alert alert-success mb-6 rounded-2xl border-none shadow-[0_0_15px_rgba(34,197,94,0.3)] bg-success/20 text-success-content backdrop-blur-sm">
							<span class="font-medium text-white">Merci pour votre message ! Nous l'avons bien reçu.</span>
						</div>
					{/if}
					
					{#if submitError}
						<div class="alert alert-error mb-6 rounded-2xl border-none shadow-[0_0_15px_rgba(239,68,68,0.3)] bg-error/20 text-error-content backdrop-blur-sm">
							<span class="font-medium text-white">{submitError}</span>
						</div>
					{/if}

					<div class="form-control mb-4">
						<label class="label"
							><span class="label-text text-slate-300">Nom complet (Optionnel)</span></label
						>
						<input
							type="text"
							bind:value={feedbackNom}
							placeholder="Comment vous appelez-vous ?"
							class="input-bordered input w-full border-white/10 bg-white/5 text-white shadow-[0_0_15px_rgba(59,130,246,0.1)] transition-all placeholder:text-slate-500 focus:border-primary focus:ring-1 focus:ring-primary"
						/>
					</div>
					<div class="form-control mb-6">
						<label class="label"><span class="label-text text-slate-300">Votre message</span></label
						>
						<textarea
							bind:value={feedbackMessage}
							class="textarea-bordered textarea h-32 w-full border-white/10 bg-white/5 text-white shadow-[0_0_15px_rgba(59,130,246,0.1)] transition-all placeholder:text-slate-500 focus:border-primary focus:ring-1 focus:ring-primary"
							placeholder="Écrivez votre encouragement ou feedback ici..."
						></textarea>
					</div>
					<button
						type="button"
						onclick={submitFeedback}
						disabled={isSubmitting || !feedbackMessage.trim()}
						class="group btn w-full shadow-lg shadow-primary/30 transition-all btn-primary hover:-translate-y-1 hover:shadow-primary/60 disabled:bg-primary/50 disabled:text-white/50"
					>
						{#if isSubmitting}
							<span class="loading loading-spinner loading-xs mr-2"></span>
						{:else}
							<Send
								size={18}
								class="mr-2 transition-transform group-hover:translate-x-1 group-hover:-translate-y-1"
							/>
						{/if}
						Envoyer le message
					</button>
				</form>
			</div>
		</section>

		<footer class="border-t border-slate-200 bg-slate-50 px-6 py-16">
			<div class="mx-auto grid max-w-6xl grid-cols-1 gap-12 md:grid-cols-4">
				<div class="col-span-1 md:col-span-2">
					<div class="mb-6 flex items-center gap-2">
						<div class="rounded-lg bg-primary p-1.5 text-white">
							<img src={logoIstaIcon} alt="Logo ISTA" class="h-15 w-15 object-cover" />
						</div>
						<span class="text-xl font-bold tracking-tight">MyISTA</span>
					</div>
					<p class="max-w-sm text-slate-500">
						Une plateforme académique intelligente au service de l'excellence de l'Institut
						Supérieur des Techniques Appliquées.
					</p>
				</div>
				<div>
					<h5 class="mb-4 font-bold">Navigation</h5>
					<ul class="space-y-2 text-slate-600">
						<li><a href="#problemes" class="hover:text-primary">Enjeux</a></li>
						<li><a href="#solutions" class="hover:text-primary">Fonctionnalités</a></li>
						<li><a href="#pitch" class="hover:text-primary">Pitch Officiel</a></li>
						<li><a href="#feedback" class="hover:text-primary">Nous contacter</a></li>
					</ul>
				</div>
				<div>
					<h5 class="mb-4 font-bold">Contact</h5>
					<ul class="space-y-2 text-slate-600">
						<li>Support étudiant</li>
						<li>Administration ISTA</li>
						<li>Portail de sécurité</li>
					</ul>
				</div>
			</div>
			<div
				class="mx-auto mt-12 flex max-w-6xl flex-col items-center justify-between gap-4 border-t border-slate-200 pt-8 text-sm text-slate-400 md:flex-row"
			>
				<p>© 2026 MyISTA. Conçu et développé avec passion par <a href="https://github.com/rodims-code" target="_blank" class="font-bold text-primary transition-colors hover:text-blue-600">Rodims</a> pour l'ISTA.</p>
				<div class="flex gap-6 italic">
					<span>Solution locale & évolutive</span>
				</div>
			</div>
		</footer>
	</main>
</div>

{#snippet problemCard(Icon, title, desc)}
	<div
		class="group rounded-3xl border border-slate-100 bg-slate-50 p-8 transition-all duration-300 hover:-translate-y-2 hover:bg-white hover:shadow-[0_0_30px_rgba(59,130,246,0.2)]"
	>
		<div
			class="mb-6 flex h-12 w-12 items-center justify-center rounded-2xl bg-white text-primary shadow-sm transition-all group-hover:bg-primary group-hover:text-white group-hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]"
		>
			<Icon size={24} />
		</div>
		<h4 class="mb-3 text-xl font-bold">{title}</h4>
		<p class="text-sm leading-relaxed text-slate-500">{desc}</p>
	</div>
{/snippet}

{#snippet solutionItem(Icon, title, desc)}
	<div
		class="group flex gap-6 rounded-2xl border border-transparent p-6 transition-all hover:border-white/10 hover:bg-white/5 hover:shadow-[0_0_20px_rgba(59,130,246,0.15)]"
	>
		<div
			class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/20 text-primary transition-all group-hover:scale-110 group-hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]"
		>
			<Icon size={24} />
		</div>
		<div>
			<h4 class="mb-1 text-lg font-bold text-white">{title}</h4>
			<p class="text-sm text-slate-400">{desc}</p>
		</div>
	</div>
{/snippet}

<style>
	:global(html) {
		scroll-behavior: smooth;
	}

	@keyframes float {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-10px);
		}
	}

	.animate-bounce-slow {
		animation: float 4s ease-in-out infinite;
	}
</style>
