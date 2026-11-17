# A1 alignment report — hac_align

Model: `akbargherbal/wav2vec2-large-xlsr-53-arabic` @ `4ca1c9c6ac85`
Device: cuda · generated 2026-11-17T05:39:49Z

| song | words | coverage | on/off | intro | cues | warnings | player |
|---|---|---|---|---|---|---|---|
| `hac_01` | 139/139 | 1.00 | 2.02 | ok | 23 line | 2 | [open](hac_01.player.html) |
| `hac_02` | 139/139 | 0.97 | 2.01 | ok | 23 line | 2 | [open](hac_02.player.html) |

## Totals

- 2/2 songs aligned, 278 words
- 0 silent-intro violation(s), 2 song(s) with QA warnings

## Files

`<song>.words.json` is the source of truth; `.vtt`/`.srt` are line-level subtitles; `.player.html` is the karaoke page.
The silent-intro check independently verifies that word 0 waits for the vocal stem (the failure that disqualified MMS-1b in B2).

Subtitles are line-level by design. Word-level timing lives in the JSON and drives the player.
