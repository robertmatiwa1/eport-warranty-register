# eport-warranty-register

## 1. Solution Overview

This solution extends the Asset Manager app from Task 1 with a dedicated Warranty Register microservice built in Python and deployed on an Ubuntu 24.04 server using Docker and Nginx.

**High-level architecture:**

### Next.js Asset Manager (Task 1)

* Users can view their assets and register a warranty directly from the UI.
* A server-side Next.js API route (`/api/register-warranty`) securely relays requests to the Python Warranty Register service using an API key.
* The UI shows real-time status per asset (Warranty Registered / Warranty Not Registered).

### Python FastAPI Warranty Register (Task 2)

* Exposes REST endpoints to:

  * Register a device or asset for warranty
  * Authenticate users and allow them to view all registered warranties
  * Provide a `/warranty` dashboard for the Warranty Centre
* Uses PostgreSQL as the backing store.
* Protected with JWT-based auth and API-key security.

### PostgreSQL (Docker container)

* Stores warranty registrations and user accounts.
* Tuned via a custom postgres-conf/custom.conf.

### Nginx reverse proxy

* Terminates TLS using Let’s Encrypt certificates.
* Proxies all external traffic to FastAPI.
* Enforces HTTPS.

### Ubuntu 24.04 Server

* Hardened SSH and firewall.
* Automatic security updates enabled.
* All components deployed as Docker containers:

  * `warranty_api`
  * `warranty_db`
  * `warranty_nginx`

---

## 2. System Architecture

```
+-----------------------+         +----------------------+
|   Next.js Asset App   |  HTTPS  |  Nginx Reverse Proxy |
|  /user/assets         +-------->+ https://server29...  |
|  /api/register-warr   |         +----------------------+
+-----------------------+                     |
                                             HTTP
                                               v
                                   +-----------------------+
                                   |  FastAPI Warranty     |
                                   |  /api/warranty/...    |
                                   |  /warranty dashboard  |
                                   +-----------+-----------+
                                               |
                                              TCP
                                               v
                                   +-----------------------+
                                   |    PostgreSQL DB      |
                                   +-----------------------+
```

---

## 3. Repository Structure

```
.
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── routers/                # API route handlers
│   ├── models/                 # SQLAlchemy models
│   ├── core/                   # Auth, security utilities
│   ├── db/                     # Database session & config
│   └── templates/              # Warranty Centre UI
│
├── nginx/
│   └── nginx.conf              # Reverse proxy & TLS config
│
├── postgres-conf/
│   └── custom.conf             # PostgreSQL tuning
│
├── docker-compose.yml          # Deployment
├── Dockerfile                  # API build
└── requirements.txt            # Python dependencies
```

---

## 4. Installation & Deployment

### 4.1 Clone the repository

```bash
git clone https://github.com/YOUR_REPO/eport-warranty-register.git
cd eport-warranty-register
```

### 4.2 Create required folders

```bash
mkdir -p postgres-conf
mkdir -p nginx
```

### 4.3 Build and start the service

```bash
docker-compose up -d --build
```

This starts:

* warranty_api
* warranty_db
* warranty_nginx

### 4.4 Verify containers are running

```bash
docker-compose ps
```

Expected:

```
warranty_api     Up (healthy)
warranty_db      Up
warranty_nginx   Up
```

---

## 5. API Endpoints

### Register warranty (used by Next.js)

**POST** `/api/warranty/register`

**Headers**

| Header       | Value                 |
| ------------ | --------------------- |
| X-API-Key    | your internal API key |
| Content-Type | application/json      |

**Body**

```json
{
  "asset_id": "123",
  "asset_name": "Laptop",
  "registered_by": "user@example.com"
}
```

**Response**

```json
{
  "status": "success",
  "message": "Warranty registered",
  "id": 52
}
```

### Warranty Centre UI (Admin)

* `GET /warranty`
* `GET /warranty/login`

---

## 6. Security Measures Implemented (Task 8)

### Linux & SSH hardening

* Created non-root sudo users `robert` and `eport`.
* SSH key authentication enabled.
* Password auth disabled:

```
PasswordAuthentication no
PermitRootLogin no
```

* UFW enabled:

```
OpenSSH ALLOW
80/tcp ALLOW
443/tcp ALLOW
```

* Automatic security updates enabled.

### Application Security

* JWT-based authentication.
* Password hashing with bcrypt/Passlib.
* API-key validation for service-to-service calls.
* Environment-based configuration.
* Nginx TLS termination.

### Container Security

* Postgres only inside Docker network.
* API only accessible via Nginx.
* Clear separation of API, DB, and Proxy.

---

## 7. PostgreSQL Performance Tuning (Task 9)

A custom file (`postgres-conf/custom.conf`) is mounted into Postgres.

### Key tuning parameters

| Parameter                    | Value  | Purpose                       |
| ---------------------------- | ------ | ----------------------------- |
| shared_buffers               | 512MB  | Larger memory cache           |
| effective_cache_size         | 1536MB | Better query planning         |
| work_mem                     | 16MB   | Faster sorts and joins        |
| maintenance_work_mem         | 256MB  | Faster VACUUM and index build |
| max_wal_size                 | 1GB    | Smoother checkpoints          |
| checkpoint_completion_target | 0.9    | Reduces I/O spikes            |
| synchronous_commit           | off    | Faster writes                 |
| max_connections              | 50     | Suitable for small deployment |

---

## 8. How to Test End-to-End

### 8.1 From Asset Manager (Task 1)

Expected:

* Button shows *Registering...*
* Status updates to *Warranty Registered*
* Button disappears

### 8.2 In Warranty Centre

Visit:

```
https://server29.eport.ws/warranty
```

You should see:

* Asset ID
* Asset Name
* Registered user
* Warranty Registered badge

### 8.3 Server Verification

```bash
ssh robert@server29.eport.ws
cd ~/eport-warranty-register
docker-compose ps
```

Everything should be up.

---

## 9. Environment Variables

Set via Docker Compose:

| Variable                     | Description         |
| ---------------------------- | ------------------- |
| API_KEY                      | Required by FastAPI |
| POSTGRES_USER                | DB username         |
| POSTGRES_PASSWORD            | DB password         |
| POSTGRES_DB                  | DB name             |
| WARRANTY_API_KEY             | Next.js secret key  |
| NEXT_PUBLIC_WARRANTY_API_URL | FastAPI URL         |

---

## 10. Dependencies

### Python

* FastAPI
* Uvicorn
* SQLAlchemy
* Passlib
* Python-JOSE
* Psycopg2

### Services

* PostgreSQL 15
* Nginx
* Let’s Encrypt Certbot
* Docker / Docker Compose

---

## 11. Developer Notes

* All secrets are environment-driven.
* API is stateless and scalable.
* Warranty logic lives in `routers/warranty.py`.
* UI templates use Jinja2.
* Future microservices can be added easily.

---

## 12. Credits

Developed by **Robert Matiwa**
AWS Certified | Senior Cloud & Solutions Architect
Contact: **[robertmatiwa3@gmail.com](mailto:robertmatiwa3@gmail.com)**
