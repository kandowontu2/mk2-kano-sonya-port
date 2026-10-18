# Current stage recording review

The first stage video batch completed, but its two `stock_wolf_2219_stage_video_pit_*`
MP4s are NOT Pit demonstrations. Gameplay qualification reached Pit II normally;
the independent video capture started earlier on Kombat Tomb (background1).
For example Kano's clip starts7657 and lasts124 fields, whereas the actual
Pit fall starts20531, with206 native cinematic fields including148 launch-to-fall.
The old STAGE_VIDEOS_2219.json therefore does not prove six correct stage clips.
Original traces, clips and receipts remain intact as failed capture evidence.

The coordinator now selects background0/1/6 for Dead Pool/Tomb/Pit, checks every
captured field against stage_environment.csv, and checks the Pit interval exactly
against its linked cinematic timing plus60 completion fields before encoding.
The filtered two-case retry uses fresh `stock_wolf_2219_pit_video_filtered_*`
directories. No native ROM/controller gameplay changes were required.

Filtered retry is now terminal exit0. Both clips have266 fields, exactly
206 linked cinematic fields plus60 completion fields, correct background6
throughout, full decode and native rejoin qualification. PIT_VIDEOS_2219.json
indexes the correct clips. Both sampled decoded sheets were viewed through
launch, scrolling fall, own victim impact and winner text. All four earlier
Dead Pool/Tomb captures also passed the added arena check. Full-video visual
and exact audio-sync acceptance remain separate.

Both Dead Pool sample sheets show uppercut, own victim launch/fall, acid splash
and own winner pose. Both Tomb sheets show uppercut and own victim impalement.
These four sampled reviews are not all-frame/audio-sync acceptance. Black unused
contact-sheet tiles are layout padding, not captured in-game frames.
