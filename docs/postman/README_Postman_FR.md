# Postman Scenarios – SoftDesk API

## Description

Cette collection Postman permet de tester l’ensemble des fonctionnalités de l’API SoftDesk.

Elle couvre :
- Authentification JWT
- Gestion des projets (CRUD)
- Gestion des contributeurs
- Gestion des issues
- Gestion des commentaires

## Environnements

Trois environnements sont utilisés pour simuler différents utilisateurs :

- Alice (auteur)
- Olivier (contributeur)
- Test_3 (utilisateur externe)

Chaque environnement contient :
- access_token
- refresh_token
- project_id
- issue_id
- comment_id
- contributor_id

## Authentification

Chaque utilisateur doit obtenir un token via :
POST /api/auth/token/

Le token est ensuite utilisé automatiquement dans les requêtes suivantes.

## Scénarios testés

### Cas nominaux
- Création de projet
- Ajout de contributeur
- Création d’issue
- Création de commentaire

### Cas d’erreur
- 401 : utilisateur non authentifié
- 403 : action non autorisée
- 404 : ressource inaccessible
- 400 : règles métier non respectées (ex : assignee non contributor)

## Pagination

La pagination est activée globalement :
- PAGE_SIZE = 10

Les réponses incluent :
- count
- next
- previous
- results

## Objectif

Démontrer :
- le bon fonctionnement de l’API
- le respect des règles métier
- la gestion des permissions
