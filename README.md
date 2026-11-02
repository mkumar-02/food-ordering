# Food Ordering API

Build a working FastAPI service that lets customers browse restaurants, place orders, and track them. Restaurant owners manage menus and order status.

This repo starts empty. You implement everything listed below.

## Tech stack

Use what you learned in the course:

- Python 3.11+
- FastAPI
- Pydantic for request/response schemas
- SQLAlchemy or SQLModel
- SQLite for local development
- JWT authentication (OAuth2 password flow)
- Passlib / bcrypt for password hashing

A frontend is **not** required. Swagger UI (`/docs`) is enough to demo the APIs.

---

## What you have to complete

Work through these five items in order. Each one is a required deliverable.

### 1. Features of the application

Implement all of the following. Mark each as done in your own notes when it works end to end.

**Users and roles**

- [ ] Register and login
- [ ] Three roles: `customer`, `restaurant_owner`, `admin`
- [ ] Customer can view their own profile
- [ ] Admin can list users

**Restaurants and menu**

- [ ] List restaurants (name, cuisine, address, open/closed)
- [ ] Get one restaurant with its menu
- [ ] Restaurant owner can create/update their restaurant
- [ ] Restaurant owner can add, update, and disable menu items (name, description, price, available flag)
- [ ] Customers can only order items that are available

**Orders**

- [ ] Customer can create an order from one restaurant (items + quantities)
- [ ] Customer can view their order history and a single order
- [ ] Order has a status: `placed` → `confirmed` → `preparing` → `out_for_delivery` → `delivered`
- [ ] Customer can cancel an order only while it is `placed` or `confirmed`
- [ ] Restaurant owner can move the order to the next valid status
- [ ] Admin can view all orders

Do **not** build payments, delivery tracking on a map, or a cart that lives across sessions. Keep the order payload on `POST /orders`.

### 2. Business logic

Put rules in a service layer (not only inside route functions). The API must reject invalid actions with a clear error.

- [ ] An order can contain items from **one restaurant only**
- [ ] Ordered items must belong to that restaurant and must be `available`
- [ ] Quantity must be at least 1
- [ ] Restaurant must be open to accept a new order
- [ ] Order total = sum of `(unit_price * quantity)` using the **price at order time** (later menu price changes must not change old orders)
- [ ] Optional: reject orders below a minimum amount (e.g. 100)
- [ ] Status can only move **forward** along the flow above (no skipping, no going backwards)
- [ ] Customer cannot cancel after `preparing`
- [ ] Restaurant owner can manage **only their own** restaurant, menu, and orders
- [ ] Customer can read **only their own** orders

Write a short `BUSINESS_RULES.md` (or a section in your PR) listing these rules and which function enforces each one.

### 3. API design

Design REST APIs before you code. Keep resource names plural, use proper HTTP methods, and return consistent JSON.

Suggested shape (you may refine names, but keep this coverage):

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `POST` | `/auth/register` | public | Create user |
| `POST` | `/auth/login` | public | Get access token |
| `GET` | `/users/me` | logged in | Current user |
| `GET` | `/restaurants` | public | List restaurants |
| `GET` | `/restaurants/{id}` | public | Restaurant + menu |
| `POST` | `/restaurants` | restaurant_owner | Create restaurant |
| `PATCH` | `/restaurants/{id}` | owner / admin | Update restaurant |
| `POST` | `/restaurants/{id}/menu-items` | owner | Add menu item |
| `PATCH` | `/menu-items/{id}` | owner | Update / disable item |
| `POST` | `/orders` | customer | Place order |
| `GET` | `/orders` | customer: own, admin: all, owner: their restaurant | List orders |
| `GET` | `/orders/{id}` | owner of the order / restaurant / admin | Order detail |
| `POST` | `/orders/{id}/cancel` | customer | Cancel |
| `POST` | `/orders/{id}/status` | restaurant_owner | Next status |

Requirements:

- [ ] Request and response models with Pydantic (no raw dicts as API contract)
- [ ] Path vs query vs body used correctly (ids in the path, filters in query)
- [ ] Pagination on list endpoints (`skip` / `limit` or `page` / `size`)
- [ ] OpenAPI tags so `/docs` is readable
- [ ] Status codes: `201` on create, `200` on read/update, `204` only if you return no body
- [ ] Include a sample request/response for each endpoint in `/docs` (Pydantic examples or a `requests.http` file)

### 4. Error handling

Do not leak stack traces. Every failure should be a JSON body the client can display.

- [ ] One error response shape, for example: `{ "detail": "...", "code": "ORDER_NOT_CANCELLABLE" }`
- [ ] Custom exceptions for business rules (not generic `Exception`)
- [ ] FastAPI exception handlers for those exceptions
- [ ] `401` when token is missing or invalid
- [ ] `403` when the user is logged in but not allowed
- [ ] `404` when restaurant, menu item, or order does not exist
- [ ] `400` or `409` for rule violations (closed restaurant, invalid status change, mixed-restaurant order)
- [ ] `422` for Pydantic validation (invalid types, missing fields, quantity `< 1`)
- [ ] Do not return SQL errors or internal paths to the client

Add a few failing examples in `/docs` or a short `ERROR_CASES.md`.

### 5. Authentication

- [ ] `POST /auth/register` stores a **hashed** password (never plain text)
- [ ] `POST /auth/login` returns a JWT access token
- [ ] Protected routes use `Authorization: Bearer <token>`
- [ ] Dependency for `get_current_user`
- [ ] Role checks: customer vs restaurant owner vs admin
- [ ] Public routes: register, login, list/get restaurants
- [ ] Token expiry (e.g. 30–60 minutes)
- [ ] Secrets in `.env`, not in source (keep `.env.example` with dummy values)
