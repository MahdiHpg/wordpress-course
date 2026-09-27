# فصل ۱۴ — WP REST API: وردپرس به عنوان بک‌اند JSON

> 🎯 **هدف:** ورود رسمی به بخش سوم — Headless! وردپرس از قبل یک API کامل REST دارد (`/wp-json`). یاد می‌گیری endpoint ها را با curl صدا بزنی، فیلتر کنی، و با Application Password احراز هویت کنی. این پایه‌ی فهم WPGraphQL هم می‌شود (فصل ۱۵).

---

## ۱۴.۱ — API رایگان که از قبل داری!

هیچ پلاگینی لازم نیست — وردپرس از ۴.۷ به بعد REST API کامل دارد. تستش کن (در مرورگر یا curl):

```bash
$ curl "http://wp-course.local/wp-json" | head -40
# ریشه API: نقشه کل endpoint ها

$ curl "http://wp-course.local/wp-json/wp/v2/posts"
# آرایه JSON همه پست‌هایت! (همان‌هایی که فصل ۴ نوشتی)

$ curl "http://wp-course.local/wp-json/wp/v2/projects"
# CPT پورتفولیوی فصل ۱۰ 🎉
```

الگوی endpoint: `/wp-json/wp/v2/{نوع}`

| endpoint | چه چیزی | نکته |
|---|---|---|
| `/wp/v2/posts` | پست‌ها | فیلترهای قدرتمند می‌گیرد |
| `/wp/v2/pages` | صفحات | |
| `/wp/v2/projects` | CPT تو! | اگر `show_in_rest` بود (فصل ۱۰) |
| `/wp/v2/categories` / `tags` | دسته/برچسب | |
| `/wp/v2/media` | رسانه‌ها (عکس‌ها!) | برای next/image |
| `/wp/v2/users` | کاربران | عمومی فقط عمومی‌ها |
| `/wp/v2/pages?slug=about` | فیلتر | پایین‌تر |

## ۱۴.۲ — آناتومی پاسخ (چه چیزی می‌گیری؟)

بریده‌ای از خروجی یک پست:

```json
{
  "id": 12,
  "date": "2026-09-13T10:00:00",
  "slug": "my-first-post",
  "status": "publish",
  "link": "http://wp-course.local/my-first-post/",
  "title": { "rendered": "عنوان پست" },
  "content": { "rendered": "<p>متن کامل با HTML...</p>" },
  "excerpt": { "rendered": "<p>خلاصه...</p>" },
  "featured_media": 34,
  "categories": [4],
  "_links": { "self": [...], "wp:featuredmedia": [...] }
}
```

نکته‌های دولوپری:

- `slug` = همان کلید routing تو در Next.js (`/blog/[slug]`) ⭐
- `title.rendered` / `content.rendered` = **HTML آماده** (ادیتور بلوکی رندرش کرده) — در Next.js با `dangerouslySetInnerHTML` یا پارسر
- `featured_media` = فقط آی‌دی؛ عکس واقعی یا در `_links` است یا با یک درخواست دیگر (یا در GraphQL — اینجاست که GraphQL می‌درخشه!)
- مقادیر ACF با پلاگین «ACF to REST API» در کلید `acf` می‌آیند (فصل ۱۰ نصب کردی ✅)

## ۱۴.۳ — فیلترها: کوئری‌های واقعی

REST API وردپرس فیلترهای آماده دارد:

```bash
# پست با slug خاص (برای صفحه جزئیات!):
$ curl "http://wp-course.local/wp-json/wp/v2/posts?slug=my-first-post"

# صفحه‌بندی + تعداد:
$ curl ".../wp/v2/posts?per_page=5&page=1"
# نکته: هدر X-WP-Total = کل تعداد (برای pagination!)

# فیلتر دسته، ترتیب، جستجو:
$ curl ".../wp/v2/projects?per_page=12&orderby=date&order=desc&search=react"
```

## ۱۴.۴ — احراز هویت: Application Passwords ⭐

خواندنِ محتوای منتشرشده عمومیه؛ ولی **نوشتن/ویرایش** و دیدن **پیش‌نویس‌ها** نیاز به احراز هویت دارد. راه استاندارد وردپرس مدرن: **Application Password** (رمز جدا برای هر اپ، نه پسورد اصلی):

1. پنل → Users → Profile → پایین صفحه: **Application Passwords** → اسم: `nextjs-headless` → **Add New**
2. یک رمز مثل `xxxx xxxx xxxx xxxx xxxx xxxx` می‌دهد — ⭐ همین یک بار نمایش داده می‌شود؛ ذخیره‌اش کن
3. استفاده با Basic Auth:

```bash
$ curl -u "admin:XXXX XXXX XXXX XXXX XXXX XXXX" \
  "http://wp-course.local/wp-json/wp/v2/posts?status=draft"
# ← حالا پیش‌نویس‌ها را هم می‌بینی!
```

> 🔑 این همان جفت کلید/token دوره‌های قبلیت است: مثل PAT گیت‌هاب — با قابلیت لغو مستقل. در Next.js در `.env` می‌گذاری و هرگز به کلاینت نمی‌روی.

## ۱۴.۵ — نوشتن با API (تست)

```bash
$ curl -X POST -u "admin:XXXX XXXX..." \
  -H "Content-Type: application/json" \
  -d '{"title":"پست از API!","status":"draft"}' \
  "http://wp-course.local/wp-json/wp/v2/posts"
```

برو پنل — پیش‌نویس جدید! (در پروژه‌های Headless معمولاً از این برای فرم‌ها استفاده می‌شود — فصل ۱۷.)

## ۱۴.۶ — محدودیت‌های REST (و چرا GraphQL می‌آیم!)

REST وردپرس خوبه ولی سه دردسر داره:

| مشکل | مثال | نتیجه |
|---|---|---|
| **Over-fetch** | برای لیست کارت‌ها فقط `title` و `featured_media` لازم داری؛ ولی `content` کامل HTML هر پست هم می‌آید | پهنای باند هدر |
| **N+1 برای روابط** | `featured_media` فقط آی‌دی است؛ عکس واقعی = درخواست جدا برای هر پست | ۱۲ پست = ۱۲ درخواست اضافه |
| embedded پیچیده | راه‌حل `_embed` هست ولی خروجی را شلوغ و غیرقابل پیش‌بینی می‌کند | DX پایین |

**GraphQL دقیقاً این سه را حل می‌کند:** هرچی خواستی می‌پرسی (نه بیشتر)، روابط در همان کوئری می‌آیند، شکل پاسخ = شکل کوئری. فصل بعد!

---

## ✅ جمع‌بندی فصل

- `/wp-json/wp/v2/{نوع}` — بدون هیچ نصبی؛ CPT تو با `show_in_rest` آمده
- `slug` = کلید routing؛ `content.rendered` = HTML آماده؛ ACF در `acf`
- فیلترها: `?slug=`, `per_page`, `orderby`, `search`؛ هدر `X-WP-Total`
- نوشتن و پیش‌نویس‌ها = **Application Password** (مثل PAT — در .env)
- دردسرهای REST → دلیل ورود ما به GraphQL

## 📝 تمرین فصل ۱۴

1. سه endpoint را در مرورگر باز کن: posts، pages، projects — JSON هایشان را مقایسه کن.
2. با curl پست `my-first-post` را با فیلتر slug بگیر و `id` و `featured_media` را استخراج کن (با python یا فقط چشم!).
3. هدر `X-WP-Total` را ببین: `curl -sI ".../wp/v2/posts?per_page=5" | grep -i x-wp` — چند پست داری؟
4. Application Password بساز و پیش‌نویس‌ها را با آن ببین؛ بدون رمز چه خطایی می‌گیری؟ (401!)
5. با curl یک پیش‌نویس جدید بساز و در پنل ببینش.
6. فیلدهای `acf` پروژه‌هایت را در خروجی چک کن (پلاگین ACF to REST API فعال باشد).

<details><summary>نکته تمرین ۲</summary>

```bash
curl -s "http://wp-course.local/wp-json/wp/v2/posts?slug=my-first-post" | python -m json.tool
# [ { "id": 12, "featured_media": 34, ... } ] — آرایه با حداکثر یک عضو
```
الگوی مهم: اول با slug آی‌دی بگیر، بعد با آی‌دی کار کن.
</details>

➡️ **فصل بعد:** WPGraphQL — کوئری دقیق، روابط تو در تو، و پایه‌ی پروژه Next.js!
