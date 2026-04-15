# Postman Scenarios – SoftDesk API

## Description

This Postman collection is used to test all features of the SoftDesk API.

It covers:
- JWT authentication
- Project management (CRUD)
- Contributor management
- Issue management
- Comment management

## Environments

Three environments are used to simulate different users:

- Alice (author)
- Olivier (contributor)
- Test_3 (external user)

Each environment contains:
- access_token
- refresh_token
- project_id
- issue_id
- comment_id
- contributor_id

## Authentication

Each user must obtain a token via:
POST /api/auth/token/

The token is then automatically used in subsequent requests.

## Tested scenarios

### Success cases
- Project creation
- Adding contributor
- Issue creation
- Comment creation

### Error cases
- 401: unauthenticated user
- 403: unauthorized action
- 404: resource not found or inaccessible
- 400: business rule violation (e.g. assignee not contributor)

## Pagination

Pagination is globally configured:
- PAGE_SIZE = 10

Responses include:
- count
- next
- previous
- results

## Goal

To demonstrate:
- API functionality
- business rules enforcement
- permission management
