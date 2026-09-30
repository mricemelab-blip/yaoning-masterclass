#!/usr/bin/env python3
"""Extract metadata from all 79 literature .md files and output LIT_DATA JSON + HTML tab content."""
import os, json, re

LIT_DIR = "/Coze/Drive/Arise/所有对话/主对话/循证力量训练/04_每日文献/文献库/文献/"
files = sorted(f for f in os.listdir(LIT_DIR) if f.endswith('.md'))

type_map = {
    'SRMA': 'SR/MA', 'SR_MA': 'SR/MA', 'SR/MA': 'SR/MA',
    'SR': 'SR/MA', 'MA': 'SR/MA', 'SRMA': 'SR/MA',
    'NMA': 'NMA', 'BayesianNMA': 'NMA',
    'UmbrellaReview': '伞评', '伞形评价': '伞评', 'Umbrella': '伞评',
    'RCT': 'RCT', 'PositionStand': '立场声明', '立场声明': '立场声明',
}

lit_data = []
for i, fname in enumerate(files, 1):
    fpath = os.path.join(LIT_DIR, fname)
    with open(fpath, 'r') as f:
        content = f.read()

    # Extract date from filename
    date_m = re.match(r'(\d{4}-\d{2}-\d{2})_', fname)
    date = date_m.group(1) if date_m else ''

    # Extract title from first # heading
    title_m = re.search(r'^#\s+(.+)$', content, re.M)
    title = title_m.group(1).replace('文献解读：', '').strip() if title_m else fname.replace('.md','')

    # Extract author
    author_m = re.search(r'\*\*第一作者\*\*\s*\|\s*(.+?)(?:\s*\|?\s*(?:PhD|MD|BSc)?\s*(?:\n|$))', content)
    if author_m:
        author = author_m.group(1).strip().rstrip(',').strip()
        # Clean up credentials
        author = re.sub(r',?\s*(PhD|MD|BSc|MSc|FACSM|CSCS).*$', '', author).strip()
    else:
        author_m2 = re.search(r'\*\*第一作者\*\*\s*\|\s*(.+?)$', content, re.M)
        author = author_m2.group(1).strip() if author_m2 else ''

    # Extract journal
    journal_m = re.search(r'\*\*期刊\*\*\s*\|\s*(.+?)$', content, re.M)
    journal = journal_m.group(1).strip() if journal_m else ''

    # Extract lit type from filename or content
    lit_type = '解读'
    # Check content for type
    type_m = re.search(r'\*\*文献类型\*\*\s*\|\s*(.+?)$', content, re.M)
    if type_m:
        raw_type = type_m.group(1).strip()
        for key, val in type_map.items():
            if key in raw_type:
                lit_type = val
                break
    # Also check filename
    for key, val in type_map.items():
        if key in fname:
            lit_type = val
            break

    # Extract conclusion from section 五
    conclusion = ''
    concl_m = re.search(r'##\s+五[、.].*?实践.*?结论.*?\n(.*?)(?=\n##|\n---|\Z)', content, re.S)
    if concl_m:
        conclusion = concl_m.group(1).strip()[:200]
    else:
        # Fallback: grab first paragraph after 五
        concl_m2 = re.search(r'##\s+五[、.].*?\n\n(.*?)(?=\n##|\n---|\Z)', content, re.S)
        if concl_m2:
            conclusion = concl_m2.group(1).strip()[:200]

    lit_data.append({
        "id": i,
        "date": date,
        "author": author,
        "year": date[:4] if date else '',
        "title": title,
        "type": lit_type,
        "journal": journal,
        "conclusion": conclusion
    })

# Output JSON
print(json.dumps(lit_data, ensure_ascii=False, indent=2))
