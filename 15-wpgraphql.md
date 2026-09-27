# فصل ۱۵ — WPGraphQL: کوئری دقیق از وردپرس ⭐

> 🎯 **هدف:** پلاگین WPGraphQL را نصب می‌کنیم تا وردپرس یک سرور GraphQL کامل شود. با GraphiQL کوئری می‌نویسی: لیست پست‌ها با عکس، CPT با فیلدهای ACF، منوها — همه در یک درخواست. این ستون فقرات پروژه Next.js فصل بعد است.

---

## ۱۵.۱ — GraphQL در ۶۰ ثانیه (برای تو که می‌دونی)

```
تو می‌پرسی (شکل دلخواه):          سرور جواب می‌دهد (همان شکل):
{                                  {
  posts {                            "posts": {
    nodes {                            "nodes": [
      title                              { "title": "..." },
      featuredImage { node { sourceUrl } }   { "featuredImage": { ... } }
    }                                    ]
  }                                    }
}                                    }
```

هرچی بخوای می‌گیری، نه بیشتر — و روابط (عکس پست، نویسنده، دسته‌ها) در همان درخواست. دقیقاً سه مشکل REST فصل ۱۴ را حل می‌کند.

## ۱۵.۲ — نصب و GraphiQL

1. Plugins → Add New → **WPGraphQL** → Install → Activate
2. در پنل، منوی جدید **GraphQL → GraphiQL IDE** را باز کن — یک playground آماده (مثل Swagger/Postman برای GraphQL)

اولین کوئری‌ات را بزن:

```graphql
{
  posts(first: 3) {
    nodes {
      id
      slug
      title
      date
    }
  }
}
```

Ctrl+Enter → خروجی JSON با دقیقاً همین شکل. نوار سمت راست GraphiQL، **دوکومنت کامل schema** را نشان می‌دهد (Docs) — مستندات زنده خود وردپرس!

## ۱۵.۳ — کوئری لیست: پست با عکس شاخص در یک درخواست

همان چیزی که در REST به N+1 دردسر افتاد:

```graphql
{
  posts(first: 6) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      slug
      title
      date
      excerpt
      featuredImage {
        node {
          sourceUrl
          altText
          mediaDetails { width height }
        }
      }
      categories {
        nodes { name slug }
      }
    }
  }
}
```

همه‌چیز: پست + عکس + دسته‌ها — **یک درخواست.** (`pageInfo`/`endCursor` برای cursor-based pagination در Next.js — مثل فصل ۹ دوره Prisma!)

## ۱۵.۴ — کوئری تک‌پست (برای صفحه جزئیات)

```graphql
{
  post(id: "my-first-post", idType: SLUG) {
    id
    slug
    title
    date
    content            ← HTML آماده گوتنبرگ
    author {
      node { name }
    }
    featuredImage { node { sourceUrl altText } }
  }
}
```

`idType: SLUG` یعنی با slug جستجو کن — دقیقاً چیزی که از `params` روتر Next.js می‌گیری.

## ۱۵.۵ — CPT تو + فیلدهای ACF در GraphQL ⭐

CPT پروژه (فصل ۱۰) خودکار در schema آمده: `projects`. برای فیلدهای ACF، پلاگین **WPGraphQL for ACF** را نصب/فعال کن (نسخه جدید ACF خودش پشتیبانی دارد — در Field Group هر فیلد «Show in GraphQL» را on کن یا کل گروه را).

کوئری واقعی پروژه‌ها:

```graphql
{
  projects(first: 10) {
    nodes {
      id
      slug
      title
      date
      featuredImage { node { sourceUrl altText } }
      projectFields {            ← گروه فیلدهای ACF تو
        year
        demoUrl
        technologies
        gallery {
          nodes { sourceUrl altText }
        }
      }
      techStack {                ← taxonomy فصل ۱۰
        nodes { name slug }
      }
    }
  }
}
```

این JSON دقیقاً همون shape ای است که در کامپوننت React می‌خواهی — بدون transform!

## ۱۵.۶ — منوها و صفحات

```graphql
{
  menus(where: { location: PRIMARY }) {   # یا: menus(first: 5) { nodes { name ... } }
    nodes {
      name
      menuItems {
        nodes { label url parentId }
      }
    }
  }
  pages(first: 20) {
    nodes { slug title }
  }
}
```

منو و لیست صفحات برای نوار بالای سایت Next.js — در یک درخواست.

## ۱۵.۷ — نکات مهم WPGraphQL

| نکته | چرا |
|---|---|
| پیش‌نویس‌ها با auth | WPGraphQL احراز هویت را با Application Password (فصل ۱۴) هم ساپورت می‌کند — برای Preview فصل ۱۷ |
| `first: N` به جای per_page | cursor-based؛ برای صفحه‌های بی‌نهایت عالی |
| caching | WPGraphQL با پلاگین‌های کش (مثل WPGraphQL Smart Cache) بهتر می‌شود — برای production |
| secure endpoint | endpoint شما `http://wp-course.local/graphql` است — همان را Next.js صدا می‌زند |

---

## ✅ جمع‌بندی فصل

- **WPGraphQL** = سرور GraphQL روی وردپرس؛ GraphiQL = playground + مستندات زنده
- لیست با عکس و دسته در یک کوئری؛ تک‌پست با `idType: SLUG`
- CPT تو = root field (`projects`)؛ ACF بعد از فعال‌سازی GraphQL برای ACF در گروه `projectFields`
- منوها و صفحات هم در schema — کل داده سایت در یک API مدرن

## 📝 تمرین فصل ۱۵ (خروجی هر کوئری = مصرف مستقیم در فصل ۱۶!)

1. WPGraphQL را نصب/فعال کن و اولین کوئری posts را در GraphiQL بزن.
2. کوئری لیست با featuredImage را اجرا کن — sourceUrl عکس‌ها را ببین.
3. کوئری تک‌پست با SLUG را برای `my-first-post` بزن.
4. WPGraphQL for ACF را فعال کن و کوئری `projects` با `projectFields` را بزن — سال و تکنولوژی‌های پروژه‌هات را ببین! (اگر گروه فیلدها نیامد: در ویرایش Field Group، تب GraphQL → Show in GraphQL را on کن.)
5. کوئری منوها را بزن؛ اگر منو خالی بود، در پنل منو را بساز و **Location** اش را Primary کن.
6. (کشف) در GraphiQL، پنل Docs را باز کن و root فیلد `mediaItems` را پیدا کن — همه عکس‌های سایت در یک لیست!

<details><summary>نکته تمرین ۴</summary>

مسیرهای رایج: (الف) ACF نسخه 6+: Field Group → Settings → GraphQL → Enable؛ (ب) یا پلاگین «WPGraphQL for ACF». بعد از فعال‌سازی، در GraphiQL با Ctrl+Space داخل `projects { ... }` autocomplete فیلدها را می‌بینی — اگر `projectFields` نیامد، schema را رفرش کن (رفرش صفحه).
</details>

➡️ **فصل بعد:** 🚀 لحظه بزرگ — اتصال Next.js به همین API و ساخت سایت واقعی!
