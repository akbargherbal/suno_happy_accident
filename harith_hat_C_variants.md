# harith_hat_C_variants.json — منفست واحد، أربع مداخل

**المصدر:** `harith_hac_C.json` — البرومبت الحالي **ملغى** ولم يدخل أي نسخة.
**البديل:** المسودة الأولى (v1) + سطور التجربة.

| # | الاسم | الأغنية | النسخة | البذور |
|---|---|---|---|---|
| 1 | `hat_01_v1` | hat_01 | V1 — الأصل + المشترك | 1212121 · 1616161 |
| 2 | `hat_01_v2` | hat_01 | V2 — الأصل + HAT 1 | 1212121 · 1616161 |
| 3 | `hat_02_v1` | hat_02 | V1 — الأصل + المشترك | 3331333 · 3337333 |
| 4 | `hat_02_v3` | hat_02 | V3 — الأصل + HAT 2 | 3331333 · 3337333 |

⇒ لكل أغنية نسختان، والبذور **متطابقة** داخل كل زوج ⇒ المقارنة بذرة بذرة، والمتغيّر الوحيد سطر الستايل.

## ما حُذف من البرومبت الحالي

| حُذف | السبب |
|---|---|
| `belting` · `powerful operatic performance` | النبرة تينور عالٍ لا أوبرالي (#51 · #52) |
| `call and response` · `backing vocals` · `rich layered vocal harmonies` · `massive choir` | مغنٍّ واحد، والكورال منفيّ ثلاث مرات (#24 · #54 · #109) |
| `Natural Minor Scale (Aeolian)` | يضادّ `Maqam Nahawand` (§8.3) |
| `audiophile` | صفة بلا فعل |

## ما بقي حرفيًا

`base_dir` · `defaults` · `loras` · `cap` · `lyrics` · `seeds` · `mood` لكل أغنية.

## السطور المتغيّرة

- **V1:** `single dry close-mic lead voice, uncrowded space around the lead, no autotune, no digital artifacts`
- **V2:** `open chest, sustained open cadences, natural vibrato fading at each line's end` · `clear diction, clean phrase openings, single dry lead voice, no autotune, no repeated final word` (بدلًا من `declamatory` · `restrained vibrato` · `crisp consonants`)
- **V3:** `single dry close-mic lead voice, uncrowded space in the full-band sections` · `no autotune, no digital artifacts` · `late drum and electric-guitar entry, the introduction stays quiet`

## عيب مُعلن قبل التشغيل

كلمات `hat_01` فيها `[Chorus | ... with backing harmonies | ...]`، و`hat_02` فيها `[Instrumental | wordless vocal melisma | ...]`.
لم تُمسّ (لتبقى المقارنة نظيفة)، لكنها تناقض `single dry lead voice`.
⇒ إن خرج كورال، فالمصدر سطر الكلمات لا الستايل.
