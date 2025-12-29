Backend (Flask + SQLite)

Run locally:
- Install dependencies: `pip install -r backend/requirements.txt`
- Start server: `python backend/app.py`
- API base: `http://127.0.0.1:5501/`

Endpoints:
- `GET /api/health` — health check
- `GET /api/news` — list news
- `POST /api/news` — create news (JSON: title, content, date?, author_name?, author_initials?)
- `PUT /api/news/:id` — update selected fields
- `DELETE /api/news/:id` — delete
- `POST /api/auth/login` — save a user record (name required; role, email optional)

Database: `backend/data.db` is created automatically.

Notes:
- CORS enabled for local static frontend.
- This is a starter; we can add events, activities, media endpoints next.

---

Cloud Run deployment (Production)

- Project: `mdj-jemmel-prod`
- Service name: `mdj-backend`
- Region: `us-central1`

What’s already set up
- `backend/Dockerfile` builds the Flask app and runs it with `gunicorn` listening on `0.0.0.0:${PORT}` (Cloud Run convention).
- GitHub workflow `.github/workflows/cloud-run.yml` deploys from `./backend` to the Cloud Run service above.
- Firebase Hosting rewrites in `firebase.json` proxy `/api/**` to Cloud Run (`serviceId: mdj-backend`, `region: us-central1`).

Required GitHub secrets (Repository → Settings → Secrets and variables → Actions)
- `GCP_PROJECT_ID`: `mdj-jemmel-prod`
- `GCP_SERVICE_ACCOUNT_KEY`: paste the full JSON contents of your Google Service Account key.
  - The same Service Account can also be used for Firebase Hosting as long as it has the right roles.
- For Firebase Hosting workflow (frontend):
  - `FIREBASE_PROJECT_ID`: `mdj-jemmel-prod`
  - `FIREBASE_SERVICE_ACCOUNT`: paste the full JSON contents of your Firebase Service Account key.

Minimum roles for the Service Account
- Cloud Run: `roles/run.admin`
- Cloud Build: `roles/cloudbuild.builds.editor`
- Artifact Registry: `roles/artifactregistry.admin`
- Storage: `roles/storage.admin`
- Firebase Hosting: `roles/firebase.admin` (or `roles/firebasehosting.admin`)

Deploy steps
1) Push to `main` branch.
2) GitHub Actions will:
   - Build and deploy backend to Cloud Run.
   - Deploy frontend to Firebase Hosting.
3) Test:
   - Frontend: `https://<your-firebase-app>.web.app/`
   - Health via Hosting proxy: `https://<your-firebase-app>.web.app/api/health`

Important
- Do NOT commit Service Account JSON files to the repo. Keep them only in GitHub Secrets.
- SQLite in Cloud Run is ephemeral; for persistence, use Cloud SQL (Postgres/MySQL) or Firestore.