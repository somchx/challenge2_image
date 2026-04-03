# Media Guide: What Files to Prepare

Place your template images and videos in the folders below.
Run `python run_case.py <id>` to test each case.
Run `python run_all.py` to process all 20 cases and generate results_summary.csv.

---

## Easy Success Cases (e1–e5)

| ID | Template file | Video file | Object | What to do |
|----|--------------|-----------|--------|------------|
| e1 | `templates/easy/template_e1.jpg` | `videos/easy/video_e1.mp4` | Book cover | Photo of textbook front, straight-on. Video: book propped against wall, gentle tilt. |
| e2 | `templates/easy/template_e2.jpg` | `videos/easy/video_e2.mp4` | Printed A4 poster | Photo of poster flat. Video: poster pinned to wall, slow left-right pan. |
| e3 | `templates/easy/template_e3.jpg` | `videos/easy/video_e3.mp4` | Cereal box front | Photo of box front, flat on table. Video: box on table, overhead, static 15s. |
| e4 | `templates/easy/template_e4.jpg` | `videos/easy/video_e4.mp4` | Magazine cover | Photo of magazine front. Video: slow zoom in and out. |
| e5 | `templates/easy/template_e5.jpg` | `videos/easy/video_e5.mp4` | Playing card (face card) | Photo of card straight-on. Video: card on white table, camera approaches/retreats. |

---

## Difficult Success Cases (d1–d5)

| ID | Template file | Video file | Challenge |
|----|--------------|-----------|-----------|
| d1 | `templates/difficult/template_d1.jpg` | `videos/difficult/video_d1.mp4` | Same book as e1, hand covers ~35% of cover in video |
| d2 | `templates/difficult/template_d2.jpg` | `videos/difficult/video_d2.mp4` | Poster under neutral light (template), warm yellow light (video) |
| d3 | `templates/difficult/template_d3.jpg` | `videos/difficult/video_d3.mp4` | Cereal box, camera rotates to 50-60° angle |
| d4 | `templates/difficult/template_d4.jpg` | `videos/difficult/video_d4.mp4` | Textbook held and gently bent (~15-20° flex) |
| d5 | `templates/difficult/template_d5.jpg` | `videos/difficult/video_d5.mp4` | CD/DVD printed label, slight glare from reflection |

---

## Expected Fail Cases (f1–f5)

| ID | Template file | Video file | Why it should fail |
|----|--------------|-----------|-------------------|
| f1 | `templates/expected_fail/template_f1.jpg` | `videos/expected_fail/video_f1.mp4` | Plain white wall — no texture, zero keypoints |
| f2 | `templates/expected_fail/template_f2.jpg` | `videos/expected_fail/video_f2.mp4` | Solid-color t-shirt (no print) — no features |
| f3 | `templates/expected_fail/template_f3.jpg` | `videos/expected_fail/video_f3.mp4` | Blank notebook cover — smooth surface |
| f4 | `templates/expected_fail/template_f4.jpg` | `videos/expected_fail/video_f4.mp4` | Clear glass bottle — transparent, features belong to background |
| f5 | `templates/expected_fail/template_f5.jpg` | `videos/expected_fail/video_f5.mp4` | Uniform carpet patch — no stable keypoints |

---

## Unexpected Fail Cases (u1–u5)

| ID | Template file | Video file | Why it unexpectedly fails |
|----|--------------|-----------|--------------------------|
| u1 | `templates/unexpected_fail/template_u1.jpg` | `videos/unexpected_fail/video_u1.mp4` | Same book as easy case, but wave camera fast → severe motion blur |
| u2 | `templates/unexpected_fail/template_u2.jpg` | `videos/unexpected_fail/video_u2.mp4` | Poster: lights off mid-video (sudden darkness) |
| u3 | `templates/unexpected_fail/template_u3.jpg` | `videos/unexpected_fail/video_u3.mp4` | Template = tiny 80×80px logo crop; video shows full product |
| u4 | `templates/unexpected_fail/template_u4.jpg` | `videos/unexpected_fail/video_u4.mp4` | Brick wall — repetitive texture confuses matcher |
| u5 | `templates/unexpected_fail/template_u5.jpg` | `videos/unexpected_fail/video_u5.mp4` | Phone back / mirror — reflections change with viewpoint |

---

## Tips

- **Template photos**: shoot straight-on with good lighting, minimal background clutter
- **Video length**: 10–20 seconds per case is sufficient (30fps = 300–600 frames)
- **Format**: any common format works (mp4, mov, avi); output will always be mp4
- **Quick test**: `python run_case.py e1 --max-frames 60` processes only 60 frames
- **View live**: `python run_case.py e1 --show` displays detection in real-time window

---

## Parameter reference

Parameters are set per-case in `cases_config.py`. Key ones:

| Parameter | Easy | Difficult | Fail |
|-----------|------|-----------|------|
| `ratio` | 0.75 (standard Lowe) | 0.70 (tighter) | 0.75 |
| `min_matches` | 10 | 8 | 10 |
| `min_inliers` | 8 | 6 | 8 |
| `ransac_thresh` | 5.0 px | 5.0–7.0 px | 5.0 px |
| `use_clahe` | True | True | True |
