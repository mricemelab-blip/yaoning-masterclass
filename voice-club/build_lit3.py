import json, os, re

LIT_DIR = "/Coze/Drive/Arise/所有对话/主对话/循证力量训练/04_每日文献/文献库/文献"
OUTPUT = "/Coze/Drive/Arise/所有对话/主对话/3HFIT/教培中心/姚宁大师课/voice-club/lit.html"

files = sorted([f for f in os.listdir(LIT_DIR) if f.endswith('.md')])
items = []

for fname in files:
    path = os.path.join(LIT_DIR, fname)
    with open(path, 'r') as f:
        content = f.read()
    lines = content.split('\n')
    
    title = author = journal = date = lit_type = doi = ''
    for line in lines:
        ls = line.strip()
        if '**标题**' in ls:
            m = re.search(r'\*\*标题\*\*\s*\|\s*(.+)', ls)
            if m: title = m.group(1).strip()
        if '**第一作者**' in ls:
            m = re.search(r'\*\*第一作者\*\*\s*\|\s*(.+)', ls)
            if m: author = m.group(1).strip()
        if '**期刊**' in ls:
            m = re.search(r'\*\*期刊\*\*\s*\|\s*(.+)', ls)
            if m: journal = m.group(1).strip()
        if '**DOI**' in ls:
            m = re.search(r'(10\.\S+)', ls)
            if m: doi = m.group(1).strip()
        if '**文献类型**' in ls:
            m = re.search(r'\*\*文献类型\*?\*?\s*\|\s*(.+)', ls)
            if m: lit_type = m.group(1).strip()
        if not date:
            m = re.search(r'(\d{4}-\d{2}-\d{2})', ls)
            if m: date = m.group(1)

    sections = []
    cur_sec = ''
    cur_body = []
    skip_cast = False
    for line in lines:
        if line.startswith('## 开口播稿'):
            skip_cast = True
            if cur_sec:
                sections.append((cur_sec, '\n'.join(cur_body)))
            break
        if line.startswith('## '):
            if cur_sec:
                sections.append((cur_sec, '\n'.join(cur_body)))
            cur_sec = line[3:].strip()
            cur_body = []
        elif not skip_cast:
            cur_body.append(line)
    if cur_sec and not skip_cast:
        sections.append((cur_sec, '\n'.join(cur_body)))

    def md_table_to_html(text):
        parts = []
        in_table = False
        for tl in text.split('\n'):
            if '|' in tl and tl.strip().startswith('|'):
                cells = [c.strip() for c in tl.split('|')[1:-1]]
                if all(set(c) <= set('-: ') for c in cells):
                    continue
                if not in_table:
                    parts.append('<table>')
                    in_table = True
                if any('**' in c for c in cells):
                    row = '<tr>' + ''.join('<th>%s</th>' % c.replace('**','') for c in cells) + '</tr>'
                else:
                    row = '<tr>' + ''.join('<td>%s</td>' % c for c in cells) + '</tr>'
                parts.append(row)
            else:
                if in_table:
                    parts.append('</table>')
                    in_table = False
                parts.append(tl)
        if in_table:
            parts.append('</table>')
        return '\n'.join(parts)

    def md_to_html(text):
        text = md_table_to_html(text)
        text = re.sub(r'^### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)
        text = re.sub(r'^---$', '<hr>', text, flags=re.MULTILINE)
        text = re.sub(r'^[\-\*] (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'((?:<li>.*?</li>\s*)+)', r'<ul>\1</ul>', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text

    section_html = ''
    for sec_title, sec_body in sections:
        section_html += '<div class="lit-section"><h3>%s</h3>%s</div>' % (sec_title, md_to_html(sec_body))

    type_cat = '解读'
    lt_upper = lit_type.upper()
    if 'SYSTEMATIC' in lt_upper or 'META' in lt_upper or 'SR/MA' in lit_type or 'SYSTEM' in lt_upper:
        type_cat = 'SR/MA'
    elif 'RCT' in lt_upper or 'RANDOMIZED' in lt_upper:
        type_cat = 'RCT'
    elif 'UMBRELLA' in lt_upper or '伞' in lit_type:
        type_cat = '伞评'
    elif 'POSITION' in lt_upper or '立场' in lit_type:
        type_cat = '立场声明'

    conclusion = ''
    for sec_title, sec_body in sections:
        if '核心结论' in sec_title or '主要结果' in sec_title:
            for pl in sec_body.split('\n'):
                pl = pl.strip()
                if pl and not pl.startswith('|') and not pl.startswith('#') and len(pl) > 30:
                    conclusion = pl[:200]
                    break
            if conclusion:
                break

    items.append({
        'id': fname.replace('.md', ''),
        'title': title or fname,
        'author': author or '未知',
        'journal': journal or '未知',
        'date': date,
        'type': type_cat,
        'type_full': lit_type,
        'doi': doi,
        'conclusion': conclusion,
        'sections_html': section_html
    })

type_counts = {}
for it in items:
    t = it['type']
    type_counts[t] = type_counts.get(t, 0) + 1
print('Total: %d, Types: %s' % (len(items), type_counts))

LIT_JSON = json.dumps(items, ensure_ascii=False)

# Build filter buttons
filter_buttons = '<button class="tf-btn active" data-type="全部">全部 %d</button>' % len(items)
for t in ['SR/MA', '解读', 'RCT', '伞评', '立场声明']:
    if t in type_counts:
        filter_buttons += '<button class="tf-btn" data-type="%s">%s %d</button>\n' % (t, t, type_counts[t])

# Escape for JS
LIT_JSON_ESC = LIT_JSON.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>文献解读 - ARISE CLUB</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#E8E4DF;font-family:'Arial Black',Arial,sans-serif;color:#111;min-height:100vh}
.nav{background:#000;padding:16px 32px;display:flex;justify-content:space-between;align-items:center}
.nav-brand{color:#C8F230;font-size:12px;letter-spacing:3px;font-weight:700}
.nav-back{color:#888;text-decoration:none;font-size:13px;letter-spacing:2px;transition:color .2s}
.nav-back:hover{color:#C8F230}
.lit-header{padding:48px 32px 24px;max-width:1200px;margin:0 auto}
.lit-header .number{font-size:13px;color:#C8F230;font-weight:700;letter-spacing:2px}
.lit-header h1{font-size:clamp(28px,4vw,42px);font-weight:900;line-height:1.15;margin-top:8px}
.lit-toolbar{padding:0 32px 24px;max-width:1200px;margin:0 auto}
.lit-search{width:100%;padding:14px 18px;border:2px solid #ccc;background:#fff;font-size:14px;font-family:Arial,sans-serif;border-radius:0;outline:none;margin-bottom:16px;transition:border-color .2s}
.lit-search:focus{border-color:#C8F230}
.lit-filters{display:flex;flex-wrap:wrap;gap:8px}
.tf-btn{padding:8px 18px;border:2px solid #ccc;background:#fff;font-size:13px;font-weight:700;cursor:pointer;font-family:'Arial Black',Arial,sans-serif;transition:all .15s}
.tf-btn.active,.tf-btn:hover{background:#000;color:#C8F230;border-color:#000}
.lit-list{max-width:1200px;margin:0 auto;padding:0 32px 80px}
.lit-card{padding:40px 0;border-bottom:1px solid #ccc;cursor:pointer;transition:opacity .2s}
.lit-card:hover{opacity:.7}
.lit-card-num{font-size:clamp(40px,5vw,64px);font-weight:900;color:#ccc;line-height:1;margin-right:20px;float:left}
.lit-card-body{overflow:hidden}
.lit-card-meta{font-size:12px;color:#888;letter-spacing:1px;margin-bottom:6px}
.lit-card-title{font-size:clamp(16px,2vw,22px);font-weight:900;line-height:1.3;margin-bottom:6px}
.lit-card-journal{font-size:13px;color:#666;font-style:italic;margin-bottom:10px}
.lit-card-conclusion{font-size:13px;color:#555;line-height:1.6;font-family:Georgia,serif}
.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);z-index:1000;overflow-y:auto}
.modal-overlay.show{display:block}
.modal-content{max-width:800px;margin:40px auto;background:#F5F2ED;padding:48px;position:relative;min-height:80vh}
.modal-close{position:fixed;top:20px;right:28px;font-size:28px;color:#fff;cursor:pointer;z-index:1001;background:none;border:none;font-family:Arial}
.modal-title{font-size:28px;font-weight:900;line-height:1.3;margin-bottom:8px}
.modal-meta{font-size:13px;color:#888;margin-bottom:32px;padding-bottom:20px;border-bottom:2px solid #000}
.modal-doi{color:#C8F230;text-decoration:none;font-weight:700}
.lit-section{margin-bottom:32px}
.lit-section h3{font-size:18px;font-weight:900;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #ddd}
.lit-section h4{font-size:15px;font-weight:700;margin:16px 0 8px}
.lit-section p{font-size:14px;line-height:1.8;margin-bottom:12px;font-family:Georgia,serif}
.lit-section table{width:100%;border-collapse:collapse;margin:12px 0;font-size:13px}
.lit-section th{background:#000;color:#C8F230;padding:8px 12px;text-align:left;font-weight:700}
.lit-section td{padding:8px 12px;border-bottom:1px solid #ddd}
.lit-section blockquote{border-left:3px solid #C8F230;padding:8px 16px;margin:12px 0;background:rgba(200,242,48,.05);font-size:14px;line-height:1.7}
.lit-section ul{margin:8px 0 8px 20px;font-size:14px;line-height:1.8;font-family:Georgia,serif}
.lit-section hr{border:none;border-top:1px solid #ddd;margin:16px 0}
.lit-section strong{color:#000}
@media(max-width:768px){
.lit-header,.lit-toolbar,.lit-list{padding-left:16px;padding-right:16px}
.modal-content{margin:0;padding:24px;min-height:100vh}
.lit-card-num{float:none;margin-bottom:8px}
}
</style>
</head>
<body>
<nav class="nav"><span class="nav-brand">ARISE CLUB</span><a href="app.html" class="nav-back">← 返回</a></nav>
<div class="lit-header"><div class="number">//01</div><h1>文献解读</h1></div>
<div class="lit-toolbar">
<input type="text" class="lit-search" id="litSearch" placeholder="搜索文献标题、作者、期刊...">
<div class="lit-filters" id="litFilters">
__FILTERS__
</div></div>
<div class="lit-list" id="litList"></div>
<div class="modal-overlay" id="modalOverlay">
<button class="modal-close" id="modalClose">&#10005;</button>
<div class="modal-content" id="modalContent"></div>
</div>
<script>
var LIT_DATA=__LIT_DATA__;
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function renderCard(item,idx){
return '<div class="lit-card" data-idx="'+idx+'"><div class="lit-card-num">'+String(idx+1).padStart(2,'0')+'</div><div class="lit-card-body"><div class="lit-card-meta">'+esc(item.date||'')+' &middot; '+esc(item.author)+'</div><div class="lit-card-title">'+esc(item.title)+'</div><div class="lit-card-journal">'+esc(item.journal)+'</div>'+(item.conclusion?'<div class="lit-card-conclusion">'+esc(item.conclusion)+'</div>':'')+'</div></div>'}
var currentType='全部',currentSearch='';
function renderList(){
var list=document.getElementById('litList');
var filtered=LIT_DATA.filter(function(item,idx){
var mt=currentType==='全部'||item.type===currentType;
var q=currentSearch.toLowerCase();
var ms=!q||item.title.toLowerCase().indexOf(q)>-1||item.author.toLowerCase().indexOf(q)>-1||item.journal.toLowerCase().indexOf(q)>-1;
return mt&&ms});
if(!filtered.length){list.innerHTML='<div style="padding:60px 0;text-align:center;color:#999;font-size:15px">暂无匹配文献</div>';return}
list.innerHTML=filtered.map(function(item){var origIdx=LIT_DATA.indexOf(item);return renderCard(item,origIdx)}).join('');
document.querySelectorAll('.lit-card').forEach(function(card){card.addEventListener('click',function(){openModal(parseInt(this.getAttribute('data-idx')))})})}
function openModal(idx){
var item=LIT_DATA[idx];
var doiLink=item.doi?'<a class="modal-doi" href="https://doi.org/'+esc(item.doi)+'" target="_blank">DOI: '+esc(item.doi)+'</a>':'';
var html='<div class="modal-title">'+esc(item.title)+'</div><div class="modal-meta">'+esc(item.author)+' &middot; '+esc(item.journal)+(item.date?' &middot; '+esc(item.date):'')+(doiLink?'<br>'+doiLink:'')+'</div>'+item.sections_html;
document.getElementById('modalContent').innerHTML=html;
document.getElementById('modalOverlay').classList.add('show');
document.body.style.overflow='hidden'}
function closeModal(){document.getElementById('modalOverlay').classList.remove('show');document.body.style.overflow=''}
document.getElementById('modalClose').addEventListener('click',closeModal);
document.getElementById('modalOverlay').addEventListener('click',function(e){if(e.target===this)closeModal()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal()});
document.getElementById('litSearch').addEventListener('input',function(){currentSearch=this.value;renderList()});
document.getElementById('litFilters').addEventListener('click',function(e){if(e.target.classList.contains('tf-btn')){document.querySelectorAll('.tf-btn').forEach(function(b){b.classList.remove('active')});e.target.classList.add('active');currentType=e.target.getAttribute('data-type');renderList()}});
renderList();
</script>
</body>
</html>'''

html = html.replace('__FILTERS__', filter_buttons)
html = html.replace('__LIT_DATA__', LIT_JSON_ESC)

with open(OUTPUT, 'w') as f:
    f.write(html)
print('Written %s' % OUTPUT)
