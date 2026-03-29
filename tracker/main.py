from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

SUPABASE_URL    = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY    = os.getenv("SUPABASE_KEY", "")
ADMIN_PASSWORD  = os.getenv("ADMIN_PASSWORD", "admin123")
LOCAL_TEST      = os.getenv("LOCAL_TEST", "false").lower() == "true"

# ── DB setup ────────────────────────────────────────────────
if LOCAL_TEST:
    # in-memory store for local testing
    _visits: list   = []
    _messages: list = []

    class _FakeTable:
        def __init__(self, store): self._store = store
        def insert(self, data):
            self._store.append(data); return self
        def select(self, *a): return self
        def order(self, *a, **kw): return self
        def limit(self, *a): return self
        def execute(self): return type('R', (), {'data': list(reversed(self._store))})()

    class _FakeDB:
        def table(self, name):
            return _FakeTable(_visits if name == 'visits' else _messages)

    supabase = _FakeDB()
    print("🟡 LOCAL TEST MODE — using in-memory storage")
else:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("🟢 PRODUCTION MODE — connected to Supabase")

# ── App ─────────────────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "https://ayanika-portfolio.vercel.app",
        "https://*.vercel.app",
    ],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

# ── Models ──────────────────────────────────────────────────
class ContactMessage(BaseModel):
    name: str
    email: str
    message: str

# ── Helpers ─────────────────────────────────────────────────
def get_real_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

async def get_geo(ip: str) -> dict:
    if ip in ("127.0.0.1", "::1", "localhost"):
        return {"country": "Local", "city": "Localhost", "region": "Dev", "lat": None, "lon": None}
    try:
        async with httpx.AsyncClient(timeout=4) as client:
            r = await client.get(f"https://ipapi.co/{ip}/json/")
            d = r.json()
            return {
                "country": d.get("country_name", "Unknown"),
                "city":    d.get("city", "Unknown"),
                "region":  d.get("region", "Unknown"),
                "lat":     d.get("latitude"),
                "lon":     d.get("longitude"),
            }
    except Exception:
        return {"country": "Unknown", "city": "Unknown", "region": "Unknown", "lat": None, "lon": None}

# ── Routes ──────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "AP Tracker running ✓", "mode": "local" if LOCAL_TEST else "production"}

@app.post("/track")
async def track_visit(request: Request):
    ip = get_real_ip(request)
    ua_string = request.headers.get("user-agent", "")

    try:
        from user_agents import parse as ua_parse
        ua = ua_parse(ua_string)
        device  = "mobile" if ua.is_mobile else ("tablet" if ua.is_tablet else "desktop")
        browser = ua.browser.family
        device_name = ua.device.family if ua.device.family != "Other" else None
    except Exception:
        device, browser, device_name = "unknown", "unknown", None

    geo = await get_geo(ip)

    try:
        body = await request.json()
        referrer = body.get("referrer", "direct")
    except Exception:
        referrer = request.headers.get("referer", "direct")

    record = {
        "ip":          ip,
        "country":     geo["country"],
        "city":        geo["city"],
        "region":      geo["region"],
        "lat":         geo["lat"],
        "lon":         geo["lon"],
        "device":      device,
        "device_name": device_name,
        "browser":     browser,
        "referrer":    referrer,
        "visited_at":  datetime.now(timezone.utc).isoformat(),
    }

    supabase.table("visits").insert(record).execute()
    print(f"  ✓ Visit tracked: {geo['city']}, {geo['country']} [{device}]")
    return {"ok": True}

@app.post("/contact")
async def save_contact(msg: ContactMessage):
    record = {
        "name":    msg.name,
        "email":   msg.email,
        "message": msg.message,
        "sent_at": datetime.now(timezone.utc).isoformat(),
    }
    supabase.table("messages").insert(record).execute()
    print(f"  ✓ Message from: {msg.name} <{msg.email}>")
    return {"ok": True}

@app.get("/api/visits")
async def api_visits():
    res = supabase.table("visits").select("*").order("visited_at", desc=True).limit(500).execute()
    return res.data

@app.get("/api/messages")
async def api_messages():
    res = supabase.table("messages").select("*").order("sent_at", desc=True).execute()
    return res.data

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(pwd: str = ""):
    if pwd != ADMIN_PASSWORD:
        return HTMLResponse(LOGIN_HTML, status_code=401)
    return HTMLResponse(ADMIN_HTML)

# ── HTML ────────────────────────────────────────────────────
LOGIN_HTML = """<!DOCTYPE html><html><head><title>Admin</title>
<style>*{box-sizing:border-box;margin:0;padding:0;}
body{background:#0a0a0a;color:#e8e8e8;font-family:'IBM Plex Mono',monospace;
     display:flex;align-items:center;justify-content:center;min-height:100vh;}
.box{border:2px solid #222;padding:40px;width:340px;}
h2{font-size:.9rem;letter-spacing:.15em;text-transform:uppercase;margin-bottom:24px;color:#ffff00;}
input{width:100%;background:transparent;border:none;border-bottom:2px solid #333;
      color:#e8e8e8;font-family:inherit;font-size:14px;padding:10px 0;outline:none;margin-bottom:24px;}
input:focus{border-bottom-color:#ffff00;}
button{width:100%;background:#ffff00;color:#000;border:none;font-family:inherit;
       font-size:12px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;padding:14px;cursor:pointer;}
</style></head><body><div class="box">
<h2>Admin Access</h2>
<form method="get">
  <input type="password" name="pwd" placeholder="Password" autofocus />
  <button type="submit">Enter →</button>
</form></div></body></html>"""

ADMIN_HTML = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AP · Admin</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
:root{--bg:#0a0a0a;--s1:#111;--border:#1e1e1e;--yellow:#ffff00;--text:#e8e8e8;--muted:#555;}
body{background:var(--bg);color:var(--text);font-family:'IBM Plex Mono',monospace;padding:40px;}
h1{font-size:1.4rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;}
h1 span{color:var(--yellow);}
.subtitle{font-size:11px;color:var(--muted);letter-spacing:.1em;margin-bottom:40px;}
.stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:40px;}
.stat{background:var(--s1);border:1px solid var(--border);padding:20px;}
.stat .num{font-size:2rem;font-weight:700;color:var(--yellow);display:block;}
.stat .lbl{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:4px;}
.tabs{display:flex;gap:0;border-bottom:2px solid var(--border);}
.tab{font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding:12px 24px;cursor:pointer;
     border:1px solid transparent;border-bottom:none;color:var(--muted);transition:all .2s;}
.tab.active{background:var(--s1);border-color:var(--border);color:var(--yellow);}
.panel{display:none;background:var(--s1);border:1px solid var(--border);border-top:none;overflow-x:auto;}
.panel.active{display:block;}
table{width:100%;border-collapse:collapse;font-size:12px;}
th{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
   padding:12px 16px;text-align:left;border-bottom:1px solid var(--border);white-space:nowrap;}
td{padding:12px 16px;border-bottom:1px solid var(--border);color:var(--text);white-space:nowrap;}
tr:last-child td{border-bottom:none;}
tr:hover td{background:rgba(255,255,0,.03);}
.badge{font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:2px 8px;border:1px solid var(--border);}
.badge.mobile{border-color:#a78bfa;color:#a78bfa;}
.badge.desktop{border-color:#56d9fe;color:#56d9fe;}
.badge.tablet{border-color:#39ff8a;color:#39ff8a;}
.empty{padding:40px;text-align:center;color:var(--muted);font-size:12px;}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:32px;}
.refresh{font-size:11px;letter-spacing:.1em;text-transform:uppercase;background:transparent;
         border:1px solid var(--border);color:var(--muted);padding:8px 16px;cursor:pointer;
         font-family:inherit;transition:all .2s;}
.refresh:hover{border-color:var(--yellow);color:var(--yellow);}
.mode-badge{font-size:10px;letter-spacing:.1em;text-transform:uppercase;padding:4px 10px;
            border:1px solid #333;color:#555;}
.table-toolbar{display:flex;justify-content:space-between;align-items:center;
               padding:12px 16px;border-bottom:1px solid var(--border);flex-wrap:wrap;gap:12px;}
.sort-btns{display:flex;gap:8px;flex-wrap:wrap;}
.sort-btn{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;
          text-transform:uppercase;background:transparent;border:1px solid var(--border);
          color:var(--muted);padding:6px 12px;cursor:pointer;transition:all .2s;}
.sort-btn:hover,.sort-btn.active{border-color:var(--yellow);color:var(--yellow);}
.unique-badge{font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:2px 8px;
              border:1px solid #39ff8a;color:#39ff8a;margin-left:6px;}
.date-filter{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.date-filter label{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);}
.date-input{background:var(--bg);border:1px solid var(--border);color:var(--text);
            font-family:'IBM Plex Mono',monospace;font-size:11px;padding:6px 10px;
            outline:none;cursor:pointer;transition:border-color .2s;}
.date-input:focus{border-color:var(--yellow);}
.date-input::-webkit-calendar-picker-indicator{filter:invert(1) brightness(0.6);cursor:pointer;}
.date-clear{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;
            text-transform:uppercase;background:transparent;border:1px solid var(--border);
            color:var(--muted);padding:6px 10px;cursor:pointer;transition:all .2s;}
.date-clear:hover{border-color:#ff4d4d;color:#ff4d4d;}
</style>
</style></head><body>
<div class="topbar">
  <div>
    <h1>AP <span>·</span> Admin</h1>
    <p class="subtitle">Portfolio analytics dashboard</p>
  </div>
  <div style="display:flex;gap:12px;align-items:center;">
    <span class="mode-badge" id="modeBadge">—</span>
    <button class="refresh" onclick="loadData()">↻ Refresh</button>
  </div>
</div>

<div class="stats">
  <div class="stat"><span class="num" id="totalVisits">—</span><span class="lbl">Total Visits</span></div>
  <div class="stat"><span class="num" id="uniqueVisitors">—</span><span class="lbl">Unique Visitors</span></div>
  <div class="stat"><span class="num" id="todayVisits">—</span><span class="lbl">Today</span></div>
  <div class="stat"><span class="num" id="uniqueCountries">—</span><span class="lbl">Countries</span></div>
  <div class="stat"><span class="num" id="totalMessages">—</span><span class="lbl">Messages</span></div>
</div>

<div class="tabs">
  <div class="tab active" onclick="switchTab('visits')">Visits</div>
  <div class="tab" onclick="switchTab('messages')">Messages</div>
</div>

<div class="panel active" id="panel-visits">
  <div class="table-toolbar">
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
      <span id="visitCount" style="color:var(--muted);font-size:11px;letter-spacing:.1em;"></span>
      <div class="date-filter">
        <label>From</label>
        <input type="date" class="date-input" id="dateFrom" onchange="renderVisits()">
        <label>To</label>
        <input type="date" class="date-input" id="dateTo" onchange="renderVisits()">
        <button class="date-clear" onclick="clearDates()">✕ Clear</button>
      </div>
    </div>
    <div class="sort-btns">
      <button class="sort-btn active" onclick="sortVisits('recent',event)">Recent First</button>
      <button class="sort-btn" onclick="sortVisits('oldest',event)">Oldest First</button>
      <button class="sort-btn" onclick="sortVisits('unique',event)">Unique Only</button>
    </div>
  </div>
  <table><thead><tr>
    <th>#</th><th>Time</th><th>Country</th><th>State / Region</th><th>City</th>
    <th>Device</th><th>Device Name</th><th>Browser</th><th>Referrer</th><th>Type</th>
  </tr></thead>
  <tbody id="visitsBody"><tr><td colspan="10" class="empty">Loading...</td></tr></tbody></table>
</div>

<div class="panel" id="panel-messages">
  <table><thead><tr>
    <th>#</th><th>Time</th><th>Name</th><th>Email</th><th>Message</th>
  </tr></thead>
  <tbody id="messagesBody"><tr><td colspan="5" class="empty">Loading...</td></tr></tbody></table>
</div>

<script>
let allVisits = [];
let currentSort = 'recent';

function switchTab(name) {
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',['visits','messages'][i]===name));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('panel-'+name).classList.add('active');
}

function sortVisits(mode, e) {
  currentSort = mode;
  document.querySelectorAll('.sort-btn').forEach(b=>b.classList.remove('active'));
  if (e) e.target.classList.add('active');
  renderVisits();
}

function clearDates() {
  document.getElementById('dateFrom').value = '';
  document.getElementById('dateTo').value   = '';
  renderVisits();
}

function renderVisits() {
  let data = [...allVisits];

  // date filter
  const from = document.getElementById('dateFrom').value;
  const to   = document.getElementById('dateTo').value;
  if (from) data = data.filter(v => v.visited_at >= from);
  if (to)   data = data.filter(v => v.visited_at.slice(0,10) <= to);

  if (currentSort === 'oldest') {
    data.sort((a,b) => new Date(a.visited_at) - new Date(b.visited_at));
  } else if (currentSort === 'recent') {
    data.sort((a,b) => new Date(b.visited_at) - new Date(a.visited_at));
  } else if (currentSort === 'unique') {
    const seen = new Set();
    data = data.filter(v => { if (seen.has(v.ip)) return false; seen.add(v.ip); return true; });
    data.sort((a,b) => new Date(b.visited_at) - new Date(a.visited_at));
  }

  const fromLabel = from ? ` from ${from}` : '';
  const toLabel   = to   ? ` to ${to}`     : '';
  const rangeLabel = (from || to) ? `${fromLabel}${toLabel} · ` : '';

  document.getElementById('visitCount').textContent =
    currentSort === 'unique'
      ? `${rangeLabel}${data.length} unique visitor${data.length !== 1 ? 's' : ''}`
      : `${rangeLabel}${data.length} visit${data.length !== 1 ? 's' : ''}`;

  const seenIPs = new Set();
  const ipCount = {};
  allVisits.forEach(v => { ipCount[v.ip] = (ipCount[v.ip]||0) + 1; });

  const vb = document.getElementById('visitsBody');
  vb.innerHTML = data.length
    ? data.map((v,i) => {
        const isRepeat = ipCount[v.ip] > 1;
        return `<tr>
          <td style="color:var(--muted)">${i+1}</td>
          <td>${new Date(v.visited_at).toLocaleString()}</td>
          <td>${v.country||'—'}</td>
          <td>${v.region||'—'}</td>
          <td>${v.city||'—'}</td>
          <td><span class="badge ${v.device}">${v.device||'—'}</span></td>
          <td>${v.device_name||'—'}</td>
          <td>${v.browser||'—'}</td>
          <td style="max-width:180px;overflow:hidden;text-overflow:ellipsis">${v.referrer||'direct'}</td>
          <td>${isRepeat ? `<span class="badge" style="border-color:#f59e0b;color:#f59e0b;">${ipCount[v.ip]}x</span>` : '<span class="unique-badge">new</span>'}</td>
        </tr>`;
      }).join('')
    : '<tr><td colspan="9" class="empty">No visits yet.</td></tr>';
}

async function loadData() {
  const [vRes, mRes, rootRes] = await Promise.all([
    fetch('/api/visits'), fetch('/api/messages'), fetch('/')
  ]);
  allVisits          = await vRes.json();
  const messages     = await mRes.json();
  const root         = await rootRes.json();

  document.getElementById('modeBadge').textContent = root.mode + ' mode';

  const today        = new Date().toISOString().slice(0,10);
  const uniqueIPs    = new Set(allVisits.map(v=>v.ip));

  document.getElementById('totalVisits').textContent     = allVisits.length;
  document.getElementById('uniqueVisitors').textContent  = uniqueIPs.size;
  document.getElementById('todayVisits').textContent     = allVisits.filter(v=>v.visited_at?.startsWith(today)).length;
  document.getElementById('uniqueCountries').textContent = new Set(allVisits.map(v=>v.country)).size;
  document.getElementById('totalMessages').textContent   = messages.length;

  renderVisits();

  const mb = document.getElementById('messagesBody');
  mb.innerHTML = messages.length
    ? messages.map((m,i)=>`<tr>
        <td style="color:var(--muted)">${i+1}</td>
        <td>${new Date(m.sent_at).toLocaleString()}</td>
        <td>${m.name}</td>
        <td>${m.email}</td>
        <td style="max-width:300px;white-space:normal">${m.message}</td>
      </tr>`).join('')
    : '<tr><td colspan="5" class="empty">No messages yet.</td></tr>';
}

loadData();
</script>
</body></html>"""
