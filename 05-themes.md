# فصل ۵ — تم‌ها: ظاهر سایت، Site Editor و تم فرزند

> 🎯 **هدف:** اکوسیستم تم‌ها رو بشناسی، یک تم نصب و شخصی‌سازی کنی، و مهم‌ترین مفهوم توسعه‌ای: **تم فرزند (Child Theme)**. برای Headless تم کمتر مهمه — ولی فهم تم = فهم قلب وردپرسه، و در پروژه‌های Classic هم نیازت می‌شه.

---

## ۵.۱ — تم: قالب نمایش محتوا

همون محتوا (فصل ۴) با تم‌های مختلف، ظاهرهای کاملاً متفاوت می‌گیره. دو نسل تم:

| نسل | چیه | شخصی‌سازی |
|---|---|---|
| **Classic Themes** | تم‌های PHP سنتی (Twenty Twenty-One...) | Customizer (پنل قدیمی) |
| **Block Themes** ⭐ | تم‌های بلوکی مدرن — کل قالب از بلوک‌ها ساخته شده | **Site Editor** (ادیتور همان گوتنبرگ برای کل سایت!) |

وردپرس 6.9 به سمت Block Themes رفته و تم پیش‌فرض‌های جدید (Twenty Twenty-Five/Six) همگی Block Theme اند.

## ۵.۲ — نصب و تست تم

**Appearance → Themes → Add New** → جستجو/نصب رایگان از مخزن وردپرس → **Activate**.

تم‌های خوب رایگان برای شروع: **Twenty Twenty-Five** (پیش‌فرض)، **Astra**، **GeneratePress** (دوومی سبک و محبوب برای Classic).

بعد از Activate، سایت رو رفرش کن — همین! ظاهر عوض شد، محتوا همونه. (همون جداسازی data/view که تو در React با props/children می‌بینی.)

## ۵.۳ — Site Editor: طراحی با بلوک‌ها

**Appearance → Editor** (در Block Themes): کل سایت قابل ویرایش با بلوک‌ها:

- **Templates:** قالب‌های صفحه (صفحه اصلی، تک‌پست، آرشیو...) — ساختار صفحه
- **Styles:** رنگ‌ها و تایپوگرافی سراسری (مثل design tokens!)
- **Navigation / Header / Footer:** به صورت بخش‌های template part

تمرین: در Styles یک رنگ اصلی و فونت عوض کن → Save → سایت رو ببین.

> 💡 برای تو: Site Editor = «Visual Studio Code برای HTML/CSS» به زبان بلوکی. و Templates دقیقاً همون layout های Next.js ان (`app/(shop)/layout.tsx` فکر کن) — فقط با بلوک.

## ۵.۴ — Customizer (برای تم‌های کلاسیک)

**Appearance → Customize:** پنل شخصی‌سازی تم‌های قدیمی (لوگو، رنگ‌ها، منوها). اگر تم Classic نصب کردی اینو می‌بینی؛ برای Block Themes منسوخه. فقط بدون وجود داره.

## ۵.۵ — منوها (Navigation)

**Appearance → Menus** (یا در Site Editor، بلوک Navigation): منوی بالای سایت رو با صفحات/دسته‌ها بساز. در Headless از API خونده می‌شه (`wp/v2/menu-items` یا GraphQL) — پس اینجا منو رو درست بساز که داده‌اش تمیز باشه.

## ۵.۶ — Child Theme: قانون طلایی توسعه ⭐

**هیچ‌وقت فایل‌های تم اصلی رو مستقیم ویرایش نکن** — با اولین آپدیت تم، همه تغییراتت می‌پره!

راه‌حل: **تم فرزند** — تمی که «از تم مادر ارث می‌بره» و فقط چیزهای تغییریافته رو override می‌کنه:

```
wp-content/themes/
├── twentytwentyfive/        ← تم مادر (دست نمی‌زنیم — آپدیت می‌شود)
└── twentytwentyfive-child/  ← تم فرزند (کد تو)
    ├── style.css            ← هدر اجباری + استایل‌ها
    └── functions.php        ← کدهای PHP تو
```

`style.css` تم فرزند فقط یک هدر کامنت لازم داره:

```css
/*
Theme Name: Twenty Twenty-Five Child
Template: twentytwentyfive     ← ⭐ ارجاع به پوشه تم مادر = رابطه فرزندی
*/
```

فعلاً فقط مفهومش رو بگیر: **تغییرات تو همیشه در لایه‌ای جدا از هسته/تم اصلی** — همون فلسفه‌ای که در کد هم داری (قبل از override کردن library، fork کن!).

> 💡 ساخت سریع با WP-CLI (فصل ۳): `wp scaffold child-theme twentytwentyfive-child --parent=twentytwentyfive`

## ۵.۷ — تم‌های premium و Page Builder ها (آگاهی)

در بازار ایران: تم‌های premium (مثل Enfold، Flatsome) و **Page Builder** ها (Elementor، WPBakery) — ابزارهای درگ‌اند‌دراپ صفحه‌سازی. بدون که:
- Elementor محبوب‌ترینه و بسیاری از پروژه‌های ایرانی باهاش ساخته می‌شن
- ولی برای Headless **به درد نمی‌خورن** (خروجی‌شون HTML تمپلیت است نه داده ساخت‌یافته) — Headless مسیر خودش رو داره: CPT + ACF + API (فصل‌های ۱۰ به بعد)

---

## ✅ جمع‌بندی فصل

- دو نسل تم: Classic (Customizer) و **Block (Site Editor)** — آینده با Block
- Site Editor = ویرایش کل سایت با بلوک (Templates + Styles)
- منوها را تمیز بساز — در Headless از API می‌آیند
- **تم فرزند = لایه تغییرات جدا از تم اصلی** — هرگز فایل تم اصلی را ویرایش نکن
- Page Builder ها (Elementor و...) برای Headless به درد نمی‌خورند

## 📝 تمرین فصل ۵

1. دو تم نصب و فعال کن و فرق ظاهر را ببین؛ بعد Twenty Twenty-Five را برگردان.
2. در Site Editor: رنگ اصلی سایت و فونت را عوض کن و Save — سایت را ببین.
3. منوی بالای سایت را با صفحات فصل ۴ (درباره ما، تماس) و یک دسته‌بندی بساز.
4. با WP-CLI یک تم فرزند بساز و فعالش کن (`wp scaffold child-theme ...` + `wp theme activate ...`) — سایت همچنان کار می‌کند؟
5. (کشف) در Site Editor یک Template را باز کن (مثلاً Single) و ساختار بلوکی‌اش را ببین — این همان «layout» است.

<details><summary>راهنمای تمرین ۴</summary>

```bash
# در Open Site Shell:
wp scaffold child-theme tt5-child --parent=twentytwentyfive
wp theme activate tt5-child
wp theme list --status=active
```
اگر پوشه تم مادر اسم دیگری دارد، `--parent` را با همان نام پوشه بده.
</details>

➡️ **فصل بعد:** صفحه‌سازی عملی — هدر، فوتر، منو، مگامنو و Elementor؛ یک سایت شرکتی کامل می‌سازیم.
