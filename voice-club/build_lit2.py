#!/usr/bin/env python3
"""Build lit.html with inline modal for literature details (no external links)."""
import json, os, re

LIT_DIR = "/Coze/Drive/Arise/所有对话/主对话/循证力量训练/04_每日文献/文献库/文献/"
files = sorted(f for f in os.listdir(LIT_DIR) if f.endswith('.md'))

lit_data = []
for i, fname in enumerate(files, 1):
    fpath = os.path.join(LIT_DIR, fname)
    with open(fpath, 'r') as f:
        content = f.read()

    date_m = re.match(r'(\d{4}-\d{2}-\d{2})_', fname)
    date = date_m.group(1) if date_m else ''

    title_m = re.search(r'^#\s+(.+)$', content, re.M)
    title = title_m.group(1).replace('文献解读：', '').strip() if title_m else fname.replace('.md','')

    author_m = re.search(r'\*\*第一作者\*\*\s*\|\s*(.+?)(?:\s*\|?\s*(?:PhD|MD|BSc)?\s*(?:\n|$))', content)
    if author_m:
        author = re.sub(r',?\s*(PhD|MD|BSc|MSc|FACSM|CSCS).*$', '', author_m.group(1).strip()).strip().rstrip(',').strip()
    else:
        author_m2 = re.search(r'\*\*第一作者\*\*\s*\|\s*(.+?)$', content, re.M)
        author = author_m2.group(1).strip() if author_m2 else ''

    journal_m = re.search(r'\*\*期刊\*\*\s*\|\s*(.+?)$', content, re.M)
    journal = journal_m.group(1).replace(' |','').strip() if journal_m else ''

    doi_m = re.search(r'\*\*DOI\*\*\s*\|\s*(.+?)$', content, re.M)
    doi = doi_m.group(1).strip() if doi_m else ''

    # Extract key sections for modal display
    # Section 一: basic info table
    basic_info = ''
    bi_m = re.search(r'##\s+一[、.].*?文献基本信息.*?\n(.*?)(?=\n##\s+二)', content, re.S)
    if bi_m:
        basic_info = bi_m.group(1).strip()[:500]

    # Section 四 or 五: conclusion
    conclusion = ''
    concl_m = re.search(r'##\s+[四五][、.].*?(?:实践.*?结论|核心结论).*?\n(.*?)(?=\n##|\n---|\Z)', content, re.S)
    if concl_m:
        conclusion = concl_m.group(1).strip()[:300]
    else:
        concl_m2 = re.search(r'##\s+[四五][、.].*?\n\n(.*?)(?=\n##|\n---|\Z)', content, re.S)
        if concl_m2:
            conclusion = concl_m2.group(1).strip()[:300]

    # Full text (first 2000 chars after first heading)
    full_text = ''
    ft_m = re.search(r'^#\s+.+?\n\n(.*?)(?=\n##\s+二)', content, re.S)
    if ft_m:
        full_text = ft_m.group(1).strip()[:1500]

    type_map = {
        'SRMA': 'SR/MA', 'SR_MA': 'SR/MA', 'SR/MA': 'SR/MA',
        'SR': 'SR/MA', 'MA': 'SR/MA',
        'NMA': 'NMA', 'BayesianNMA': 'NMA',
        'UmbrellaReview': '伞评', 'Umbrella': '伞评',
        'RCT': 'RCT', 'PositionStand': '立场声明',
    }
    lit_type = '解读'
    type_m = re.search(r'\*\*文献类型\*\*\s*\|\s*(.+?)$', content, re.M)
    if type_m:
        raw_type = type_m.group(1).strip()
        for key, val in type_map.items():
            if key in raw_type:
                lit_type = val; break
    for key, val in type_map.items():
        if key in fname:
            lit_type = val; break

    # Clean conclusion for display (remove markdown artifacts)
    conclusion_clean = conclusion.replace('**', '').replace('* ', '- ').replace('\n\n', '\n').strip()

    lit_data.append({
        "id": i,
        "date": date,
        "author": author,
        "year": date[:4] if date else '',
        "title": title,
        "type": lit_type,
        "journal": journal,
        "doi": doi,
        "conclusion": conclusion_clean,
        "full_text": full_text.replace('**', '').replace('\n\n', '\n').strip()[:1200]
    })

lit_json = json.dumps(lit_data, ensure_ascii=False)

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

.nav{background:#E8E4DF;border-bottom:1px solid #D0CBC5;padding:0 8vw;height:56px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
.nav-logo{font-size:12px;font-weight:700;letter-spacing:5px;text-transform:uppercase;cursor:pointer}
.nav-right{display:flex;align-items:center;gap:16px}
.nav-user{font-size:12px;color:#888}
.nav-back{background:none;border:1px solid #ccc;color:#888;padding:5px 14px;font-size:10px;font-weight:600;cursor:pointer;letter-spacing:2px;text-transform:uppercase;transition:all .2s;font-family:inherit}
.nav-back:hover{border-color:#1A1A1A;color:#1A1A1A}

.page-header{padding:60px 8vw 40px;border-bottom:1px solid #D0CBC5}
.page-header .back-link{font-size:11px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#999;cursor:pointer;margin-bottom:32px;display:inline-block;transition:color .2s}
.page-header .back-link:hover{color:#1A1A1A}
.page-header h1{font-size:clamp(32px,5vw,56px);font-weight:900;letter-spacing:-.03em;line-height:1.1;margin-bottom:8px}
.page-header .subtitle{font-size:14px;font-weight:300;color:#888}

.toolbar{padding:32px 8vw 24px;max-width:1080px;margin:0 auto}
.search-box{width:100%;padding:14px 18px;font-size:15px;border:1px solid #D0CBC5;border-radius:2px;background:#fff;color:#1A1A1A;outline:none;font-family:inherit;transition:border-color .2s}
.search-box:focus{border-color:#1A1A1A}
.search-box::placeholder{color:#aaa}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.filter-btn{padding:6px 16px;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;border:1px solid #D0CBC5;background:transparent;color:#666;cursor:pointer;transition:all .2s;font-family:inherit}
.filter-btn:hover{border-color:#1A1A1A;color:#1A1A1A}
.filter-btn.active{background:#1A1A1A;color:#E8E4DF;border-color:#1A1A1A}

.lit-list{max-width:1080px;margin:0 auto;padding:0 8vw 80px}
.lit-item{display:grid;grid-template-columns:60px 1fr;gap:24px;padding:36px 0;border-bottom:1px solid #D0CBC5;cursor:pointer;transition:opacity .3s;align-items:start}
.lit-item:hover{opacity:.6}
.lit-num{font-size:clamp(36px,5vw,56px);font-weight:900;letter-spacing:-.04em;line-height:1;color:#D0CBC5}
.lit-body{padding-top:4px}
.lit-meta{font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#999;margin-bottom:8px}
.lit-type-tag{display:inline-block;padding:2px 8px;font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;border:1px solid #D0CBC5;color:#888;margin-right:8px}
.lit-title{font-size:clamp(16px,2vw,20px);font-weight:700;line-height:1.4;margin-bottom:8px;letter-spacing:-.01em}
.lit-journal{font-size:13px;font-weight:400;color:#888;font-style:italic;margin-bottom:10px}
.lit-conclusion{font-size:13px;font-weight:300;line-height:1.7;color:#666}
.lit-empty{text-align:center;padding:80px 0;color:#999;font-size:14px}

/* ===== MODAL ===== */
.modal-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);z-index:200;justify-content:center;align-items:flex-start;padding:40px 20px;overflow-y:auto}
.modal-overlay.active{display:flex}
.modal{background:#E8E4DF;max-width:720px;width:100%;padding:48px;border-radius:2px;position:relative;max-height:90vh;overflow-y:auto}
.modal-close{position:absolute;top:16px;right:20px;background:none;border:none;font-size:24px;cursor:pointer;color:#888;font-family:inherit;transition:color .2s}
.modal-close:hover{color:#1A1A1A}
.modal-number{font-size:14px;font-weight:400;letter-spacing:1px;color:#999;margin-bottom:24px}
.modal-title{font-size:clamp(22px,3vw,32px);font-weight:900;letter-spacing:-.02em;line-height:1.2;margin-bottom:16px}
.modal-meta{font-size:12px;color:#888;margin-bottom:8px}
.modal-journal{font-size:13px;font-style:italic;color:#888;margin-bottom:24px;padding-bottom:24px;border-bottom:1px solid #D0CBC5}
.modal-section-title{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#999;margin-bottom:12px;margin-top:32px}
.modal-text{font-size:14px;font-weight:300;line-height:1.8;color:#444;white-space:pre-wrap}
.modal-doi{font-size:12px;color:#888;margin-top:24px;padding-top:16px;border-top:1px solid #D0CBC5}
.modal-doi a{color:#666;text-decoration:underline}

.footer{border-top:1px solid #D0CBC5;padding:40px 8vw;text-align:center;font-size:10px;color:#999;letter-spacing:2px;text-transform:uppercase}

@media(max-width:768px){
  .page-header,.toolbar,.lit-list{padding-left:6vw;padding-right:6vw}
  .lit-item{grid-template-columns:1fr;gap:8px;padding:28px 0}
  .lit-num{font-size:36px}
  .nav{padding:0 6vw}
  .modal{padding:32px 24px}
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

<!-- MODAL -->
<div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
  <div class="modal" id="modalContent">
    <button class="modal-close" onclick="closeModal()">&times;</button>
    <div id="modalBody"></div>
  </div>
</div>

<footer class="footer">&copy; 2026 ARISE CLUB &middot; Where Strength Meets Science</footer>

<script>
(function(){
  var role=localStorage.getItem('vc_role');
  if(!role){window.location.href='login.html';return}
  document.getElementById('navUser').textContent=localStorage.getItem('vc_name')||'用户';
})();

var LIT_DATA = ''' + lit_json + ''';

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

function renderLit(){
  var list=document.getElementById('litList');
  var filtered=LIT_DATA.filter(function(l){
    if(currentFilter!=='all'&&l.type!==currentFilter)return false;
    if(currentSearch){var hay=(l.title+' '+l.author+' '+l.journal).toLowerCase();if(hay.indexOf(currentSearch)===-1)return false}
    return true;
  });

  if(filtered.length===0){list.innerHTML='<div class="lit-empty">无匹配文献</div>';return}

  list.innerHTML=filtered.map(function(l,i){
    return '<div class="lit-item" onclick="openModal('+l.id+')">' +
      '<div class="lit-num">'+String(i+1).padStart(2,'0')+'</div>' +
      '<div class="lit-body">' +
        '<div class="lit-meta">'+l.date+' · '+l.author+'</div>' +
        '<div class="lit-title"><span class="lit-type-tag">'+l.type+'</span>'+escHtml(l.title)+'</div>' +
        '<div class="lit-journal">'+escHtml(l.journal)+'</div>' +
        '<div class="lit-conclusion">'+escHtml(l.conclusion)+'</div>' +
      '</div>' +
    '</div>';
  }).join('');
}

function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}

function openModal(id){
  var l=LIT_DATA.find(function(x){return x.id===id});
  if(!l)return;
  var html='<div class="modal-number">#'+String(l.id).padStart(3,'0')+'</div>';
  html+='<div class="modal-title">'+escHtml(l.title)+'</div>';
  html+='<div class="modal-meta">'+l.date+' · '+escHtml(l.author)+'</div>';
  html+='<div class="modal-journal">'+escHtml(l.journal)+(l.doi?' · DOI: '+l.doi:'')+'</div>';
  if(l.full_text){
    html+='<div class="modal-section-title">文献解读</div>';
    html+='<div class="modal-text">'+escHtml(l.full_text)+'</div>';
  }
  if(l.conclusion){
    html+='<div class="modal-section-title">核心结论</div>';
    html+='<div class="modal-text">'+escHtml(l.conclusion)+'</div>';
  }
  if(l.doi){
    html+='<div class="modal-doi">DOI: <a href="https://doi.org/'+escHtml(l.doi)+'" target="_blank">'+escHtml(l.doi)+'</a></div>';
  }
  document.getElementById('modalBody').innerHTML=html;
  document.getElementById('modalOverlay').classList.add('active');
  document.body.style.overflow='hidden';
}

function closeModal(e){
  if(e&&e.target!==document.getElementById('modalOverlay')&&!e.target.classList.contains('modal-close'))return;
  document.getElementById('modalOverlay').classList.remove('active');
  document.body.style.overflow='';
}

document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal()});

renderLit();
</script>
</body>
</html>'''

with open('/Coze/Drive/Arise/所有对话/主对话/3HFIT/教培中心/姚宁大师课/voice-club/lit.html', 'w') as f:
    f.write(html)
print(f"Written lit.html with {len(lit_data)} items, inline modal enabled")
