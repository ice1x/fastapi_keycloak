# FastAPI & Keycloak & Vue integration

```plaintext
project/
│
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
|   └── src/
│       └── main.py        ← FastAPI
│
└── frontend/
    ├── Dockerfile
    └── src/
        └── main.js     ← Vue + keycloak-js
```


# Keycloak setup:
1. Login with `admin:admin`
2. Create new realm: `demo-realm`
3. Create new client: `frontend-client`
   - Client type: `Public`
   - Root URL: `http://localhost:5173`
   - Valid redirect URIs: `http://localhost:5173/*`
   - Web origins: `http://localhost:5173`
   - Save

4. In client `frontend-client` settings:
   - Make sure **Standard Flow Enabled** is ON
   - Set **Access Type** to `public`
   - Ensure **Full Scope Allowed** is ON

5. Add a role:
   - Go to `Roles`, create new role: `admin`

6. Create user:
   - Go to `Users`, add new user (e.g. `admin`)
   - Set credentials manually (e.g. `admin:admin`)
   - In `Role Mappings`, assign `admin` role to this user

7. Token must contain `realm_access.roles` with `admin`, and audience must match `frontend-client`
   - To ensure correct audience claim (`aud`), go to `Client Scopes`
   - Create a new scope or edit an existing one
   - Add a protocol mapper:
     - Mapper type: `Audience`
     - Included Client Audience: `frontend-client`
     - Add to ID token: ON
     - Add to access token: ON
     - Add to userinfo: OFF
     - Save
   - Assign this scope to the `frontend-client` via its default scopes

8. Optional: verify token at runtime (debug output of token contents in frontend)

9. Ensure client scopes:
   - Navigate to **Client Scopes**
   - Default scopes for `frontend-client` must include:
     - `roles`
     - `profile`
     - `email`
   - If missing, add them manually
   - These scopes ensure the token contains `realm_access.roles` and user identity information

---

This setup ensures that Keycloak returns a valid token with the expected roles and audience for proper FastAPI backend authorization.
