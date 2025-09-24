# 🔐 FastAPI Authentication Architecture (StockMind Project)


## 🧠 Summary

Authentication in FastAPI is declarative. You define:

* How to create and verify tokens (`JWTStrategy`)
* How users are stored and managed (`UserManager` + DB)
* What dependencies to inject into routes (`Depends(current_active_user)`)

And FastAPI **does the rest.**

---

## ⚙️ Authentication Flow (JWT + fastapi-users)

### 1. 🔐 **User logs in** (`POST /auth/jwt/login`)

* Sends email and password in request body
* FastAPI-Users:

  * Fetches user from DB via `get_user_db()`
  * Verifies password using `UserManager`
  * If valid → creates a JWT access token

### 2. 📦 **Token is returned**

* Stored in client (Authorization header, or cookie)
* Token contains encoded claims (e.g. user ID)

### 3. 📥 **Client makes authenticated requests**

* Adds header:

  ```http
  Authorization: Bearer <access_token>
  ```

### 4. 🧩 **FastAPI resolves dependencies**

* Route contains: `user: User = Depends(current_active_user)`
* FastAPI:

  * Reads Authorization header
  * Verifies JWT with your `JWTStrategy`
  * Extracts `user_id` from token
  * Calls `get_user_db()` → loads user
  * Injects user into route

### 5. 🎉 **Your route runs with the authenticated user**

---

## 📁 File Roles (StockMind Auth System)

| File         | Role                                                                                 |
| ------------ | ------------------------------------------------------------------------------------ |
| `models.py`  | SQLAlchemy user table (inherits from `SQLAlchemyBaseUserTable`)                      |
| `schemas.py` | Pydantic models for UserCreate and UserRead                                          |
| `manager.py` | Defines UserManager logic: registration hooks, secrets                               |
| `db.py`      | Creates the SQLAlchemyUserDatabase adapter                                           |
| `deps.py`    | Defines auth backend, JWT strategy, FastAPIUsers instance, and `current_active_user` |
| `auth.py`    | Includes actual routes: `/auth/jwt/login`, `/auth/register`, `/users/me`             |
| `main.py`    | Includes `auth.router` in the app                                                    |

---

## 🔑 Key Classes & Functions

### `UserManager`

* Subclass of `BaseUserManager`
* Handles logic after registration, password reset, etc.
* Defines `SECRET` used to sign tokens

### `JWTStrategy`

* Defines how tokens are created/verified
* You pass a `SECRET` and expiration time

### `AuthenticationBackend`

* Combines transport + strategy
* In your case: Bearer tokens via headers

### `FastAPIUsers`

* Main glue class that connects:

  * User DB adapter
  * Auth backend(s)
  * Pydantic schemas
  * User manager

### `Depends(current_active_user)`

* FastAPI injects this user into any route
* Only active users are allowed (can customize if needed)

---

## ✅ Registering Auth Routes

```python
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_users_router(UserRead),
    prefix="/users",
    tags=["users"]
)
```

---

## 🛡️ Example Protected Route

```python
from fastapi import APIRouter, Depends
from app.users.deps import current_active_user
from app.users.models import User

router = APIRouter()

@router.get("/me")
async def read_current_user(user: User = Depends(current_active_user)):
    return user
```

✅ Only logged-in users with valid tokens will get access.

---

## 💡 Dev Tips

* Set `SECRET` in `.env` for security
* Use `BearerTransport` (headers) or `CookieTransport` (browser cookies)
* Customize `UserManager` to send email, log events, etc.
* Use `UserUpdate` schema to allow profile editing
* Use `current_user(active=True, verified=True)` for extra checks

---

## 📚 Learn More

* [FastAPI Users Docs](https://fastapi-users.github.io/fastapi-users/12.1/)
* [Pydantic Docs](https://docs.pydantic.dev/)
* [JWT (RFC 7519)](https://datatracker.ietf.org/doc/html/rfc7519)

---

✅ This doc is your reference. Read it again whenever you build a new auth system in FastAPI.
