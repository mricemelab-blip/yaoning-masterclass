#!/usr/bin/env python3
"""Build lit.html - separate literature list page with links to full interpretations."""
import json

lit_data = json.load(open('/Coze/Drive/Arise/所有对话/主对话/3HFIT/教培中心/姚宁大师课/voice-club/lit_data.json'))

# Build URL mapping: each literature links to the evidence-literature-db
# The literature website is at: https://mricemelab-blip.github.io/evidence-literature-db/
# Files are named like: 2026-06-05_Currier2026_ACSM_ResistanceTraining_PositionStand.html

lit_links = {}
import os
LIT_DIR = "/Coze/Drive/Arise/所有对话/主对话/循证力量训练/04_每日文献/文献库/文献/"
for f in os.listdir(LIT_DIR):
    if f.endswith('.md'):
        base = f.replace('.md', '')
        lit_links[base] = f"https://mricemelab-blip.github.io/evidence-literature-db/{base}.html"

lit_json = json.dumps(lit_data, ensure_ascii=False)

# Build link map as JS object
link_obj = {}
for f in os.listdir(LIT_DIR):
    if f.endswith('.md'):
        base = f.replace('.md', '')
        link_obj[base] = f"https://mricemelab-blip.github.io/evidence-literature-db/{base}.html"
link_json = json.dumps(link_obj, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>文献解读 - ARISE CLUB</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  font-family:'Helvetica Neue','Arial Black',Arial,'PingFang SC','Noto Sans SC',sans-serif;
  background:#E8E4DF;
  color:#1A1A1A;
  line-height:1.6;
  -webkit-font-smoothing:antialiased;
}

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
.nav-logo{font-size:12px;font-weight:700;letter-spacing:5px;text-transform:uppercase;cursor:pointer}
.nav-right{display:flex;align-items:center;gap:16px}
.nav-user{font-size:12px;color:#888}
.nav-back{
  background:none;border:1px solid #ccc;color:#888;
  padding:5px 14px;font-size:10px;font-weight:600;cursor:pointer;
  letter-spacing:2px;text-transform:uppercase;transition:all .2s;
  font-family:inherit;
}
.nav-back:hover{border-color:#1A1A1A;color:#1A1A1A}

/* ===== PAGE HEADER ===== */
.page-header{
  padding:60px 8vw 40px;
  border-bottom:1px solid #D0CBC5;
}
.page-header .back-link{
  font-size:11px;
  font-weight:600;
  letter-spacing:2px;
  text-transform:uppercase;
  color:#999;
  cursor:pointer;
  margin-bottom:32px;
  display:inline-block;
  transition:color .2s;
}
.page-header .back-link:hover{color:#1A1A1A}
.page-header h1{
  font-size:clamp(32px,5vw,56px);
  font-weight:900;
  letter-spacing:-.03em;
  line-height:1.1;
  margin-bottom:8px;
}
.page-header .subtitle{
  font-size:14px;
  font-weight:300;
  color:#888;
}

/* ===== TOOLBAR ===== */
.toolbar{
  padding:32px 8vw 24px;
  max-width:1080px;
  margin:0 auto;
}
.search-box{
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
.search-box:focus{border-color:#1A1A1A}
.search-box::placeholder{color:#aaa}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.filter-btn{
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
.filter-btn:hover{border-color:#1A1A1A;color:#1A1A1A}
.filter-btn.active{background:#1A1A1A;color:#E8E4DF;border-color:#1A1A1A}

/* ===== LIT LIST ===== */
.lit-list{max-width:1080px;margin:0 auto;padding:0 8vw 80px}
.lit-item{
  display:grid;
  grid-template-columns:60px 1fr;
  gap:24px;
  padding:36px 0;
  border-bottom:1px solid #D0CBC5;
  cursor:pointer;
  transition:opacity .3s;
  align-items:start;
}
.lit-item:hover{opacity:.6}
.lit-num{
  font-size:clamp(36px,5vw,56px);
  font-weight:900;
  letter-spacing:-.04em;
  line-height:1;
  color:#D0CBC5;
}
.lit-body{padding-top:4px}
.lit-meta{
  font-size:11px;
  font-weight:600;
  letter-spacing:1.5px;
  text-transform:uppercase;
  color:#999;
  margin-bottom:8px;
}
.lit-type-tag{
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
.lit-title{
  font-size:clamp(16px,2vw,20px);
  font-weight:700;
  line-height:1.4;
  margin-bottom:8px;
  letter-spacing:-.01em;
}
.lit-journal{
  font-size:13px;
  font-weight:400;
  color:#888;
  font-style:italic;
  margin-bottom:10px;
}
.lit-conclusion{
  font-size:13px;
  font-weight:300;
  line-height:1.7;
  color:#666;
}
.lit-empty{text-align:center;padding:80px 0;color:#999;font-size:14px}

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

@media(max-width:768px){
  .page-header,.toolbar,.lit-list{padding-left:6vw;padding-right:6vw}
  .lit-item{grid-template-columns:1fr;gap:8px;padding:28px 0}
  .lit-num{font-size:36px}
  .nav{padding:0 6vw}
}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-logo" onclick="location.href='app.html'">ARISE CLUB</div>
  <div class="nav-right">
    <span class="nav-user" id="navUser"></span>
    <button class="nav-back" onclick="location.href='app.html'">返回</button>
  </div>
</nav>

<div class="page-header">
  <div class="back-link" onclick="location.href='app.html'">&larr; 返回首页</div>
  <h1>文献解读</h1>
  <div class="subtitle">Evidence-Based Literature Review &middot; <span id="litCount"></span> 篇</div>
</div>

<div class="toolbar">
  <input class="search-box" id="litSearch" type="text" placeholder="搜索文献标题、作者、期刊…">
  <div class="filters" id="litFilters"></div>
</div>

<div class="lit-list" id="litList"></div>

<footer class="footer">&copy; 2026 ARISE CLUB &middot; Where Strength Meets Science</footer>

<script>
(function(){
  var role=localStorage.getItem('vc_role');
  if(!role){window.location.href='login.html';return}
  document.getElementById('navUser').textContent=localStorage.getItem('vc_name')||'用户';
})();

var LIT_DATA = ''' + lit_json + ''';
var LIT_LINKS = ''' + link_json + ''';

document.getElementById('litCount').textContent = LIT_DATA.length;

var typeCount={};
LIT_DATA.forEach(function(l){var t=l.type||'其他';typeCount[t]=(typeCount[t]||0)+1});

var filtersEl=document.getElementById('litFilters');
var allBtn=document.createElement('button');
allBtn.className='filter-btn active';
allBtn.textContent='全部 '+LIT_DATA.length;
allBtn.dataset.type='all';
allBtn.onclick=function(){setFilter('all')};
filtersEl.appendChild(allBtn);

Object.keys(typeCount).sort(function(a,b){return typeCount[b]-typeCount[a]}).forEach(function(t){
  var btn=document.createElement('button');
  btn.className='filter-btn';
  btn.textContent=t+' '+typeCount[t];
  btn.dataset.type=t;
  btn.onclick=function(){setFilter(t)};
  filtersEl.appendChild(btn);
});

var currentFilter='all',currentSearch='';

function setFilter(type){
  currentFilter=type;
  document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.toggle('active',b.dataset.type===type)});
  renderLit();
}

document.getElementById('litSearch').addEventListener('input',function(e){currentSearch=e.target.value.toLowerCase();renderLit()});

function getLink(item){
  // Try to match by date+author pattern in LIT_LINKS keys
  for(var key in LIT_LINKS){
    var k=key.toLowerCase();
    if(k.indexOf(item.date.replace(/-/g,''))!==-1 || k.indexOf(item.author.split(' ').pop().toLowerCase())!==-1){
      return LIT_LINKS[key];
    }
  }
  return null;
}

function renderLit(){
  var list=document.getElementById('litList');
  var filtered=LIT_DATA.filter(function(l){
    if(currentFilter!=='all'&&l.type!==currentFilter)return false;
    if(currentSearch){var hay=(l.title+' '+l.author+' '+l.journal).toLowerCase();if(hay.indexOf(currentSearch)===-1)return false}
    return true;
  });

  if(filtered.length===0){list.innerHTML='<div class="lit-empty">无匹配文献</div>';return}

  list.innerHTML=filtered.map(function(l,i){
    var link=getLink(l);
    var clickAttr=link?'onclick="window.open(\\''+link+'\\',\\'_blank\\')"':'onclick="alert(\\'文献解读页面链接待配置\\')"';
    return '<div class="lit-item" '+clickAttr+'>' +
      '<div class="lit-num">'+String(i+1).padStart(2,'0')+'</div>' +
      '<div class="lit-body">' +
        '<div class="lit-meta">'+l.date+' · '+l.author+'</div>' +
        '<div class="lit-title"><span class="lit-type-tag">'+l.type+'</span>'+l.title+'</div>' +
        '<div class="lit-journal">'+l.journal+'</div>' +
        '<div class="lit-conclusion">'+l.conclusion+'</div>' +
      '</div>' +
    '</div>';
  }).join('');
}

renderLit();
</script>
</body>
</html>'''

with open('/Coze/Drive/Arise/所有对话/主对话/3HFIT/教培中心/姚宁大师课/voice-club/lit.html', 'w') as f:
    f.write(html)
print(f"Written lit.html with {len(lit_data)} items and {len(link_obj)} links")
