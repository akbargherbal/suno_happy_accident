# مسودة برومبت — بناءً على 5 جولات · 2026-11-19

> **ليست وصفة.** كل سطر موسوم بمصدره. الوسم يعني: من أين جاء، لا كم هو جميل.
> **[مقيس]** رقم من ملفاتنا · **[مسموع]** أذن صاحب المشروع · **[واصف]** قاله جيمناي (وحده لا يكفي) · **[تخمين]** لا دليل، ويُحذف أولًا عند الاختبار.
>
> **وقاعدة ضد الـoverfitting:** كل بند إما **قاعدة** تُكتب على **الموضع** (تنطبق على أي نص)، أو **معامل** يحمل **قيمة هذه القطعة** ويُمرَّر متغيرًا. لا يُكتب مثال لغوي داخل قاعدة: «البكاء→البكاءُو» مثال، لا قاعدة.

---

## أ) الصوت

| Tag | المصدر |
|---|---|
| `male high tenor, deep chest resonance, wide breath support` | [مسموع] + [مقيس]: وسيط D5، 82% ≥ C5 |
| `no shouting, no rock grit, no rasp` | [مسموع]: «ليس صراخ الروك» |
| `clear consonant articulation, syllables separated, no slurring` | [مسموع]: «تاء ساكنة ثم نون مفتوحة، القطع سهل» |
| `melismatic delivery; long madda on the rhyme` | [مقيس] + [مسموع] |
| **قاعدة:** `on every line ending, sustain the final syllable and resolve its short vowel into its long counterpart (dammeh→waw, fatha→alif, kasra→ya) — ishba'/wasl` | [مقيس] + [مسموع] + `CHECKPOINT §5.1` |
| **معامل هذه القصيدة فقط:** `rowi = hamza with damma → waw` | [مسموع] — يُمرَّر كقيمة، لا يُكتب داخل القاعدة |
| `solo voice, no harmonies, no doubling` | [مسموع]: مغنٍّ واحد؛ والجولة 04 ادّعت صوتًا ثانيًا فسقط |
| `no audible inhalation` | [مسموع] |
| `vocal-forward mix; voice above the band, not inside it` | [مسموع] + [مقيس]: الجهارة متساوية (‑11.5) ومع ذلك يُسمع الأخفّ صوتًا |

## ب) الأداء

| Tag | المصدر |
|---|---|
| `slow declamation: about 2 seconds per word in slow lines` | [مقيس] — **معامل**: يتبع وزن النص؛ القاعدة أن يكون أبطأ من نبض الفرقة |
| `do not rush the verse body and compensate on the rhyme` | [مقيس] + [مسموع]: B يمرّ ثم يمدّ القافية |
| `rising arc: quiet entry → building intensity → peak on the final couplet` | [واصف] + [مقيس]: منحنى الطاقة |
| `recited, tartil-like gravity` | [مسموع] — تشبيه المالك. [تخمين] كـtag |

## ج) الإنتاج — أضعف طبقة عندنا

| Tag | المصدر |
|---|---|
| `large hall reverb` | [تخمين] — لم تُفكَّك بعد |
| `smooth vocal delay` | [تخمين] |
| `sparse, guitar-led intro; band fills in later` | [مقيس]: تسطّح طيفي منخفض في أول 22 ثانية |

## د) الأسلوب والإيقاع — **كلها معاملات هذه القطعة، لا قواعد**

| Tag | المصدر |
|---|---|
| `87 bpm` | [مقيس] — **لا 110**. معامل: سرعة هذه القطعة |
| `C minor (Nahawand on C)` | [مقيس] كمفتاح غربي؛ المقام نفسه [مفتوح]. معامل |
| `distorted electric guitar enters after the intro, not at bar one` | [مقيس] + [مسموع]. **قاعدة**: لا تبدأ بالفرقة كاملة |

## هـ) ما يُحذف من البرومبتات السابقة (له دليل)

| يُحذف | لماذا |
|---|---|
| `male baritone vocals` | متناقض مع D5 وأذنه: **تينور عالٍ** |
| `backing harmonies` في اللازمة | مغنٍّ واحد؛ والوسم أنتج ادعاء كورال في المحاولة |
| `110 bpm` | الناتج 87.0 |
| مدد مكتوبة مثل `[Instrumental Intro - 15 seconds]` | Suno لا يحترمها: المقدمة 22.2s |
| `and more` / قوائم الصفات الطويلة | لا تُقاس، ولا تُميَّز عن غيرها |

---

## الحدّ الذي يجب أن يُقرأ مع المسودة

**[مؤكد من تجاربنا]** وسوم النص هي **أضعف قناة**، وحدها لا تكفي:
- طُلب الإشباع بثلاث صيغ (واو · نقط · LoRA) ولم يُنفَّذ.
- السكور المُمرَّر للتوليد لا يحمل المدّ أصلًا (أطول نغمة 0.35s في موضع «البكاء»).

⇒ هذه المسودة تصف **ما يجب أن يُسمع**، ولا تضمن أن يُنفَّذ. والطبقة الحاكمة عندنا اليوم: **السكور** (§16).

**الترتيب المقترح عند الاختبار:** ابدأ بالصوت والأداء (أ، ب) لأن كل بنده مسموع أو مقيس؛ ثم احذف (ج) كاملًا لتعرف أثره؛ ولا تُعد إلى (د) قبل حسم السكور.

---

## و) السطر الجاهز (نسخة واحدة)

**النواة — كل بند فيها مقيس أو مسموع:**

```
male high tenor, deep chest resonance, wide breath support, clear consonant
articulation, syllables separated, no slurring, no shouting, no rock grit,
melismatic, long madda on every line ending, rhyme's final vowel resolved into
its long counterpart (damma to waw, fatha to alif, kasra to ya), solo voice,
no harmonies, no audible inhalation, vocal-forward mix, voice above the band,
slow declamation, no rushing the verse then compensating on the rhyme,
rising arc from quiet entry to peak on the final couplet, sparse guitar-led
intro, band enters after the intro, 87 bpm, C minor
```

**الملحق — [تخمين] يُضاف أو يُحذف كاملًا:**

```
large hall reverb, smooth vocal delay, recited gravity
```

**ترتيب الأولوية إن قُصر السطر:** [قواعد الأداء] ← [الصوت] ← [المزيج] ← [المعاملات] ← [الإنتاج].
