---
id: contribuer
title: Comment contribuer
sidebar_label: Contribuer
sidebar_position: 2
---

# Comment contribuer à ce cadre de référence

Ce cadre de référence est hébergé sur GitLab et généré par Docusaurus. Toute
contribution est la bienvenue — correction d'une erreur, ajout d'un exemple,
documentation d'un nouveau dashboard, amélioration d'un guide.

---

## Petites corrections

Pour corriger une faute, une imprécision ou un lien cassé :

1. Ouvrir le fichier Markdown concerné sur GitLab
2. Cliquer sur **Edit** (icône crayon)
3. Effectuer la correction directement dans l'éditeur GitLab
4. Créer une merge request avec une description courte

---

## Contributions plus importantes

Pour ajouter une page, documenter un nouveau dashboard, ou proposer une évolution
d'un standard :

1. Cloner le repository
2. Créer une branche depuis `main` : `doc/[description-courte]`
3. Créer ou modifier les fichiers Markdown dans le bon répertoire
4. Vérifier le rendu localement avec `npm run start`
5. Créer une merge request vers `main` en assignant un membre de l'équipe plateforme

---

## Bonnes pratiques de rédaction

- Écrire en français, au présent, à la troisième personne ou à l'infinitif
- Rester factuel — éviter les formulations vagues comme "il est conseillé de…"
- Préférer des exemples concrets aux explications abstraites
- Utiliser les blocs Docusaurus avec parcimonie :
  - `:::note` pour une précision technique importante
  - `:::tip` pour un raccourci ou une recommandation
  - `:::warning` pour un piège ou une erreur fréquente
  - `:::danger` pour un antipattern à éviter absolument
- Ajouter des liens vers les sections connexes (`Référence croisée`)
- Ne pas dupliquer du contenu déjà présent ailleurs — faire un lien

---

## Structure des fichiers

```
docs/
└── [numéro]-[section]/
    ├── index.md            # Page d'entrée de la section (obligatoire)
    └── [numéro]-[page].md  # Pages de la section
```

Le numéro préfixé contrôle l'ordre d'affichage dans la sidebar Docusaurus.
Le `sidebar_position` dans le frontmatter doit être cohérent avec ce numéro.
