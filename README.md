# jam-ng
Angular 2 Jam -----

## title: Security Trimming
sidebar_label: Security Trimming
sidebar_position: 1
tags: [sécurité, habilitations, front, back, pattern]

# Security Trimming

## Problème

Lorsqu’un utilisateur dispose d’habilitations partielles sur des types de comptes ou de ressources, l’IHM peut proposer des actions ou des onglets que l’API refusera avec un `403 Forbidden`.

Ces erreurs 403 **ne sont pas de vraies anomalies applicatives** : elles résultent d’une désynchronisation entre ce que l’IHM propose et ce que le back-end autorise réellement. Elles polluent les logs, les dashboards APM et faussent les alertes.

## Solution : Security Trimming

Le security trimming consiste à **charger les habilitations de l’utilisateur en amont**, puis à n’afficher que les éléments de l’interface auxquels il a accès. L’utilisateur ne peut pas déclencher un appel voué à échouer.

```
Authentification → Chargement des habilitations → Filtrage de l'IHM → Appels API toujours autorisés
```

:::info Origine du pattern
Le terme *security trimming* est notamment connu via SharePoint, mais le concept s’applique à tout système exposant une interface conditionnée par des droits utilisateur.
:::

-----

## Mise en œuvre

### 1. Endpoint d’habilitations (Back-end)

Exposer un endpoint dédié, appelé une fois à l’authentification ou au chargement de l’application :

```http
GET /api/v1/me/habilitations
Authorization: Bearer <token>
```

```json
{
  "accountTypes": ["COURANT", "EPARGNE"]
}
```

La réponse doit exprimer des **capacités UI** — ce que l’utilisateur peut consulter — et non les règles ou rôles internes du système d’autorisation.

### 2. Stockage côté IHM (Front-end)

Les habilitations sont stockées dans le state applicatif dès leur réception (store Redux, contexte Angular, composable Vue, etc.) et rendues disponibles à tous les composants concernés.

### 3. Filtrage des composants

Chaque onglet, filtre ou action sensible est conditionné à la présence du droit correspondant :

```jsx
// React — exemple
{habilitations.accountTypes.includes("PEA") && <OngletPEA />}
```

```typescript
// Angular — exemple
<app-onglet-pea *ngIf="habilitations.accountTypes.includes('PEA')" />
```

-----

## Contrat entre Back et Front

|Responsabilité                  |Back-end                      |Front-end|
|--------------------------------|------------------------------|---------|
|Vérifier les droits             |✅ Toujours (source de vérité) |✗        |
|Exposer les capacités UI        |✅ Endpoint `/me/habilitations`|✗        |
|Filtrer l’affichage             |✗                             |✅        |
|Bloquer les appels non autorisés|✅ Retourner 403 si bypass     |✗        |

:::warning Defense in depth
Le security trimming est une mesure **UX et de réduction du bruit**, pas une mesure de sécurité à part entière. L’API **doit toujours** contrôler les droits et retourner `403` si un appel non autorisé est émis — notamment en cas de bypass direct de l’IHM.
:::

-----

## Conception de l’endpoint d’habilitations

### Ce qu’il faut exposer

L’endpoint doit retourner uniquement la **liste positive** des types autorisés pour l’utilisateur courant.

```json title="✅ Réponse attendue"
{
  "accountTypes": ["COURANT", "EPARGNE"]
}
```

### Ce qu’il ne faut pas exposer

:::danger Ne pas exposer le modèle de droits interne
Éviter d’inclure dans la réponse tout élément révélant le fonctionnement interne du système d’autorisation.

```json title="❌ À ne pas faire"
{
  "roles": ["ROLE_GESTIONNAIRE_PATRIMOINE"],
  "policies": ["POL_EPARGNE_READ", "POL_COURANT_WRITE"],
  "reason": "client segment PREMIUM autorisé par règle R-042"
}
```

Ces informations permettraient à un attaquant de reconstituer le modèle de droits, de cibler ses attaques ou de forger des requêtes malveillantes.
:::

:::danger Ne pas lister les types interdits
Retourner une liste exhaustive avec un statut `true/false` expose la surface complète du système.

```json title="❌ À ne pas faire"
{
  "COURANT": true,
  "EPARGNE": true,
  "PEA": false,
  "TITRES": false
}
```

L’IHM n’a pas besoin de savoir ce qui est interdit — uniquement ce qui est autorisé.
:::

-----

## Bonnes pratiques

:::tip Authentification stricte
L’endpoint `/me/habilitations` ne doit jamais répondre sans token valide. Il retourne les droits de l’utilisateur **du token courant**, jamais d’un utilisateur passé en paramètre.
:::

:::tip Cache court côté IHM
Les habilitations peuvent changer (révocation, changement de segment client). Prévoir une durée de vie courte si elles sont mises en cache côté front, ou les recharger à chaque ouverture de session.
:::

:::tip Source de vérité unique
L’endpoint doit être dérivé du **même référentiel** que les contrôles d’accès de l’API. Une désynchronisation entre ce que l’IHM cache et ce que l’API autorise génère soit des 403 résiduels, soit des accès à tort.
:::

:::tip Parler le langage de l’IHM
Les valeurs retournées (`"COURANT"`, `"EPARGNE"`, etc.) doivent correspondre aux identifiants utilisés côté front pour conditionner l’affichage — pas aux codes internes du référentiel métier.
:::

-----

## Bénéfices

- **Zéro 403 parasite** dans les logs APM et ELK — seules les vraies anomalies remontent
- **UX propre** — l’utilisateur ne voit jamais une action qu’il ne peut pas effectuer
- **Alerting fiable** — un 403 dans les logs signifie désormais un vrai problème (bypass, token expiré, bug)
- **Découplage** — l’IHM ne connaît pas le moteur d’autorisation, seulement ses capacités d’affichage


