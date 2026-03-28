# Ayanika Paul — Portfolio

React + Vite frontend with a FastAPI visitor tracker backend.

## Structure

```
portfolio-react/     ← deploy to Vercel
  src/
  tracker/           ← deploy to Render
    main.py
    requirements.txt
```

## Deploy

### 1. Supabase (database)
1. Create project at supabase.com
2. SQL Editor → paste `tracker/supabase_schema.sql` → Run
3. Copy Project URL and anon key from Settings → API

### 2. Render (backend)
1. Push this repo to GitHub
2. New Web Service → connect repo → set **Root Directory** to `tracker`
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env vars:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `ADMIN_PASSWORD` (choose a strong password)
   - `LOCAL_TEST` = `false`
6. Deploy → copy the `.onrender.com` URL

### 3. Vercel (frontend)
1. Import repo on vercel.com
2. Framework: Vite (auto-detected)
3. Add env var: `VITE_TRACKER_URL` = your Render URL
4. Deploy

### 4. After deploy
- Update CORS in `tracker/main.py` — add your exact Vercel URL
- Admin dashboard: `https://your-render-url.onrender.com/admin?pwd=yourpassword`
