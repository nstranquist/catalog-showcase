#!/usr/bin/env python3
"""Repeatable public projection pipeline for Nico's software catalog.

Fetch (GitHub connector, sequential+retries) -> Project (PublicEntity DTO
fields only, mirroring nicos-catalog projection.go) -> Hygiene (public tag
rules) -> Validate (prohibited-content scan, DTO key check) -> Report.

Usage: python3 pipeline.py [--skip-fetch]
Outputs: public-products.json, projection-audit.md, raw/ (corpus cache)
"""
import subprocess, json, os, re, sys, time
from collections import Counter
from urllib.parse import urlparse
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OWNER, REPO = "nstranquist", "nicos-tools"
DIR = "nicos-dev/docs/feature-catalog/products"

DROP_TAGS = {"manual", "product"}  # hygiene: provenance marker + kind duplicate

PROHIB = [
    (re.compile(r'(?i)(?:/users/[^/\s]+/|/home/[^/\s]+/|file://|~/|(?:^|[\s"\'(])[a-z]:\\)'), 'path-disclosure'),
    (re.compile(r'(?i)\b(?:private-admin-evidence|sources/(?:originals|extracted-text)|\.jobkit|\.ssh)\b'), 'internal-path'),
    (re.compile(r'(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*\S+'), 'credential-pair'),
    (re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})\b'), 'token-shape'),
]
def scan(text):
    # NOTE: ids like product.jobkit legitimately contain a prohibited-looking
    # token; scan is for prose fields only, callers pass summaries/tags/names.
    for pat, rule in PROHIB:
        if pat.search(text or ''):
            return rule
    return None

def gh_read(path, retries=3):
    for attempt in range(retries):
        out = subprocess.run(["/opt/hatch/bin/github", "call-read-tool", "--name",
                              "get_file_contents", "--arguments-json",
                              json.dumps({"owner": OWNER, "repo": REPO, "path": path})],
                             capture_output=True, text=True)
        try:
            d = json.loads(out.stdout)
            contents = d['result']['content']
            for c in contents:
                if 'resource' in c:
                    return c['resource'].get('text', '')
            return contents[0].get('text', '')
        except Exception:
            time.sleep(2)
    return ""

def fetch():
    os.makedirs(RAW, exist_ok=True)
    listing = gh_read(DIR)
    items = json.loads(listing)
    names = [i['name'] for i in items if i['name'].startswith('product.')]
    print(f"fetch: {len(names)} product files")
    for name in names:
        dest = os.path.join(RAW, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 100:
            continue
        txt = gh_read(f"{DIR}/{name}")
        open(dest, 'w').write(txt or "")
        print(" fetched", name, len(txt or ""))
        time.sleep(0.4)
    return names

def bound_summary(text, maxb=320):
    s = ' '.join((text or '').split())
    if len(s.encode()) <= maxb:
        return s
    cut = s.encode()[:maxb - 3].decode(errors='ignore')
    if ' ' in cut:
        cut = cut.rsplit(' ', 1)[0]
    return cut + '…'

def project():
    raw, audit = {}, []
    for fn in sorted(os.listdir(RAW)):
        txt = open(os.path.join(RAW, fn)).read()
        m = re.match(r'^---\n(.*?)\n---\n?(.*)$', txt, re.S)
        if not m:
            audit.append(f"- {fn}: NO FRONTMATTER — skipped"); continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except Exception as e:
            audit.append(f"- {fn}: YAML parse error — skipped"); continue
        raw[fm.get('id', '')] = (fm, m.group(2).strip(), fn)
    all_ids = set(raw)
    items = []
    for pid, (fm, body, fn) in sorted(raw.items()):
        notes = []
        paras = []
        for block in re.split(r'\n\s*\n', body):
            b = block.strip()
            if not b or b.startswith(('#', '```', '|', '- ', '> ')):
                continue
            paras.append(b); break
        summary_raw = paras[0] if paras else ''
        summary_raw = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', summary_raw)
        summary_raw = summary_raw.replace('`', '').replace('**', '').replace('*', '')
        # Local raw cache marks withheld credential tokens as [withheld];
        # never publish the marker — drop the token (and a preceding " / ").
        summary_raw = re.sub(r'\s*/\s*\[withheld\]', '', summary_raw).replace('[withheld]', '')
        if scan(summary_raw):
            notes.append("summary dropped (prohibited content)"); summary = ''
        else:
            summary = bound_summary(summary_raw)
        tags = []
        for t in (fm.get('tags') or []):
            t = str(t).strip()
            if not t or t in DROP_TAGS:
                continue
            if scan(t):
                notes.append("a tag dropped (prohibited content)"); continue
            tags.append(t)
        url = ''
        hp = str(fm.get('homepage') or '').strip()
        if hp:
            u = urlparse(hp)
            if (u.scheme == 'https' and u.hostname and not u.username and not u.query
                    and not u.fragment and u.port is None and u.hostname != 'localhost'
                    and not u.hostname.endswith('.local') and not u.hostname.startswith('127.')):
                url = hp
            else:
                notes.append("url dropped (not a clean public https url)")
        conns = []
        for r in (fm.get('refs') or []):
            try:
                tgt, kind = r.get('target'), r.get('kind')
            except AttributeError:
                continue
            if tgt in all_ids and tgt != pid and str(tgt).startswith('product.'):
                conns.append({"kind": str(kind), "target": str(tgt)})
        item = {"id": str(fm.get('id', '')), "name": str(fm.get('name', '')),
                "kind": str(fm.get('kind', 'product')),
                "status": str(fm.get('status', '')) if fm.get('status') else "",
                "summary": summary, "tags": tags, "url": url, "connections": conns}
        item = {k: v for k, v in item.items() if v not in ('', [], None)}
        items.append(item)
        if notes:
            audit.append(f"- {pid}: " + "; ".join(notes))
    items.sort(key=lambda x: x['id'])
    return items, audit

def validate(items):
    allowed = {'id', 'name', 'kind', 'status', 'summary', 'tags', 'url', 'connections'}
    problems = []
    for i in items:
        extra = set(i) - allowed
        if extra:
            problems.append(f"{i['id']}: non-DTO fields {extra}")
        for field in ('name', 'summary'):
            if i.get(field) and scan(i[field]):
                problems.append(f"{i['id']}: prohibited content in {field}")
        for t in i.get('tags', []):
            if scan(t):
                problems.append(f"{i['id']}: prohibited content in a tag")
    return problems

def main():
    if '--skip-fetch' not in sys.argv:
        fetch()
    items, audit = project()
    problems = validate(items)
    if problems:
        print("VALIDATION FAILED:"); [print(" -", p) for p in problems]; sys.exit(1)
    json.dump({"schema_version": 1, "count": len(items), "items": items},
              open(os.path.join(HERE, "public-products.json"), 'w'), indent=1)
    st = Counter(i.get('status', '(none)') for i in items)
    tagc = Counter(t for i in items for t in i.get('tags', []))
    facet_tags = {t: n for t, n in tagc.most_common() if n >= 3}
    report = ["# Projection audit", "",
              f"Products projected: {len(items)}",
              f"Status counts: {dict(st)}",
              f"With public URL: {sum(1 for i in items if 'url' in i)}",
              f"Without summary: {sum(1 for i in items if 'summary' not in i)}",
              f"Distinct tags (after hygiene): {len(tagc)}",
              f"Facet tags (>=3 products): {len(facet_tags)}", "", "## Notes", ""]
    report += audit if audit else ["No drops."]
    open(os.path.join(HERE, "projection-audit.md"), 'w').write("\n".join(report) + "\n")
    print(f"OK: {len(items)} products | {dict(st)} | urls {sum(1 for i in items if 'url' in i)} | no-summary {sum(1 for i in items if 'summary' not in i)} | distinct tags {len(tagc)} | facet tags {len(facet_tags)}")

if __name__ == '__main__':
    main()
