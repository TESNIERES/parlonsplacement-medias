# Consignes de production - Parlons Placement

Ce dépôt héberge les images des publications Instagram de @parlonsplacement et le moteur qui les fabrique. Chaque exécution de la tâche quotidienne suit ces consignes à la lettre.

## Mission d'une exécution

Préparer, publier dans ce dépôt et programmer dans Metricool **un sujet** pour le prochain jour libre, décliné en trois formats le même jour (heure de Paris) :

- **08:47** : le carrousel (type `POST`), pour le profil et les enregistrements ;
- **08:52** : la story qui l'annonce (type `STORY`) ;
- **12:31** : le Reel tiré du carrousel (type `REEL`). C'est le format qui touche les personnes qui ne nous suivent pas encore : **il est obligatoire**, c'est lui qui fait venir les abonnés.

Un sujet par jour, jamais deux carrousels le même jour.

## Les étapes

1. **Mise en route.** `pip install --break-system-packages pillow playwright` si besoin (Chromium et Playwright sont normalement préinstallés : ne pas lancer `playwright install`).
2. **Lire** `calendrier.md` (prochain sujet « À faire »), `journal.md` (dernier numéro utilisé, ce qui est déjà programmé) et ce fichier.
3. **Trouver le jour cible.** Metricool `getScheduledPosts` (brandId `7804054`, timezone `Europe/Paris`) sur les 8 prochains jours. Le jour cible est le premier jour, à partir de demain, sans **carrousel** (type `POST`) programmé. Les Reels et les stories déjà programmés ne rendent pas un jour « occupé ».
4. **Rattrapage d'abord.** Si un dossier de `publications/` est marqué « Prêt » dans `journal.md` mais pas « Programmé », le programmer sur le jour cible au lieu de produire un nouveau sujet. Ne produire qu'une publication par exécution.
5. **Vérifier les faits** sur une source primaire : service-public.gouv.fr, impots.gouv.fr, banque-france.fr, insee.fr, amf-france.org, legifrance.gouv.fr, info.gouv.fr, economie.gouv.fr, drees.solidarites-sante.gouv.fr. Noter pour chaque chiffre l'URL et la date de vérification. **Un fait non vérifiable = on change de sujet** (prendre le suivant du calendrier).
6. **Rédiger et maquetter** 5 à 8 pages avec `moteur/ed.py` et `moteur/ed_extra.py`, en partant des exemples `moteur/exemples/`. Créer `moteur/posts/post_NXXX.py`. Varier les gabarits d'une page à l'autre (une, règle, si/alors, chiffre, source, à retenir, colophon).
7. **Rendu** : `python3 moteur/posts/post_NXXX.py /tmp/NXXX` puis conversion de chaque PNG en JPEG qualité 92, sans sous-échantillonnage (`subsampling=0`), dans `publications/NXXX-slug/` (`slug-01.jpg`, `slug-02.jpg`…). Écrire `publications/NXXX-slug/legende.txt`.
8. **Relecture obligatoire** : ouvrir chaque image et vérifier orthographe, chiffres, typographie française (espaces insécables, 1ᵉʳ en exposant), absence de tiret cadratin, sources en notes, colophon complet, mention pédagogique.
9. **Publier dans le dépôt** : `git add`, `git commit` (auteur `Parlons Placement <parlonsplacement@users.noreply.github.com>`), `git push`.
10. **Programmer dans Metricool** avec `createScheduledPost` :
    - `blogId` : `7804054`
    - `date` : `AAAA-MM-JJT08:47:00+01:00` (heure d'hiver) ou `+02:00` (heure d'été)
    - `info.publicationDate` : `{"dateTime": "AAAA-MM-JJT08:47:00", "timezone": "Europe/Paris"}`
    - `info.providers` : `[{"network": "instagram"}]`, `info.instagramData` : `{"type": "POST"}`
    - `info.media` : les URL figées sur le commit poussé, `https://raw.githubusercontent.com/TESNIERES/parlonsplacement-medias/<SHA complet de git rev-parse HEAD>/publications/NXXX-slug/slug-01.jpg`… dans l'ordre des pages (jamais `main` : le cache de GitHub peut servir une ancienne image). Vérifier avec `curl` que la première URL répond 200.
    - `info.text` : le contenu de `legende.txt` ; `autoPublish` : true ; `draft` : false
11. **La story du jour.** `python3 moteur/story.py /tmp/NXXX/slug-01.png "<rubrique>" "<titre court, un passage en <em>>" /tmp/NXXX/story.png`, convertir en `publications/NXXX-slug/story-01.jpg` (JPEG qualité 92), relire, pousser, puis `createScheduledPost` avec `info.instagramData` : `{"type": "STORY"}`, **sans champ text**, le même jour à **08:52** (5 minutes après le post), média = URL figée sur le commit. Une story par post, pas plus.
12. **Le Reel du jour** (obligatoire).
    - `python3 moteur/reel.py publications/NXXX-slug "<rubrique>" "<titre de la une, un passage en <em>>"`. Dans le titre, espaces insécables avant `:` `?` `!` (` `) et milliers en `1<span style="margin-left:.12em"> </span>000` (l'espace fine seule disparaît en Instrument Serif). Le script crée `reel.mp4` (9:16, environ 28 s : couverture, pages 2 à 8, page de fin « Une fiche sourcée par jour ») et `reel-couverture.jpg`.
    - **Relire** : extraire 3 images (`ffmpeg -ss 1`, `-ss 6`, `-ss` fin moins 1 s, `-frames:v 1`) et les ouvrir. Vérifier qu'aucun titre ne se coupe au milieu d'un nombre.
    - Écrire `publications/NXXX-slug/reel.txt` selon la « Légende de Reel » ci-dessous, pousser, puis `createScheduledPost` le même jour à **12:31** : `info.instagramData` : `{"type": "REEL", "showReelOnFeed": true}`, `info.media` : l'URL figée de `reel.mp4`, `info.videoThumbnailUrl` : l'URL figée de `reel-couverture.jpg`, `info.text` : `reel.txt`.
    - Si un carrousel déjà publié n'a pas encore de Reel (`journal.md`), en faire un aussi et le programmer à **19:01** le premier jour où ce créneau est libre. Un rattrapage par exécution au plus.
13. **Mettre à jour** `journal.md` (numéro, date de publication, sujet, sources, statut « Programmé », liens Metricool du carrousel, de la story et du Reel) et `calendrier.md`, puis commit et push.
14. **Le lundi** : relever la croissance dans `croissance.md` (voir plus bas), puis appliquer ce qu'elle enseigne aux sujets et aux accroches de la semaine.
15. **Résumé final** en 5 lignes : sujet, jour et heures programmés, sources, liens Metricool, et toute alerte.

**En cas de blocage** (push refusé, erreur Metricool, source introuvable, rendu raté) : ne rien programmer, expliquer précisément le blocage dans le résumé.

## Photos réelles

Deux publications par semaine au moins portent une vraie photo, en page 2 du carrousel :

- `search_photos` sur Unsplash (requête courte et concrète : « keys on table », « grocery receipt »), choisir une photo de lieu, d'objet ou de scène. **Jamais une personne présentée comme témoin.**
- `download_asset` sur la photo retenue (obligatoire pour Unsplash), puis utiliser comme média l'URL `urls.raw` suivie de `&w=1080&h=1350&fit=crop&fm=jpg&q=85` pour obtenir exactement le format 4:5 du carrousel.
- Crédit dans la légende et dans le colophon : « Photo : Prénom Nom / Unsplash ».

## Ligne éditoriale

- Des sujets **concrets et universels** : livrets, loyer, crédit, impôts, retraite, frais bancaires, inflation, assurance-vie, bourse, immobilier, arnaques. Toujours l'angle « ce que ça change pour toi ».
- **Tutoiement**, phrases courtes, 45 mots maximum par page, chaque terme technique expliqué. Vouvoiement uniquement pour la rubrique Côté CGP.
- **Décrire, jamais prescrire.** Jamais « achète », « vends », « mets ton argent dans », « le meilleur placement ». Aucune promesse de rendement. Aucun produit ni établissement mis en avant.
- Si un placement risqué est évoqué : « Investir comporte un risque de perte en capital » sur la page concernée.
- Dernière page : colophon avec toutes les sources et la mention « Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé. »
- Actualité : titre exact entre guillemets, source, date, lien en légende. Jamais la photo d'un article. Jamais de photo de personnalité.

## Style Édition (ne pas dévier)

- Une publication = une page de journal : bandeau avec le logo et le filet double (**jamais de numéro de post ni de date dans le bandeau**, ça fait artificiel), rubrique avec pavé lime, titres en Instrument Serif, texte en Inter, notes de sources numérotées, folio « 3 / 8 → ».
- 80 % papier, 15 % sapin, 5 % lime. Une page sapin maximum, deux dans les longs formats.
- **Interdits** : numéro de post ou date dans l'en-tête, pastilles arrondies, boutons ronds, flèches dessinées, barres de progression, cartes à icônes, emoji, dégradés, surligneur fluo, images générées par IA, mise en page identique sur toutes les pages.

## Gagner des abonnés qualifiés

Le compte part de zéro : Instagram ne montre presque rien d'un compte sans abonnés, sauf ses Reels. Chaque publication doit donc donner à un inconnu une raison de **s'arrêter, enregistrer, partager, puis s'abonner**.

- **Le sujet** : une vraie question que se posent les 20-40 ans et les épargnants qui débutent, ou un chiffre qui surprend, ou une idée reçue corrigée. Le calendrier alterne ces trois familles. Un sujet trop abstrait pour être envoyé à un proche passe après.
- **L'accroche** (titre de la une, première ligne des légendes, couverture du Reel) : concrète, au tutoiement, avec le mot que les gens tapent dans la recherche (« Livret A », « LEP », « impôts », « crédit immobilier »). Formes qui marchent : la situation (« Verser le 15 ou le 16 sur ton Livret A, ce n'est pas pareil »), le chiffre (« 1 000 € en 2015, 1 209,50 € en 2025 »), le droit méconnu (« Ta banque doit te rembourser d'abord »). Jamais d'accroche alarmiste, jamais de promesse de gain.
- **L'appel à l'action**, une seule phrase avant les sources, varié d'un jour à l'autre : enregistrer (« Enregistre-le pour ta déclaration »), partager (« Envoie-le à quelqu'un qui… »), commenter (une question fermée simple), suivre (« Suis @parlonsplacement : une fiche sourcée par jour »).
- **Hashtags** : 4 à 5, précis et en français : 1 ou 2 du sujet (#livretA, #impots, #creditimmobilier), puis #epargne ou #financespersonnelles, puis #educationfinanciere. Jamais de hashtags génériques en anglais ni de liste de 30.
- **Interdits** : acheter des abonnés ou des likes, suivre et ne plus suivre en masse, groupes d'engagement, jeux-concours. Ces pratiques font venir un public non qualifié et Instagram les pénalise.

## Croissance (le lundi)

Relever dans Metricool (`getAnalyticsDataByMetrics`, brandId `7804054`) sur les 7 derniers jours : abonnés (`IGEV01`), abonnés gagnés (`IGEV43`), portée du compte (`IGEV06`), et pour chaque Reel (`IGRE11` portée, `IGRE23` vues, `IGRE24` durée moyenne de visionnage, `IGRE21` partages, `IGRE12` enregistrements) et chaque carrousel (`IGPO14`, `IGPO15`, `IGPO27`, `IGPO29` abonnements). Ajouter une ligne à `croissance.md`, puis noter en une phrase ce qui a le mieux marché (sujet, accroche, format) et le reproduire dans les sujets suivants du calendrier.

## Légende type

```
[Accroche : la phrase qui donne envie de lire, avec le mot clé du sujet]

[2 à 4 phrases qui résument l'essentiel, factuelles.]

[Un appel à l'action : enregistrer, partager, commenter ou suivre.]

Sources :
[url courte] ([date de vérification])

Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.

#[4 à 5 hashtags précis, en français]
```

## Légende de Reel

Plus courte que celle du carrousel, mêmes faits, mêmes sources (exemples : `publications/N002-livret-a-quinzaines/reel.txt`, `N004-inflation-1000-euros/reel.txt`).

```
[Accroche en une ligne, différente du titre du carrousel]

[2 ou 3 phrases factuelles, puis « le détail est dans la vidéo ».]

[Appel à l'action] Suis @parlonsplacement : une fiche sourcée par jour.

Sources :
[url courte] ([date de vérification])

Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.

#[4 à 5 hashtags précis, en français]
```
