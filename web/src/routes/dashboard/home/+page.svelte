<script lang="ts">
	import { Sparkles, Clock3, ArrowRight, Instagram } from 'lucide-svelte';
</script>

<svelte:head>
	<title>Nouvelle feature bientôt disponible — MyISTA</title>
</svelte:head>

<div class="min-h-[calc(100vh-7rem)] flex items-center justify-center px-4 py-12">
	<div class="w-full max-w-4xl rounded-[2rem] border border-base-200/60 bg-base-100/95 p-8 shadow-2xl shadow-primary/10 backdrop-blur-xl">
		<div class="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
			<div class="space-y-6">
				<div class="inline-flex items-center gap-3 rounded-full bg-primary/10 px-4 py-2 text-sm font-semibold text-primary">
					<Instagram size={18} />
					Mode Insta-campus activé
				</div>

				<h1 class="text-4xl font-extrabold tracking-tight text-base-content sm:text-5xl">
					Cette feature arrive bientôt, reste connecté·e ✨
				</h1>

				<p class="max-w-2xl text-base text-base-content/70 sm:text-lg">
					On prépare un espace qui ressemble à Instagram, mais pensé pour la vibe étudiante MyISTA : partage de documents, ambiance visuelle moderne, et des surprises pour booster ton campus.
				</p>

				<div class="grid gap-4 sm:grid-cols-2">
					<div class="rounded-3xl border border-base-200 bg-base-200/70 p-5 shadow-sm">
						<div class="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary">
							<Sparkles size={20} />
						</div>
						<p class="font-semibold text-base-content">Design inspiré d’Instagram</p>
						<p class="mt-2 text-sm text-base-content/60">Look fluide, couleurs douces et layout mobile friendly.</p>
					</div>
					<div class="rounded-3xl border border-base-200 bg-base-200/70 p-5 shadow-sm">
						<div class="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-secondary/10 text-secondary">
							<Clock3 size={20} />
						</div>
						<p class="font-semibold text-base-content">Feature déjà en route</p>
						<p class="mt-2 text-sm text-base-content/60">On peaufine tout pour que ça arrive propre, rapide et fun.</p>
					</div>
				</div>

				<div class="flex flex-col gap-3 sm:flex-row sm:items-center">
					<a href="/dashboard/documents" class="btn btn-primary gap-2">
						<ArrowRight size={18} />
						Découvrir les documents
					</a>
					<span class="text-sm text-base-content/50">
						En attendant, explore les ressources académiques et reste à l’affût.
					</span>
				</div>
			</div>

			<div class="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-primary via-secondary to-accent p-8 text-white shadow-xl">
				<div class="absolute inset-0 bg-white/10"></div>
				<div class="relative space-y-6">
					<div class="rounded-3xl bg-white/10 p-5 backdrop-blur-sm">
						<p class="text-xs uppercase tracking-[0.25em] text-white/80">Nouveauté</p>
						<h2 class="text-3xl font-bold">Feed étudiant réinventé</h2>
					</div>

					<div class="grid gap-4">
						<div class="rounded-3xl border border-white/20 bg-white/10 p-4">
							<p class="text-sm text-white/80">Partage tes beaux moments au seins du campus, publie tes docs, swipe entre les contenus campus, ♥ like et partage.</p>
						</div>
						<div class="rounded-3xl border border-white/20 bg-white/10 p-4">
							<p class="text-sm text-white/80">Stay hype : mode stories et filtres de filière arrivent aussi bientôt.</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
