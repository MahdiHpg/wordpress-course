# -*- coding: utf-8 -*-
"""Build a single RTL Persian PDF-ready HTML from the WordPress course markdown files."""
import re, pathlib, markdown
from pygments.formatters import HtmlFormatter

BASE = pathlib.Path(__file__).resolve().parent.parent
BUILD = BASE / "build"

CHAPTERS = [
    ("README.md", "شروع دوره — نقشه ۴ بخشی"),
    ("01-what-is-wp.md", "فصل ۱ — وردپرس چیست"),
    ("02-web-infra.md", "فصل ۲ — زیرساخت وب: دامنه، هاست، DNS، SSL"),
    ("03-install-local.md", "فصل ۳ — نصب لوکال با Local"),
    ("04-dashboard-content.md", "فصل ۴ — داشبورد و محتوا"),
    ("05-themes.md", "فصل ۵ — تم‌ها و Site Editor"),
    ("06-page-building.md", "فصل ۶ — صفحه‌سازی عملی و Elementor"),
    ("07-plugins.md", "فصل ۷ — پلاگین‌ها"),
    ("08-seo.md", "فصل ۸ — سئو عملی"),
    ("09-users-settings.md", "فصل ۹ — کاربران و تنظیمات"),
    ("10-cpt-acf.md", "فصل ۱۰ — CPT و ACF ⭐"),
    ("11-php-dev-basics.md", "فصل ۱۱ — PHP برای دولوپر JS"),
    ("12-woocommerce.md", "فصل ۱۲ — 🛒 ووکامرس"),
    ("13-security-maintenance.md", "فصل ۱۳ — امنیت، بکاپ و نگهداری"),
    ("14-rest-api.md", "فصل ۱۴ — WP REST API"),
    ("15-wpgraphql.md", "فصل ۱۵ — WPGraphQL ⭐"),
    ("16-nextjs-headless.md", "فصل ۱۶ — 🚀 Next.js + وردپرس"),
    ("17-headless-advanced.md", "فصل ۱۷ — Headless پیشرفته"),
    ("18-go-live-iran.md", "فصل ۱۸ — مهاجرت به هاست و ایران‌سازی"),
    ("19-freelancing.md", "فصل ۱۹ — فریلنسری و درآمد"),
    ("20-cheatsheet.md", "فصل ۲۰ — چیت‌شیت و گلاساری"),
]

ANCHOR = {fn: f"ch{i:02d}" for i, (fn, _) in enumerate(CHAPTERS)}
LINK_RE = re.compile(r"\]\((\.?/?)([\w\-]+\.md)([#\w\-]*)\)")

MD_EXT = ["tables", "fenced_code", "codehilite", "md_in_html", "attr_list", "sane_lists"]
MD_CFG = {"codehilite": {"guess_lang": False}}


def preprocess(text: str) -> str:
    def repl(m):
        target, frag = m.group(2), m.group(3) or ""
        if target in ANCHOR:
            return f"](#{ANCHOR[target]}{frag})"
        return m.group(0)
    text = LINK_RE.sub(repl, text)
    text = re.sub(r"```mermaid\n(.*?)```", lambda m: f'<div class="mermaid">\n{m.group(1)}</div>', text, flags=re.S)
    text = text.replace("<details>", '<details markdown="1" open>')
    text = text.replace("<summary>", '<summary markdown="span">')
    return text


def render_chapter(fn: str, idx: int) -> str:
    raw = (BASE / fn).read_text(encoding="utf-8")
    body = markdown.markdown(preprocess(raw), extensions=MD_EXT, extension_configs=MD_CFG)
    return f'<section class="chapter" id="ch{idx:02d}">{body}</section>'


CSS = """
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Regular.ttf') format('truetype'); font-weight:400; }
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Medium.ttf') format('truetype'); font-weight:500; }
@font-face { font-family:'Vazirmatn'; src:url('fonts/Vazirmatn-Bold.ttf') format('truetype'); font-weight:700; }
@font-face { font-family:'JetBrains Mono'; src:url('fonts/JetBrainsMono-Regular.ttf') format('truetype'); font-weight:400; }
@font-face { font-family:'JetBrains Mono'; src:url('fonts/JetBrainsMono-Bold.ttf') format('truetype'); font-weight:700; }

@page { size: A4; margin: 16mm 13mm 18mm 13mm; }

:root {
  --ink:#1a1f2e; --muted:#5c6478; --line:#e3e7ef;
  --primary:#1d5c8f; --primary-soft:#eef5fb;
  --accent:#7f54b3; --accent-soft:#f6f2fb;
  --green:#059669; --green-soft:#ecfdf5;
  --amber:#b45309; --amber-soft:#fffbeb;
  --rose:#be123c; --rose-soft:#fff1f2;
  --code-bg:#152238; --code-ink:#e2e8f0;
}
* { box-sizing:border-box; }
html { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body {
  direction:rtl; text-align:right;
  font-family:'Vazirmatn', Tahoma, sans-serif;
  color:var(--ink); font-size:11.2pt; line-height:2;
  margin:0; padding:0;
}

/* cover */
.cover {
  page-break-after:always; height:250mm;
  display:flex; flex-direction:column; justify-content:center; align-items:center;
  text-align:center; color:#fff; border-radius:14px; padding:20mm;
  background:linear-gradient(135deg,#10233f 0%,#1d5c8f 50%,#7f54b3 100%);
}
.cover .badge { background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.35);
  padding:4px 18px; border-radius:999px; font-size:10pt; letter-spacing:.3px; }
.cover h1 { font-size:30pt; line-height:1.6; margin:14px 0 6px; border:none; color:#fff; background:none; }
.cover h2 { font-size:14pt; font-weight:500; color:#dbeafe; border:none; margin:0; }
.cover .stack { display:flex; gap:10px; margin-top:26px; flex-wrap:wrap; justify-content:center; }
.cover .stack span { background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.3);
  border-radius:10px; padding:6px 16px; font-size:10.5pt; }
.cover .foot { margin-top:40px; font-size:9.5pt; opacity:.85; }

/* toc */
.toc { page-break-after:always; }
.toc h1 { border:none; }
.toc ol { list-style:none; padding:0; counter-reset:toc; }
.toc li { counter-increment:toc; border-bottom:1px dashed var(--line);
  padding:9px 2px; display:flex; justify-content:space-between; align-items:baseline;
  page-break-inside:avoid; break-inside:avoid; }
.toc a { text-decoration:none; color:var(--ink); font-weight:500; }
.toc li::before { content:counter(toc); background:var(--primary-soft); color:var(--primary);
  font-weight:700; border-radius:8px; width:30px; height:30px; display:inline-flex;
  align-items:center; justify-content:center; margin-left:14px; flex:none; }
.toc li .desc { color:var(--muted); font-size:9.5pt; }

/* chapters / headings */
.chapter { page-break-before:always; }
h1 {
  font-size:19pt; color:#fff; background:linear-gradient(90deg,#1d5c8f,#2271b1);
  padding:14px 22px; border-radius:12px; line-height:1.7;
  margin:0 0 18px; page-break-after:avoid;
}
h2 {
  color:var(--primary); font-size:14.5pt; margin:26px 0 10px;
  padding-right:12px; border-right:4px solid var(--primary); line-height:1.8;
  page-break-after:avoid;
}
h3 { color:var(--accent); font-size:12.5pt; margin:20px 0 8px; page-break-after:avoid; }
p { margin:8px 0; }
strong { color:#123055; }
a { color:var(--primary); text-decoration:none; }

/* lists */
ul, ol { padding-right:1.6em; padding-left:0; margin:8px 0; }
li { margin:3px 0; }
li::marker { color:var(--primary); font-weight:700; }
input[type="checkbox"] { accent-color:var(--primary); }

/* tables */
table { border-collapse:collapse; width:100%; margin:12px 0; font-size:10pt;
  border-radius:10px; overflow:hidden; page-break-inside:avoid; }
th { background:linear-gradient(90deg,#1d5c8f,#2271b1); color:#fff; font-weight:700; }
th, td { border:1px solid #d5dfea; padding:6px 10px; text-align:right; vertical-align:top; }
tbody tr:nth-child(even) { background:#f7fafd; }

/* code */
pre, code, kbd { font-family:'JetBrains Mono','Vazirmatn',Consolas,monospace; direction:ltr; }
code { background:#eef5fb; color:#1d5c8f; padding:1px 6px; border-radius:5px;
  font-size:8.8pt; unicode-bidi:embed; }
pre { background:var(--code-bg); color:var(--code-ink); direction:ltr; text-align:left;
  padding:13px 16px; border-radius:12px; overflow-x:hidden; font-size:8.6pt;
  line-height:1.65; margin:10px 0; border:1px solid #1e3a5f; page-break-inside:avoid; }
pre code { background:none; color:inherit; padding:0; font-size:inherit; }
.codehilite { background:var(--code-bg); border-radius:12px; margin:10px 0; page-break-inside:avoid; }
.codehilite pre { margin:0; border:none; }
.codehilite .k,.codehilite .kd,.codehilite .kn,.codehilite .ow { color:#93c5fd; }
.codehilite .s,.codehilite .s1,.codehilite .s2,.codehilite .sd { color:#a7f3d0; }
.codehilite .n,.codehilite .na,.codehilite .nx { color:#e2e8f0; }
.codehilite .nf { color:#fbbf24; }
.codehilite .mi,.codehilite .mf { color:#fda4af; }
.codehilite .o,.codehilite .p { color:#94a3b8; }
.codehilite .nb,.codehilite .nv { color:#7dd3fc; }
.codehilite .cp { color:#93c5fd !important; font-style:italic; }
.codehilite .err { color:#e2e8f0; background:none; border:none; }
.codehilite .c,.codehilite .c1,.codehilite .cm { color:#7dd3fc !important; font-style:italic; }
.codehilite .nt { color:#f0abfc; }
.codehilite .nd { color:#fbbf24; }
.codehilite .php .keyword { color:#93c5fd; }

/* blockquotes */
blockquote {
  margin:12px 0; padding:10px 16px; border-radius:12px;
  border-right:5px solid var(--primary); background:var(--primary-soft);
  page-break-inside:avoid;
}
blockquote p { margin:4px 0; }
blockquote p:first-child { font-weight:500; }
blockquote:has(> p:first-child strong:contains("⚠")) { background:var(--amber-soft); border-right-color:var(--amber); }
blockquote:has(> p:first-child strong:contains("🚨")) { background:var(--rose-soft); border-right-color:var(--rose); }
blockquote:has(> p:first-child strong:contains("💡")) { background:var(--green-soft); border-right-color:var(--green); }
blockquote:has(> p:first-child strong:contains("🔑")) { background:var(--green-soft); border-right-color:var(--green); }
blockquote:has(> p:first-child strong:contains("🎯")) { background:var(--primary-soft); border-right-color:var(--primary); }
blockquote:has(> p:first-child strong:contains("⭐")) { background:var(--accent-soft); border-right-color:var(--accent); }
blockquote:has(> p:first-child strong:contains("🚀")) { background:var(--primary-soft); border-right-color:var(--primary); }

/* hr, details */
hr { border:none; border-top:2px dashed var(--line); margin:22px 0; }
details { background:#f7fafd; border:1px solid var(--line); border-radius:10px;
  padding:8px 14px; margin:10px 0; page-break-inside:avoid; }
summary { cursor:pointer; font-weight:700; color:var(--green); }

/* mermaid */
.mermaid {
  background:#fff; border:1px solid var(--line); border-radius:12px;
  padding:10px; margin:12px 0; text-align:center; page-break-inside:avoid;
  display:flex; justify-content:center;
}
.mermaid svg { max-width:100%; height:auto; }

del { color:var(--muted); }
em { color:#243b5e; }
"""

PYGMENTS_CSS = HtmlFormatter(style="default").get_style_defs(".codehilite")

COVER = """
<section class="cover">
  <div class="badge">آموزش صفر تا صد — نسخه ۲۰۲۶</div>
  <h1>WordPress<br/>صفر تا سایت واقعی و Headless با Next.js</h1>
  <h2>وردپرس کامل: فروشگاه، مهاجرت، ایران‌سازی — و به عنوان بک‌اند؛ Next.js به عنوان فرانت تو</h2>
  <div class="stack">
    <span>WordPress 6.9</span><span>Elementor</span><span>SEO</span>
    <span>WooCommerce</span><span>CPT + ACF</span><span>REST API</span>
    <span>WPGraphQL</span><span>Next.js App Router</span><span>Deploy Vercel</span>
  </div>
  <div class="foot">۲۰ فصل در ۴ بخش · پروژه: سایت شرکتی + فروشگاه + Headless · تمرین با جواب · چیت‌شیت و گلاساری</div>
</section>
"""

DESCS = {
    "README.md": "نقشه دوره و مسیر چهار بخشی",
    "01-what-is-wp.md": "CMS، معماری، اکوسیستم، Headless چیست",
    "02-web-infra.md": "دامنه، ایرنیک، DNS، هاست، سی‌پنل، SSL",
    "03-install-local.md": "برنامه Local، اولین سایت، WP-CLI",
    "04-dashboard-content.md": "پست/صفحه، بلوک‌ها، رسانه",
    "05-themes.md": "Block Themes، Site Editor، تم فرزند",
    "06-page-building.md": "هدر/فوتر، منو/مگامنو، اسلایدر، Elementor",
    "07-plugins.md": "نصب، ضروری‌ها، امنیت، Yoast",
    "08-seo.md": "Yoast/Rank Math، sitemap، سرچ کنسول، نشان/بلد",
    "09-users-settings.md": "نقش‌ها، Permalinks، تنظیمات",
    "10-cpt-acf.md": "Custom Post Type + ACF — پایه Headless",
    "11-php-dev-basics.md": "PHP سریع، The Loop، Hooks، اولین پلاگین",
    "12-woocommerce.md": "محصولات، سبد، ارسال، درگاه ایرانی، WooGraphQL",
    "13-security-maintenance.md": "Wordfence، بکاپ ۳-۲-۱، بازیابی، کش، SMTP",
    "14-rest-api.md": "endpoint ها، فیلترها، Application Password",
    "15-wpgraphql.md": "GraphiQL، کوئری‌های دقیق، ACF در GraphQL",
    "16-nextjs-headless.md": "لیست، [slug]، ISR، پروژه CPT",
    "17-headless-advanced.md": "Preview، فرم‌ها، SEO، Vercel",
    "18-go-live-iran.md": "خرید هاست، مهاجرت، انماد، درگاه، SMS",
    "19-freelancing.md": "سه بسته خدماتی، قیمت‌گذاری، قرارداد",
    "20-cheatsheet.md": "مرور سریع + گیرهای کلاسیک",
}


def build_toc() -> str:
    items = []
    for i, (fn, title) in enumerate(CHAPTERS):
        items.append(f'<li><a href="#ch{i:02d}">{title}</a><span class="desc">{DESCS.get(fn, "")}</span></li>')
    return f'<section class="toc"><h1>فهرست مطالب</h1><ol>{"".join(items)}</ol></section>'


def main():
    parts = [COVER, build_toc()]
    for i, (fn, _) in enumerate(CHAPTERS):
        parts.append(render_chapter(fn, i))
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8"/>
<title>دوره WordPress + Headless</title>
<style>{CSS}
{PYGMENTS_CSS}
</style></head>
<body>{''.join(parts)}
<script src="mermaid.min.js"></script>
<script>mermaid.initialize({{ startOnLoad:true, theme:'base',
  themeVariables: {{ fontFamily:'Vazirmatn, Tahoma', fontSize:'13px',
    primaryColor:'#eef5fb', primaryBorderColor:'#1d5c8f', primaryTextColor:'#1a1f2e',
    lineColor:'#64748b', secondaryColor:'#f6f2fb', tertiaryColor:'#f7fafd' }},
  flowchart: {{ htmlLabels:true, curve:'basis' }} }});</script>
</body></html>"""
    out = BUILD / "course.html"
    out.write_text(html, encoding="utf-8")
    print(f"OK -> {out}  ({len(html)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
