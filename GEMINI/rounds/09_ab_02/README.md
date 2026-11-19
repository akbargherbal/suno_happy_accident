# الجولة 09 — زوج TRACK_02: البتّ ثم الوسم

**المادة:** `attachments/round09/A.mp3` (= `TRACK_02`، 10/10) · `B.mp3` (= `hat_02_ar75_3337333`، 8/10).
**الأسماء محايدة** · الوسوم مجرّدة · PCM مطابق للأصل ومُتحقَّق.

## المرحلة 1 — نفس سؤال الجولة 07 حرفيًا

- تعليمات النظام: `GEMINI/rounds/07_score_gap/system.txt`
- الرسالة: `GEMINI/rounds/07_score_gap/message.txt`
- **لا تعديل حرف واحد** — ليكون الفرق الوحيد هو المادة.

## المرحلة 2 — سؤال الوسم (بعد أن يختار A)

- تعليمات النظام: `GEMINI/rounds/08_tag_hypothesis/system.txt`
- الرسالة: `GEMINI/rounds/08_tag_hypothesis/message.txt`
- في **نفس المحادثة** (كنمط الجولة 08)، ليُقارن وسْمُه هنا بوسمه هناك.

## خطوات التشغيل

1. `python3 GEMINI/studio.py newchat`
2. `python3 GEMINI/studio.py prepare --system GEMINI/rounds/07_score_gap/system.txt --message GEMINI/rounds/07_score_gap/message.txt --files GEMINI/attachments/round09/A.mp3,GEMINI/attachments/round09/B.mp3`
3. صاحب المشروع يرفع الملفين ويضغط Run.

## بعد الرد

إن اختار **A**: أبدّل تعليمات النظام إلى نسخة 08 وأكتب رسالة الوسم — ثم يضغط Run ثانية.

## ما يُقاس في النهاية

| المخرج | الاستخدام |
|---|---|
| هل تكرر البتّ الصحيح؟ | خاصية أم بذرة (§11.2 بوابة 3) |
| تقاطع الوسمين (01 · 02) | المكوّن الشامل الذي يدخل `PROMPT_DRAFT §26` |
| ما ظهر في واحد فقط | **[بذرة]** — لا يدخل |
