# Render Backend Deployment Guide
## AI-Powered Automatic Block Planning System (FastAPI + OR-Tools + Supabase)

---

## 1. Prerequisites Checklist

Before beginning deployment, ensure you have:
1. A **[Render Account](https://render.com/)** (Free tier works seamlessly).
2. A **[GitHub](https://github.com/)** or **GitLab** account with this repository pushed.
3. Your **Supabase Database Credentials**:
   * `SUPABASE_URL` (e.g. `https://your-project.supabase.co`)
   * `SUPABASE_KEY` (Your public `anon` key or service role key)

---

## 2. Project File Structure & Verification

Ensure your repository root contains:
* [`main.py`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/main.py) (The FastAPI application with `app = FastAPI()`)
* [`requirements.txt`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/requirements.txt):
  ```text
  fastapi
  uvicorn[standard]
  supabase
  python-dotenv
  ortools
  ```
* [`.gitignore`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/.gitignore) (Ensure `.env` is ignored so secrets are never pushed to GitHub).

---

## 3. Step-by-Step Deployment Instructions on Render

### Step 1: Push the Code to GitHub
Open your terminal in the project directory and push your code:
```bash
git add .
git commit -m "Prepare backend for Render deployment"
git push origin main
```

---

### Step 2: Create a New Web Service on Render
1. Open the **[Render Dashboard](https://dashboard.render.com/)**.
2. Click the blue **"New +"** button at the top-right and select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and click **Next**.
4. Connect and select your GitHub repository.

---

### Step 3: Configure Web Service Settings

Fill in the configuration fields on Render:

| Field | Value / Setting | Description |
|---|---|---|
| **Name** | `railblock-api` *(or your custom name)* | The subdomain URL prefix on Render |
| **Region** | `Singapore (Southeast Asia)` or `Frankfurt` | Choose the region closest to your users |
| **Branch** | `main` | Production Git branch |
| **Root Directory** | *(Leave empty / root)* | Points to repository root containing `main.py` |
| **Runtime** | `Python 3` | Built-in Python environment |
| **Build Command** | `pip install -r requirements.txt` | Installs FastAPI, Uvicorn, Supabase, OR-Tools |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` | Starts the production ASGI server |
| **Instance Type** | `Free` | Free Tier (512 MB RAM, 0.1 CPU) |

---

### Step 4: Add Environment Variables

Scroll down to the **"Environment Variables"** section and click **"Add Environment Variable"**:

| Key | Value | Purpose |
|---|---|---|
| `SUPABASE_URL` | `https://xxxx.supabase.co` | Supabase project API URL |
| `SUPABASE_KEY` | `eyJhbGciOi...` | Supabase API authentication key |
| `PYTHON_VERSION` | `3.11.8` *(optional)* | Ensures optimal compatibility for OR-Tools |

> [!IMPORTANT]
> Never commit real API keys directly into `main.py` or Git. Always input them securely via Render's **Environment Variables** panel.

---

### Step 5: Deploy & Monitor Logs

1. Click **"Create Web Service"**.
2. Render will automatically:
   * Clone your Git repository.
   * Run `pip install -r requirements.txt`.
   * Bind Uvicorn to `0.0.0.0:$PORT`.
3. In the deployment console, you should see:
   ```text
   ==> Uploading build...
   ==> Build successful 🎉
   ==> Starting service with 'uvicorn main:app --host 0.0.0.0 --port $PORT'
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:10000
   ==> Your service is live 🚀
   ```

---

## 4. Validating the Live Backend API

Once deployed, test your API endpoints by replacing `https://railblock-api.onrender.com` with your assigned Render service URL:

1. **Root Health Check:**
   ```bash
   curl https://railblock-api.onrender.com/
   ```
   *Expected:* `{"message": "AI Block Planning API is running."}`

2. **Interactive OpenAPI / Swagger Documentation:**
   * Open `https://railblock-api.onrender.com/docs` in your browser.

3. **Verify Core Problem Statement Endpoints:**
   * `GET https://railblock-api.onrender.com/summary` → Returns before/after KPI metrics.
   * `GET https://railblock-api.onrender.com/defects` → Returns prioritized defect inbox.
   * `GET https://railblock-api.onrender.com/block-plan` → Returns CP-SAT optimized schedule.
   * `GET https://railblock-api.onrender.com/block-requests` → Returns auto-generated block request justifications.

---

## 5. Troubleshooting & Best Practices

* **Cold Start (Free Tier):**
  Render Free Tier spins down after 15 minutes of inactivity. The first request after sleep may take ~30–50 seconds to boot up. Subsequent requests respond instantly.
* **CORS Settings:**
  `main.py` already includes `CORSMiddleware` with `allow_origins=["*"]`, allowing your deployed frontend to communicate with the backend across different domains without CORS errors.
* **Supabase Connection Issues:**
  If you see `500 Internal Server Error`, double-check the `SUPABASE_URL` and `SUPABASE_KEY` values in Render's **Environment** tab.
