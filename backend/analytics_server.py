#!/usr/bin/env python3
"""AiMedbrief Analytics Server — with auth"""
import http.server, json, sqlite3, os, time, sys, traceback, hashlib, secrets
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, 'analytics.db')
PORT = 5000

# ── Auth Config ─────────────────────────────────────────
ADMIN_USER = 'admin'
ADMIN_PASS_HASH = hashlib.sha256('Admin2025!'.encode()).hexdigest()  # change me
ACTIVE_TOKENS = {}  # token → expiry_timestamp
SESSION_TTL = 3600  # 1 hour

# ── DB ───────────────────────────────────────────────────
def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("CREATE TABLE IF NOT EXISTS page_views (id INTEGER PRIMARY KEY AUTOINCREMENT,page TEXT,article_id TEXT,referrer TEXT,ua TEXT,ip TEXT,created_at TEXT DEFAULT (datetime('now','localtime')))")
    db.execute("CREATE TABLE IF NOT EXISTS article_clicks (id INTEGER PRIMARY KEY AUTOINCREMENT,article_id TEXT,title TEXT,created_at TEXT DEFAULT (datetime('now','localtime')))")
    db.commit(); db.close()

def _q(sql, params=()):
    db = sqlite3.connect(DB_PATH); db.row_factory = sqlite3.Row
    cur = db.execute(sql, params); rows = [dict(r) for r in cur.fetchall()]
    db.close(); return rows

def _e(sql, params=()):
    db = sqlite3.connect(DB_PATH); db.execute(sql, params); db.commit(); db.close()

init_db()

# ── Login HTML (inline) ──────────────────────────────────
LOGIN = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Login — AiMedbrief Analytics</title>
<style>:root{--bg:#0f1117;--card:#1a1d28;--border:#2a2d3a;--text:#e4e6ec;--muted:#888;--accent:#4f8cff;--red:#ef4444}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;min-height:100vh}
.login-box{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:40px;width:380px;max-width:90vw}
.login-box h1{font-size:22px;text-align:center;margin-bottom:4px}.login-box h1 span{color:var(--accent)}
.login-box .sub{text-align:center;color:var(--muted);font-size:13px;margin-bottom:28px}
.input-group{margin-bottom:16px}.input-group label{display:block;font-size:12px;color:var(--muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:.5px}
.input-group input{width:100%;padding:10px 14px;background:#0f1117;border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:14px;outline:none;transition:border-color .2s}
.input-group input:focus{border-color:var(--accent)}
.login-btn{width:100%;padding:12px;background:var(--accent);color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;margin-top:8px;transition:opacity .2s}
.login-btn:hover{opacity:.9}.login-btn:disabled{opacity:.5;cursor:not-allowed}
.error{color:var(--red);font-size:12px;text-align:center;margin-top:12px;display:none}
</style></head><body>
<div class="login-box">
<h1>&#128202; <span>AiMedbrief</span></h1><div class="sub">Analytics Dashboard</div>
<input class="input-group" type="text" id="user" placeholder="Username" autocomplete="off"><br>
<input class="input-group" type="password" id="pass" placeholder="Password" style="margin-top:-12px"><br>
<button class="login-btn" id="btn" onclick="doLogin()">Sign In</button>
<div class="error" id="err"></div>
</div>
<script>
document.getElementById('pass').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin()});
async function doLogin(){const u=document.getElementById('user').value,p=document.getElementById('pass').value;
if(!u||!p)return;const btn=document.getElementById('btn'),err=document.getElementById('err');
btn.disabled=true;btn.textContent='Signing in...';err.style.display='none';
try{const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:u,pass:p})});
const d=await r.json();if(d.ok){document.cookie='token='+d.token+';path=/;max-age=3600';location.href='/admin'}
else{err.textContent=d.error||'Login failed';err.style.display='block'}}
catch(e){err.textContent='Network error';err.style.display='block'}
btn.disabled=false;btn.textContent='Sign In'}
</script></body></html>"""

# ── Admin HTML (inline) ──────────────────────────────────
ADMIN = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>AiMedbrief Analytics</title>
<style>:root{--bg:#0f1117;--card:#1a1d28;--border:#2a2d3a;--text:#e4e6ec;--muted:#888;--accent:#4f8cff;--green:#34d399}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
.header{background:var(--card);border-bottom:1px solid var(--border);padding:16px 32px;display:flex;align-items:center;justify-content:space-between}
.header h1{font-size:20px;font-weight:700}.header h1 span{color:var(--accent)}.header .live{font-size:12px;color:var(--green);display:flex;align-items:center;gap:6px}
.header .live::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--green);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}.container{max-width:1200px;margin:0 auto;padding:24px}
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px}
.stat-card .label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}
.stat-card .value{font-size:32px;font-weight:700}.stat-card .value.accent{color:var(--accent)}.stat-card .value.green{color:var(--green)}
.stat-card .sub{font-size:12px;color:var(--muted);margin-top:4px}
.section-title{font-size:16px;font-weight:600;margin-bottom:12px;color:var(--muted);letter-spacing:.3px}
.articles-table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.articles-table th{background:#11131c;padding:12px 16px;font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;text-align:left}
.articles-table td{padding:12px 16px;font-size:13px;border-top:1px solid var(--border)}
.bar-wrap{background:#1a1d28;border-radius:4px;height:6px;overflow:hidden;min-width:60px}
.bar-fill{background:var(--accent);height:100%;border-radius:4px;transition:width .3s}
.recent-log{background:var(--card);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-top:24px}
.recent-log th{background:#11131c;padding:8px 16px;font-size:11px;color:var(--muted);text-align:left}
.recent-log td{padding:8px 16px;font-size:12px;border-top:1px solid var(--border);max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.refresh{font-size:11px;color:var(--muted);text-align:right;margin-top:8px}
.empty{text-align:center;color:var(--muted);padding:32px;font-size:13px}
</style></head><body>
<div class="header"><h1>&#128202; <span>AiMedbrief</span> Analytics</h1><div class="live">Live &#183; Auto-refresh 10s</div></div>
<div class="container" id="app">Loading...</div>
<script>
const $=s=>document.querySelector(s);
async function load(){const r=await fetch('/api/stats');const d=await r.json();render(d)}
function render(d){const pv=d.today_views||0,apv=d.all_views||0,ac=d.article_clicks||0,ua=d.unique_articles||0;const top=d.articles||[],recent=d.recent||[];const max=Math.max(...top.map(a=>a.page_views||0),1);
let h='<div class="stats-row">'+card('Today PV',pv,'accent',pv>0?'today so far':'waiting')+card('All-Time PV',apv,'','total')+card('Article Clicks',ac,'green',ua+' unique')+card('Unique IPs',d.unique_ips||0,'','distinct')+'</div>';
h+='<div class="section-title">&#128466; Article Performance</div>';
if(top.length){h+='<table class="articles-table"><tr><th>Article</th><th>PV</th><th>Clicks</th><th></th></tr>';
top.forEach(a=>{h+='<tr><td style="max-width:400px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+e(a.title_en||'---')+'</td><td>'+a.page_views+'</td><td>'+a.clicks+'</td><td><div class="bar-wrap"><div class="bar-fill" style="width:'+Math.round(a.page_views/max*100)+'%"></div></div></td></tr>'});h+='</table>'}
else{h+='<div class="empty">No data yet</div>'}
h+='<div class="section-title" style="margin-top:24px">&#128339; Recent Activity</div>';
if(recent.length){h+='<div class="recent-log"><table><tr><th>Time</th><th>Page</th><th>UA</th></tr>';
recent.forEach(r=>{const t=r.created_at?r.created_at.replace('T',' ').substring(0,19):'';h+='<tr><td>'+t+'</td><td>'+e(r.page)+'</td><td style="font-size:10px;color:var(--muted)">'+e((r.ua||'').substring(0,80))+'</td></tr>'});h+='</table></div>'}
h+='<div class="refresh">Updated: '+(d.generated||'')+'</div>';$('#app').innerHTML=h}
function card(l,v,c,s){return '<div class="stat-card"><div class="label">'+l+'</div><div class="value '+c+'">'+v+'</div><div class="sub">'+s+'</div></div>'}
function e(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
load();setInterval(load,10000);
</script></body></html>"""

# ── Handler ──────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _ok(self, ct='application/json'):
        self.send_response(200)
        self.send_header('Content-Type', ct)
        self._cors()
        self.end_headers()

    def _send(self, body, ct='text/html; charset=utf-8', code=200):
        self.send_response(code)
        self.send_header('Content-Type', ct)
        self._cors()
        self.end_headers()
        self.wfile.write(body.encode('utf-8') if isinstance(body, str) else body)

    def _json(self, data):
        self._ok()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _get_cookie(self, name):
        cookie = self.headers.get('Cookie', '')
        for c in cookie.split(';'):
            c = c.strip()
            if c.startswith(name + '='):
                return c[len(name)+1:]
        return None

    def _check_auth(self):
        token = self._get_cookie('token')
        if token and token in ACTIVE_TOKENS:
            if time.time() < ACTIVE_TOKENS[token]:
                return True
            del ACTIVE_TOKENS[token]
        return False

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_GET(self):
        try:
            p = urlparse(self.path)
            if p.path in ('/admin', '/'):
                if not self._check_auth():
                    return self._send(LOGIN)
                return self._send(ADMIN)
            if p.path == '/api/stats':
                if not self._check_auth():
                    self.send_response(401); self._cors(); self.end_headers()
                    return
                return self._stats()
            if p.path == '/logout':
                token = self._get_cookie('token')
                if token: ACTIVE_TOKENS.pop(token, None)
                return self._send(LOGIN)
            self.send_response(404); self._cors(); self.end_headers()
        except Exception as e:
            print(f'[ERROR GET {self.path}] {e}', file=sys.stderr)
            traceback.print_exc()
            self.send_response(500); self._cors(); self.end_headers()

    def do_POST(self):
        try:
            p = urlparse(self.path)
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length else b'{}'
            data = json.loads(body) if body else {}
            ip = self.client_address[0]

            # ── Login ──
            if p.path == '/api/login':
                u = (data.get('user') or '').strip()
                pw = (data.get('pass') or '').strip()
                if u == ADMIN_USER and hashlib.sha256(pw.encode()).hexdigest() == ADMIN_PASS_HASH:
                    token = secrets.token_hex(32)
                    ACTIVE_TOKENS[token] = time.time() + SESSION_TTL
                    self._json({'ok': True, 'token': token})
                else:
                    self._json({'ok': False, 'error': 'Invalid username or password'})
                return

            # ── Tracking (no auth needed) ──
            if p.path == '/track':
                _e("INSERT INTO page_views (page,article_id,referrer,ua,ip) VALUES (?,?,?,?,?)",
                    (data.get('page',''), data.get('article_id') or None, data.get('referrer',''),
                     self.headers.get('User-Agent',''), ip))
                return self._json({'ok': True})

            if p.path == '/track-click':
                _e("INSERT INTO article_clicks (article_id,title) VALUES (?,?)",
                    (data.get('article_id',''), data.get('title','')))
                return self._json({'ok': True})

            self.send_response(404); self._cors(); self.end_headers()
        except Exception as e:
            print(f'[ERROR POST {self.path}] {e}', file=sys.stderr)
            traceback.print_exc()
            self.send_response(500); self._cors(); self.end_headers()

    def _stats(self):
        today = time.strftime('%Y-%m-%d', time.localtime())
        tv = _q("SELECT COUNT(*) n FROM page_views WHERE created_at >= ?", (today,))[0]['n']
        av = _q("SELECT COUNT(*) n FROM page_views")[0]['n']
        ac = _q("SELECT COUNT(*) n FROM article_clicks")[0]['n']
        uip = _q("SELECT COUNT(DISTINCT ip) n FROM page_views WHERE created_at >= ?", (today,))[0]['n']

        # Load articles from data.json
        dp = os.path.join(HERE, '..', 'articles', 'data.json')
        articles = []
        if os.path.exists(dp):
            with open(dp, encoding='utf-8') as f:
                arts = json.load(f)
            for a in arts:
                pv = _q("SELECT COUNT(*) n FROM page_views WHERE article_id=?", (a['id'],))[0]['n']
                cl = _q("SELECT COUNT(*) n FROM article_clicks WHERE article_id=?", (a['id'],))[0]['n']
                articles.append({'id': a['id'], 'title_en': a.get('title_en',''), 'page_views': pv, 'clicks': cl})

        recent = _q("SELECT page,article_id,ua,created_at FROM page_views ORDER BY id DESC LIMIT 50")
        ua_count = len(set(r['article_id'] for r in recent if r['article_id']))
        self._json({'today_views': tv, 'all_views': av, 'article_clicks': ac, 'unique_articles': ua_count,
                     'unique_ips': uip, 'articles': articles, 'recent': recent,
                     'generated': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})

# ── Boot ─────────────────────────────────────────────────
if __name__ == '__main__':
    import socketserver
    print(f'\n  AiMedbrief Analytics Server')
    print(f'  Admin : http://localhost:{PORT}/admin')
    print(f'  Stats : http://localhost:{PORT}/api/stats')
    print(f'  Track : POST http://localhost:{PORT}/track')
    print(f'  Click : POST http://localhost:{PORT}/track-click\n')
    sys.stdout.flush()
    class TS(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True
    httpd = TS(('0.0.0.0', PORT), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n  Shutting down...')
        httpd.server_close()