#!/usr/bin/env python3
"""Build app.html with literature tab content embedded."""
import json

lit_data = json.load(open('/Coze/Drive/Arise/所有对话/主对话/3HFIT/教培中心/姚宁大师课/voice-club/lit_data.json'))
lit_json = json.dumps(lit_data, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ARISE CLUB</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

html{scroll-behavior:smooth}
body{
  font-family:'Helvetica Neue','Arial Black',Arial,'PingFang SC','Noto Sans SC',sans-serif;
  background:#E8E4DF;
  color:#1A1A1A;
  line-height:1.6;
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
a{color:#1A1A1A;text-decoration:none}
a:hover{text-decoration:underline}

/* ===== NAV ===== */
.nav{
  background:#E8E4DF;
  border-bottom:1px solid #D0CBC5;
  padding:0 8vw;
  height:56px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  position:sticky;
  top:0;
  z-index:100;
}
.nav-logo{font-size:12px;font-weight:700;letter-spacing:5px;text-transform:uppercase}
.nav-right{display:flex;align-items:center;gap:16px}
.nav-user{font-size:12px;color:#888}
.nav-logout{
  background:none;border:1px solid #ccc;color:#888;
  padding:5px 14px;font-size:10px;font-weight:600;cursor:pointer;
  letter-spacing:2px;text-transform:uppercase;transition:all .2s;
}
.nav-logout:hover{border-color:#1A1A1A;color:#1A1A1A}

/* ===== HERO ===== */
.hero{padding:100px 8vw 80px;border-bottom:1px solid #D0CBC5}
.hero-number{font-size:16px;font-weight:400;letter-spacing:1px;color:#999;margin-bottom:40px}
.hero-title{font-size:clamp(48px,10vw,120px);font-weight:900;letter-spacing:-.04em;line-height:1.0;margin-bottom:32px;max-width:700px}
.hero-desc{font-size:clamp(15px,1.8vw,18px);font-weight:300;line-height:1.8;color:#555;max-width:520px;margin-bottom:48px}
.hero-values{border-top:1px solid #D0CBC5;padding-top:24px}
.hero-values-title{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px}
.hero-values-list{display:grid;grid-template-columns:1fr 1fr;gap:12px 32px}
.value-item{display:flex;gap:16px;align-items:baseline}
.value-label{font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;min-width:100px}
.value-text{font-size:14px;font-weight:300;color:#555;line-height:1.6}

/* ===== LITERATURE TAB ===== */
.lit-toolbar{
  padding:48px 8vw 32px;
  max-width:1080px;
  margin:0 auto;
}
.lit-search{
  width:100%;
  padding:14px 18px;
  font-size:15px;
  border:1px solid #D0CBC5;
  border-radius:2px;
  background:#fff;
  color:#1A1A1A;
  outline:none;
  font-family:inherit;
  transition:border-color .2s;
}
.lit-search:focus{border-color:#1A1A1A}
.lit-search::placeholder{color:#aaa}
.lit-filters{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  margin-top:20px;
}
.lit-filter{
  padding:6px 16px;
  font-size:11px;
  font-weight:600;
  letter-spacing:1px;
  text-transform:uppercase;
  border:1px solid #D0CBC5;
  background:transparent;
  color:#666;
  cursor:pointer;
  transition:all .2s;
  font-family:inherit;
}
.lit-filter:hover{border-color:#1A1A1A;color:#1A1A1A}
.lit-filter.active{background:#1A1A1A;color:#E8E4DF;border-color:#1A1A1A}

.lit-grid{
  max-width:1080px;
  margin:0 auto;
  padding:0 8vw 80px;
  display:grid;
  grid-template-columns:1fr;
  gap:0;
}
.lit-card{
  display:grid;
  grid-template-columns:60px 1fr;
  gap:24px;
  padding:36px 0;
  border-bottom:1px solid #D0CBC5;
  cursor:pointer;
  transition:opacity .3s;
  align-items:start;
}
.lit-card:hover{opacity:.6}
.lit-card-number{
  font-size:clamp(36px,5vw,56px);
  font-weight:900;
  letter-spacing:-.04em;
  line-height:1;
  color:#D0CBC5;
}
.lit-card-body{padding-top:4px}
.lit-card-meta{
  font-size:11px;
  font-weight:600;
  letter-spacing:1.5px;
  text-transform:uppercase;
  color:#999;
  margin-bottom:8px;
}
.lit-card-type{
  display:inline-block;
  padding:2px 8px;
  font-size:9px;
  font-weight:700;
  letter-spacing:1px;
  text-transform:uppercase;
  border:1px solid #D0CBC5;
  color:#888;
  margin-right:8px;
}
.lit-card-title{
  font-size:clamp(16px,2vw,20px);
  font-weight:700;
  line-height:1.4;
  margin-bottom:8px;
  letter-spacing:-.01em;
}
.lit-card-journal{
  font-size:13px;
  font-weight:400;
  color:#888;
  font-style:italic;
  margin-bottom:10px;
}
.lit-card-conclusion{
  font-size:13px;
  font-weight:300;
  line-height:1.7;
  color:#666;
}
.lit-empty{
  text-align:center;
  padding:80px 0;
  color:#999;
  font-size:14px;
}

/* ===== PLACEHOLDER TAB ===== */
.placeholder-section{
  max-width:1080px;
  margin:0 auto;
  padding:80px 8vw;
  text-align:center;
  color:#999;
  font-size:14px;
  font-weight:300;
  letter-spacing:1px;
}

/* ===== FOOTER ===== */
.footer{
  border-top:1px solid #D0CBC5;
  padding:40px 8vw;
  text-align:center;
  font-size:10px;
  color:#999;
  letter-spacing:2px;
  text-transform:uppercase;
}

/* ===== RESPONSIVE ===== */
@media(max-width:768px){
  .hero{padding:60px 6vw 48px}
  .hero-values-list{grid-template-columns:1fr}
  .lit-toolbar{padding:32px 6vw 24px}
  .lit-grid{padding:0 6vw 60px}
  .lit-card{grid-template-columns:1fr;gap:8px;padding:28px 0}
  .lit-card-number{font-size:36px}
  .placeholder-section{padding:60px 6vw}
  .nav{padding:0 6vw}
}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <div class="nav-logo">ARISE CLUB</div>
  <div class="nav-right">
    <span class="nav-user" id="navUser"></span>
    <button class="nav-logout" onclick="handleLogout()">退出</button>
  </div>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-number">//01</div>
  <div class="hero-title">Where Strength Meets Science.</div>
  <div class="hero-desc">发生俱乐部 ARISE CLUB — 循证力量训练与运动表现科学</div>
  <div class="hero-values">
    <div class="hero-values-title">Core Values</div>
    <div class="hero-values-list">
      <div class="value-item"><span class="value-label">Fit body</span><span class="value-text">科学训练，构建功能性体魄</span></div>
      <div class="value-item"><span class="value-label">Kind heart</span><span class="value-text">以循证为本，拒绝伪科学</span></div>
      <div class="value-item"><span class="value-label">Focused mind</span><span class="value-text">深度研究，精准执行</span></div>
      <div class="value-item"><span class="value-label">Unbreakable spirit</span><span class="value-text">持续进化，永不止步</span></div>
    </div>
  </div>
</div>

<!-- LITERATURE SECTION -->
<div class="lit-toolbar">
  <input class="lit-search" id="litSearch" type="text" placeholder="搜索文献标题、作者、期刊…">
  <div class="lit-filters" id="litFilters"></div>
</div>
<div class="lit-grid" id="litGrid"></div>

<!-- FOOTER -->
<footer class="footer">&copy; 2026 ARISE CLUB &middot; Where Strength Meets Science</footer>

<script>
(function(){
  var role=localStorage.getItem('vc_role');
  if(!role){window.location.href='login.html';return}
  document.getElementById('navUser').textContent=localStorage.getItem('vc_name')||'用户';
})();
function handleLogout(){['vc_name','vc_user_id','vc_role','vc_invite_code'].forEach(function(k){localStorage.removeItem(k)});window.location.href='login.html'}

var LIT_DATA = ''' + lit_json + ''';

// Count types
var typeCount = {};
LIT_DATA.forEach(function(l){
  var t = l.type || '其他';
  typeCount[t] = (typeCount[t]||0) + 1;
});

// Build filters
var filtersEl = document.getElementById('litFilters');
var allBtn = document.createElement('button');
allBtn.className = 'lit-filter active';
allBtn.textContent = '全部 ' + LIT_DATA.length;
allBtn.dataset.type = 'all';
allBtn.onclick = function(){ setFilter('all') };
filtersEl.appendChild(allBtn);

Object.keys(typeCount).sort(function(a,b){return typeCount[b]-typeCount[a]}).forEach(function(t){
  var btn = document.createElement('button');
  btn.className = 'lit-filter';
  btn.textContent = t + ' ' + typeCount[t];
  btn.dataset.type = t;
  btn.onclick = function(){ setFilter(t) };
  filtersEl.appendChild(btn);
});

var currentFilter = 'all';
var currentSearch = '';

function setFilter(type){
  currentFilter = type;
  document.querySelectorAll('.lit-filter').forEach(function(b){
    b.classList.toggle('active', b.dataset.type === type);
  });
  renderLit();
}

document.getElementById('litSearch').addEventListener('input', function(e){
  currentSearch = e.target.value.toLowerCase();
  renderLit();
});

function renderLit(){
  var grid = document.getElementById('litGrid');
  var filtered = LIT_DATA.filter(function(l){
    if(currentFilter !== 'all' && l.type !== currentFilter) return false;
    if(currentSearch){
      var hay = (l.title + ' ' + l.author + ' ' + l.journal).toLowerCase();
      if(hay.indexOf(currentSearch) === -1) return false;
    }
    return true;
  });

  if(filtered.length === 0){
    grid.innerHTML = '<div class="lit-empty">无匹配文献</div>';
    return;
  }

  grid.innerHTML = filtered.map(function(l, i){
    return '<div class="lit-card">' +
      '<div class="lit-card-number">' + String(i+1).padStart(2,'0') + '</div>' +
      '<div class="lit-card-body">' +
        '<div class="lit-card-meta">' + l.date + ' · ' + l.author + '</div>' +
        '<div class="lit-card-title">' + l.title + '</div>' +
        '<div class="lit-card-journal">' + l.journal + '</div>' +
        '<div class="lit-card-conclusion">' + l.conclusion + '</div>' +
      '</div>' +
    '</div>';
  }).join('');
}

renderLit();
</script>
</body>
</html>'''

with open('/Coze/Drive/Arise/所有对话/主对话/3HFIT/教培中心/姚宁大师课/voice-club/app.html', 'w') as f:
    f.write(html)
print(f"Written app.html with {len(lit_data)} literature items")
