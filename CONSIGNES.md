# Consignes de production - Parlons Placement

Ce dépôt héberge les images des publications Instagram de @parlonsplacement et le moteur qui les fabrique. Chaque exécution de la tâche quotidienne suit ces consignes à la lettre.

## Mission d'une exécution

Préparer, publier dans ce dépôt et programmer dans Metricool **une** publication Instagram pour le prochain jour libre, à **8 h 47 heure de Paris**. Un post par jour, jamais deux le même jour.

## Les étapes

1. **Mise en route.** `pip install --break-system-packages pillow playwright` si besoin (Chromium et Playwright sont normalement préinstallés : ne pas lancer `playwright install`).
2. **Lire** `calendrier.md` (prochain sujet « À faire »), `journal.md` (dernier numéro utilisé, ce qui est déjà programmé) et ce fichier.
3. **Trouver le jour cible.** Metricool `getScheduledPosts` (brandId `7804054`, timezone `Europe/Paris`) sur les 8 prochains jours. Le jour cible est le premier jour, à partir de demain, sans publication Instagram programmée.
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
    - `info.media` : les URL `https://raw.githubusercontent.com/TESNIERES/parlonsplacement-medias/main/publications/NXXX-slug/slug-01.jpg`… dans l'ordre des pages
    - `info.text` : le contenu de `legende.txt` ; `autoPublish` : true ; `draft` : false
11. **Mettre à jour** `journal.md` (numéro, date de publication, sujet, sources, statut « Programmé », lien Metricool) et `calendrier.md`, puis commit et push.
12. **Résumé final** en 5 lignes : sujet, jour et heure programmés, sources, lien Metricool, et toute alerte.

**En cas de blocage** (push refusé, erreur Metricool, source introuvable, rendu raté) : ne rien programmer, expliquer précisément le blocage dans le résumé.

## Ligne éditoriale

- Des sujets **concrets et universels** : livrets, loyer, crédit, impôts, retraite, frais bancaires, inflation, assurance-vie, bourse, immobilier, arnaques. Toujours l'angle « ce que ça change pour toi ».
- **Tutoiement**, phrases courtes, 45 mots maximum par page, chaque terme technique expliqué. Vouvoiement uniquement pour la rubrique Côté CGP.
- **Décrire, jamais prescrire.** Jamais « achète », « vends », « mets ton argent dans », « le meilleur placement ». Aucune promesse de rendement. Aucun produit ni établissement mis en avant.
- Si un placement risqué est évoqué : « Investir comporte un risque de perte en capital » sur la page concernée.
- Dernière page : colophon avec toutes les sources et la mention « Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé. »
- Actualité : titre exact entre guillemets, source, date, lien en légende. Jamais la photo d'un article. Jamais de photo de personnalité.

## Style Édition (ne pas dévier)

- Une publication = une page de journal : bandeau de titre (logo, N°, mois, filet double), rubrique avec pavé lime, titres en Instrument Serif, texte en Inter, notes de sources numérotées, folio « 3 / 8 → ».
- 80 % papier, 15 % sapin, 5 % lime. Une page sapin maximum, deux dans les longs formats.
- **Interdits** : pastilles arrondies, boutons ronds, flèches dessinées, barres de progression, cartes à icônes, emoji, dégradés, surligneur fluo, images générées par IA, mise en page identique sur toutes les pages.

## Légende type

```
[Titre de la une]

[2 à 4 phrases qui résument l'essentiel, factuelles.]

Sources :
[url courte] ([date de vérification])

Contenu pédagogique. Ne constitue pas un conseil en investissement personnalisé.

#[3 à 4 hashtags sobres]
```
