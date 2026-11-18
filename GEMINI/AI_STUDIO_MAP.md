# خريطة واجهة Google AI Studio

> ملف تشغيلي للوكيل، لا للقارئ العابر. كل سطر هنا **مُختبَر** في 2026-11-18 على حساب صاحب المشروع،
> ما لم يُوسم **[غير مجرّب]**.
> الأداة المرافقة: `GEMINI/studio.py` (Playwright فوق CDP، لا يرسل شيئًا بلا `--yes`).

---

## 0. قاعدة الحدود (قبل أي شيء)

**المرحلة الأولى (الحالية): الوكيل يُجهّز ولا يُرسل.**
يكتب تعليمات النظام، ويضع المرفقات، ويكتب الرسالة في مربع الإدخال — ثم يتوقف. **زر Run لصاحب المشروع.**
المرفقات تُحضَّر في `GEMINI/attachments/` مع `manifest.json`، ويُخبر صاحبَ المشروع بإرفاقها؛ الإرفاق أيضًا من يده.

| ممنوع | لماذا |
|---|---|
| أي عنصر فيه `API key` أو `billing` أو `Upgrade`/`Unlock` | نافذة ترقية/فاتورة. حدثت مرة بالخطأ وأُغلقت. |
| `Get API key` (الشريط الأيسر) | مفتاح/فاتورة |
| `Reset default settings` | يمحو إعدادات الجلسة |
| حفظ/تعديل الـprompt في Gallery أو الأماكن العامة | نشر |
| الضغط على `Run` | قاعدة المرحلة الأولى |

**المسموح:** منطقة المحادثة (مربع النص، الإرفاق، أدواته، Run)، ولوحة الإعدادات اليمنى، وقراءة الصفحة.
أي نقرة خارج هذه الدائرة **تُسمّى لصاحب المشروع قبل تنفيذها**.

---

## 1. الاتصال

```python
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
pages = [pg for c in browser.contexts for pg in c.pages]
pg = next(x for x in pages if "aistudio.google.com" in x.url)
pg.bring_to_front()
```

- كروم يعمل بنافذة مرئية؛ صاحب المشروع يرى المؤشر والكتابة.
- التبويب الصحيح: `https://aistudio.google.com/prompts/new_chat`.
- لا نفتح تبويبات جديدة ولا نغيّر النافذة.

---

## 2. المناطق

| المنطقة | المحتوى | سياستنا |
|---|---|---|
| يسار (0–196px) | Playground, History, New app, My apps, Gallery, Dashboard, Documentation, **Unlock Gemini 4 Carbon**, ما الجديد, Settings, Search, **Get API key**, الحساب | **لا نلمس** إلا `History` عند الحاجة |
| وسط | اقتراحات، مربع `Enter a prompt`، الردود | عملنا |
| يمين (≈780–1030px) | بطاقة النموذج، System instructions، Thinking Level، Tools، Advanced | عملنا |
| طبقة فوقية `.cdk-overlay-container` | الحوارات والقوائم والنوافذ | تُفحص دائمًا قبل/بعد |

---

## 3. العناصر — محدّدات مستقرة

| العنصر | المحدّد | ملاحظة |
|---|---|---|
| مربع الرسالة | `textarea[aria-label="Enter a prompt"]` | |
| إرفاق ملف | `[aria-label="Insert images, videos, audio, or files"]` أو `[data-test-id="add-media-button"]` | `aria-haspopup="menu"` ⇒ يفتح قائمة |
| أدوات الرسالة | `[aria-label="Open tools menu"]` | |
| زر التشغيل | `button.ctrl-enter-submits` (نصّه `Run Ctrl keyboard_return`) | **بلا `aria-label`** — لا تستخدم `[aria-label^=Run]` |
| إجراءات أخرى | `[aria-label="View more actions"]` | |
| تعليمات النظام | `button` باسم `System instructions` | تفتح **popover** |
| حقل تعليمات النظام | `textarea[aria-label="System instructions"]` | يُحفظ في localStorage |
| مستوى التفكير | `combobox` باسم `Thinking Level` | |
| بطاقة النموذج | زر يبدأ اسمه بـ`Gemini 4 Hydrogen` | يفتح «Model selection» |
| إغلاق لوحة الإعدادات | `[aria-label="Close run settings panel"]` / `Close panel` | يوسّع مساحة القراءة |
| فحص الطبقة العلوية | `document.querySelectorAll('.cdk-overlay-container > *').length` | `0` = لا شيء مفتوح |

---

## 4. سلوك مُختبَر

1. **System instructions = popover بخلفية تحجب النقر.** ما دام مفتوحًا، كل نقرة على الصفحة تفشل
   (`cdk-overlay-backdrop ... intercepts pointer events`). **الإصلاح: `Escape`.**
   النص يُحفظ تلقائيًا ("Saved ... local storage")، وزر `delete` يمسحه.
2. **الإرفاق قائمة لا نافذة ملفات:** `Drive · Upload files · Record Audio · Camera · YouTube Video · Sample Media`.
   `Upload files` هو الذي يُطلق نافذة اختيار الملفات (حدث `filechooser` في Playwright).
3. **قائمة الأدوات:** `Structured outputs · Code execution · Function calling · Grounding with Google Search · URL context`.
   كلها مفاتيح تبديل، وتبقى في شريط الرسالة كشرائح (chips).
4. **`View more actions`:** `Share · Compare mode · Temporary chat · Save prompt · Make a copy · Delete · Raw Mode`.
   - `Raw Mode` مفيد لنا: يُظهر النص الخام بلا تنسيق.
   - `Compare mode` يقارن نموذجين على نفس الرسالة.
   - `Temporary chat` لا يُحفظ في السجل.
5. **بطاقة النموذج** تفتح `Model selection`: تصنيفات `All · Featured · Gemini · Live · Images · Video · Audio · Music · Agents · Gemma`.
   الحالي: **`gemini-4-hydrogen`**. و`Gemini 4 Carbon` يحتاج Ultra أو مفتاح API ⇒ **خارج النطاق**.
6. **`Thinking Level`:** `Low · Medium · High · Extra High`.
7. **زر الترقية ملاصق:** `Unlock Gemini 4 Carbon Access to higher quota...` في الشريط الأيسر عند (17,295).
   أي محدّد بحث عن «Gemini 4» سيطابقه أولًا. ⇒ **ثبّت الاسم من بدايته** (`^Gemini 4 Hydrogen`).

---

## 5. إجراءات جاهزة

### أ. فحص صحة
```bash
python3 GEMINI/studio.py state
```
يطبع: الرابط، عدد عناصر الطبقة العلوية، وجود مربع الرسالة، أول سطر من تعليمات النظام، عدد المرفقات.
إن كانت الطبقة العلوية > 0: `python3 GEMINI/studio.py clean`.

### ب. كتابة تعليمات النظام
```bash
python3 GEMINI/studio.py sys-set GEMINI/system_prompt.txt
python3 GEMINI/studio.py sys-show
```
تفتح الـpopover، تملأ، تقرأ للتأكيد، ثم `Escape`.

### ج. إرفاق ملف (بلا إرسال)
```bash
python3 GEMINI/studio.py attach path/to/file.mp3
python3 GEMINI/studio.py attachments
```
يستعمل حدث `filechooser` مباشرة، فلا تظهر نافذة نظام.

### د. كتابة رسالة بلا إرسال
```bash
python3 GEMINI/studio.py draft GEMINI/first_message.txt
```

### هـ. تجهيز جولة كاملة — بلا إرسال
```bash
python3 GEMINI/studio.py prepare \
    --files GEMINI/attachments/round01_a.mp3 \
    --system GEMINI/system_prompt.txt \
    --message GEMINI/rounds/01_blind/message.txt
```
ترتّب: تُنظّف الطبقات العالقة، تكتب تعليمات النظام، ترفق الملفات، تكتب الرسالة، ثم تطبع
حالة نهائية و`READY` — **ولا تضغط Run**. وصاحب المشروع وحده يرسل.

### و. قراءة الرد بعد إرساله هو
```bash
python3 GEMINI/studio.py last
```
**[غير مجرّب]** بنية منطقة الردود لم تُرسم بعد؛ تُحدَّث بعد أول إرسال حقيقي.

---

## 6. مخاطر التشغيل

| الخطر | التخفيف |
|---|---|
| نافذة/طبقة عالقة تحجب النقر | `Escape` ×3 ثم فحص عدد عناصر الطبقة |
| محدّد يطابق زر الترقية | ابدأ الاسم بـ`^` أو استخدم `aria-label` كاملًا |
| إرسال غير مقصود | `send` لا يعمل بلا `--yes`، والمسودة تُكتب منفصلة |
| حصص مجانية/حجب | رسالة واحدة في المرة، فاصل بشري بين الجولات، لا تكرار آلي |
| تلوّث التجربة | لا نصوص ولا أسماء ملفات ولا برومبت في الجولة العمياء |

---

## 7. ما ينتظر الرسم

- بنية منطقة الردود ومحدّداتها.
- هل يُعرض **التفكير** (chain of thought) تلقائيًا، وكيف يُفتح/يُغلق.
- حدود حجم/نوع الملفات الصوتية.
- شكل رسائل الخطأ (حصة، ملف كبير، صيغة غير مدعومة).
- `Compare mode` عمليًا.
