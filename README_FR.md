# SoftDesk Support (API de suivi de bugs)

## Présentation

SoftDesk Support est une API REST sécurisée développée avec **Django** et **Django REST Framework**.

Les utilisateurs authentifiés peuvent gérer :
- des projets
- des contributeurs
- des issues
- des commentaires

L’authentification repose sur **JWT**, les permissions sont appliquées à la fois au niveau de l’accès et des objets, et les listes de ressources sont **paginées** par défaut. L’application inclut également un endpoint de profil conforme au RGPD pour consulter, modifier et supprimer les données utilisateur.

## Fonctionnalités

- Authentification JWT (`access` / `refresh`)
- Accès aux projets limité aux contributeurs
- Modification / suppression réservées à l’auteur pour `Project`, `Issue` et `Comment`
- Gestion des contributeurs par projet
- Issues avec :
  - priorité (`LOW`, `MEDIUM`, `HIGH`)
  - balise (`BUG`, `FEATURE`, `TASK`)
  - statut (`TO_DO`, `IN_PROGRESS`, `FINISHED`)
  - assignation optionnelle limitée aux contributeurs du projet
- Commentaires liés aux issues
- UUID généré automatiquement pour les commentaires
- Pagination globale
- Endpoint profil RGPD :
  - accès aux données personnelles
  - mise à jour des consentements
  - suppression du compte

## Stack technique

- Python 3.10+
- Django 4.2+
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- SQLite (développement)

## Installation

```bash
git clone https://github.com/AlNocquet/OC-Projet10-Softdesk.git
cd OC-Projet10-Softdesk
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Variables d’environnement

Créer un fichier `.env` à la racine du projet à partir du fichier `.env.example`.

Exemple :

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
```


Vérification rapide :
GET http://127.0.0.1:8000/health/

Réponse attendue :
{"status":"ok","app":"softdesk"}

## Authentification (JWT)

POST http://127.0.0.1:8000/api/auth/token/

{
  "username": "<utilisateur>",
  "password": "<mot_de_passe>"
}

POST http://127.0.0.1:8000/api/auth/token/refresh/

Authorization: Bearer <ACCESS_TOKEN>

## Carte de l’API

/api/auth/token/                             POST
/api/auth/token/refresh/                     POST

/api/projects/                               GET, POST
/api/projects/{id}/                          GET, PATCH, DELETE

/api/projects/{id}/contributors/             GET, POST
/api/projects/{id}/contributors/{id}/        DELETE

/api/projects/{project_id}/issues/           GET, POST
/api/projects/{project_id}/issues/{id}/      GET, PATCH, DELETE

/api/projects/{project_id}/issues/{issue_id}/comments/        GET, POST
/api/projects/{project_id}/issues/{issue_id}/comments/{id}/   PATCH, DELETE

/api/profile/                                GET, PATCH, DELETE

## Permissions

- Tous les endpoints API nécessitent une authentification (sauf /health)
- Un projet est visible uniquement par ses contributeurs
- Un contributeur peut consulter les ressources du projet
- Seul l’auteur d’un Project, Issue ou Comment peut modifier ou supprimer
- Seul l’auteur du projet peut gérer les contributeurs

## RGPD

GET    /api/profile/
PATCH  /api/profile/
DELETE /api/profile/

Données gérées :
- age
- can_be_contacted
- can_data_be_shared

Règles :
- âge >= 15 ans
- accès et modification des données personnelles
- suppression du compte utilisateur

## Pagination

L’API utilise la pagination globale de Django REST Framework :

- Type : PageNumberPagination
- Taille : 10 éléments par page

Exemple :
GET /api/projects/?page=2

## Sécurité (AAA)

L’API suit le modèle AAA :

- **Authentification** :
  - Authentification JWT avec tokens access et refresh

- **Autorisation** :
  - Accès réservé aux utilisateurs authentifiés
  - Données accessibles uniquement aux contributeurs
  - Modifications réservées aux auteurs des ressources

- **Accounting (traçabilité)** :
  - Gestion de base assurée par Django
  - Une journalisation avancée des actions pourrait être ajoutée en production

## Structure du projet

```
config/         # configuration Django et urls
core/           # health, ping, profil RGPD
projects/       # logique métier
```

## Tests

L’API a été testée avec :

- Postman (tests principaux avec JWT et environnements)
- Django test files (tests.py) pour validation automatisée minimale

Postman a permis de simuler des interactions réelles (authentification, permissions, opérations CRUD), tandis que les tests Django assurent une vérification de base du comportement de l’application.

## Auteur

Alice Nocquet
https://github.com/AlNocquet
