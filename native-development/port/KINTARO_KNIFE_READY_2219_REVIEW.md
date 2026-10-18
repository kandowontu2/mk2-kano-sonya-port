# Current native campaign: stance-ready knife controller

Run: `stock_wolf_2219_kano_kintaro_knife_ready`.
Rechecked terminal receipt: exit 0, no timeout. The campaign audit verifies
stock MAME, current ROM chips, frozen controller, and no game-memory writes.
No ROM code, difficulty, damage, health, or AI was changed for this trial.

`inspect_kintaro_knife_ready.py` rechecks the raw request and campaign CSVs.
Its generated `KINTARO_KNIFE_READY_QUALIFICATION.json` binds its inputs by hash.

- 87 physical requests satisfied the logged stance-table, body-height,
  grounded-state, action, health, and distance conditions.
- 79 requests had a sampled native Knife action within 24 fields.
- Eight did not. Their complete sampled 24-field action/HP windows are in
  `missedRequestTraces`; requests alone are never counted as activations.
- Observed Kintaro damage windows: 55 of 11 HP and 13 of 2 HP. This observer
  lacks projectile identity/hitby, so those drops are not individually claimed
  as linked Knife hits.
- Best observed remaining Kintaro HP was 69. No native Kintaro round win or
  match clear was proved. This policy is not a campaign solution.

The next boss experiment must address survival/attack opportunities rather
than repeating this run or treating improved input activation as completion.
This result does not justify modifying native AI, balancing, or hitboxes.

## Normal-move sample review

Both `generated_normal_review_2219/17_sheet.png` and `18_sheet.png` were visually
inspected: 17 normal/proximity move samples per character, in the order recorded
in `SAMPLES.json`. No obvious missing actor artwork or grounding discontinuity
was identified in these samples. These are single contact/throw pose samples,
not all-frame animation or audiovisual approval. The raster image can lag a
native HP/action observation; startup poses at a damage field are not evidence
of a missing later attack pose. Three black padding tiles per sheet are not
captured gameplay frames.
