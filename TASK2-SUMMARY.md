# Task 2 – Summary Report
**Candidate:** Robert Matiwa  
**Project:** Warranty Register Microservice Deployment  
**Server:** Ubuntu 24.04 (server29.eport.ws)

## 1. Overview
This task required the implementation and deployment of a secure Warranty Register microservice using Python FastAPI, Docker, PostgreSQL, Nginx, and SSL on an Ubuntu 24.04 server. All requirements outlined in the brief have been completed and verified.

## 2. Linux Server Configuration
- Created required users: `robert` and `eport`, both with sudo privileges.  
- SSH key–only authentication enabled.  
- Password login disabled and root SSH access blocked.  
- Firewall configured to allow only ports 22, 80, and 443.

## 3. FastAPI Warranty Service
- Implemented warranty registration endpoint and supporting logic.  
- Added JWT authentication for the Warranty Centre dashboard.  
- Applied API-key validation for internal system communication.  
- Structured using routers, models, templates, and database utilities.

## 4. Docker Deployment
- Deployed using Docker Compose with three containers:  
  - `warranty_api` (FastAPI)  
  - `warranty_db` (PostgreSQL 15)  
  - `warranty_nginx` (Nginx reverse proxy with SSL)
- Containers run inside an isolated Docker network.

## 5. Nginx & SSL Configuration
- Configured Nginx as a reverse proxy for FastAPI.  
- Implemented Let’s Encrypt SSL certificates for HTTPS.  
- Enabled automatic HTTP → HTTPS redirection.

## 6. PostgreSQL Setup & Tuning
- PostgreSQL deployed with persistent volume storage.  
- Custom tuning applied via `postgres-conf/custom.conf` to optimise performance.

## 7. Security Measures
- JWT authentication and bcrypt password hashing implemented.  
- API-key protection added for internal API calls.  
- All secrets passed through environment variables.  
- Database is internal-only and not publicly accessible.

## 8. End-to-End Verification
- Warranty registration from the Asset Manager UI tested successfully.  
- Dashboard displays registered warranties as expected.  
- All containers confirmed running and healthy.

## 9. Repository
This report, along with full source code and documentation, is hosted at:  
**https://github.com/robertmatiwa1/eport-warranty-register**

## 10. Status
**Task 2 has been fully completed and is ready for assessment.**


