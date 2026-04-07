# Image Feature Matching — ผลการทดสอบ

ระบบตรวจจับวัตถุโดยใช้ Feature Matching (ORB + BFMatcher) เปรียบเทียบ template ภาพนิ่งกับวิดีโอ  
แต่ละ case แสดง: ภาพ frame ที่ตรวจจับได้ + GIF แสดง bounding polygon ขณะวัตถุเคลื่อนไหว

---

## Easy Success Cases (e1–e5)

วัตถุที่มี texture ชัดเจน แสงดี มุมตรง — คาดว่าตรวจจับได้ทุก frame

### e1 — Notebook cover

| Output frame | Output GIF |
|---|---|
| ![e1 detected](outputs/easy/output_e1.png) | ![e1 gif](outputs/easy/output_e1.gif) |

**Template:** `templates/easy/template_e1.jpg`  
**Video:** `videos/easy/video_e1.mp4`  
สมุดโน้ตถือในมือ ระบบตรวจจับปกและวาด bounding polygon ครอบวัตถุได้ถูกต้อง

---

### e2 — Airplane in sky

| Output frame | Output GIF |
|---|---|
| ![e2 detected](outputs/easy/output_e2.png) | ![e2 gif](outputs/easy/output_e2.gif) |

**Template:** `templates/easy/template_e2.jpg`  
**Video:** `videos/easy/video_e2.mp4`  
เครื่องบินกำลังบินอยู่บนท้องฟ้า ระบบตรวจจับและ track ตัวเครื่องบินได้ขณะเคลื่อนที่

---

### e3 — Cereal box front

| Output frame | Output GIF |
|---|---|
| ![e3 detected](outputs/easy/output_e3.png) | ![e3 gif](outputs/easy/output_e3.gif) |

**Template:** `templates/easy/template_e3.jpg`  
**Video:** `videos/easy/video_e3.mp4`  
กล่องซีเรียลบนโต๊ะ กล้องมองจากบนลงล่าง นิ่ง 15 วินาที

---

### e4 — Magazine cover

| Output frame | Output GIF |
|---|---|
| ![e4 detected](outputs/easy/output_e4.png) | ![e4 gif](outputs/easy/output_e4.gif) |

**Template:** `templates/easy/template_e4.jpg`  
**Video:** `videos/easy/video_e4.mp4`  
นิตยสาร zoom เข้า-ออกช้าๆ

---

### e5 — Playing card (face card)

| Output frame | Output GIF |
|---|---|
| ![e5 detected](outputs/easy/output_e5.png) | ![e5 gif](outputs/easy/output_e5.gif) |

**Template:** `templates/easy/template_e5.jpg`  
**Video:** `videos/easy/video_e5.mp4`  
ไพ่บนโต๊ะขาว กล้องเคลื่อนเข้า-ถอยออก

---

## Difficult Success Cases (d1–d5)

มีปัจจัยรบกวน แต่ระบบยังตรวจจับได้ผ่าน threshold ที่ปรับแล้ว

### d1 — Book cover (partial occlusion)

| Output frame | Output GIF |
|---|---|
| ![d1 detected](outputs/difficult/output_d1.png) | ![d1 gif](outputs/difficult/output_d1.gif) |

**Template:** `templates/difficult/template_d1.jpg`  
**Video:** `videos/difficult/video_d1.mp4`  
หนังสือเล่มเดิมกับ e1 แต่มือบัง ~35% ของปก

---

### d2 — Poster (lighting change)

| Output frame | Output GIF |
|---|---|
| ![d2 detected](outputs/difficult/output_d2.png) | ![d2 gif](outputs/difficult/output_d2.gif) |

**Template:** `templates/difficult/template_d2.jpg`  
**Video:** `videos/difficult/video_d2.mp4`  
Template ถ่ายแสงขาว, video ถ่ายแสงเหลืองอุ่น

---

### d3 — Cereal box (angled view)

| Output frame | Output GIF |
|---|---|
| ![d3 detected](outputs/difficult/output_d3.png) | ![d3 gif](outputs/difficult/output_d3.gif) |

**Template:** `templates/difficult/template_d3.jpg`  
**Video:** `videos/difficult/video_d3.mp4`  
กล้อง rotate ทำมุม 50–60° กับหน้ากล่อง

---

### d4 — Textbook (slight bend)

| Output frame | Output GIF |
|---|---|
| ![d4 detected](outputs/difficult/output_d4.png) | ![d4 gif](outputs/difficult/output_d4.gif) |

**Template:** `templates/difficult/template_d4.jpg`  
**Video:** `videos/difficult/video_d4.mp4`  
หนังสือถูกจับและงอเล็กน้อย ~15–20°

---

### d5 — CD/DVD label (glare)

| Output frame | Output GIF |
|---|---|
| ![d5 detected](outputs/difficult/output_d5.png) | ![d5 gif](outputs/difficult/output_d5.gif) |

**Template:** `templates/difficult/template_d5.jpg`  
**Video:** `videos/difficult/video_d5.mp4`  
Label ซีดีพิมพ์ มีแสงสะท้อนเล็กน้อย

---

## Expected Fail Cases (f1–f5)

วัตถุที่ไม่มี texture / keypoint เพียงพอ — ระบบควร fail ตามที่คาดไว้

### f1 — Scotch book on wooden table

| Output frame | Output GIF |
|---|---|
| ![f1 detected](outputs/expected_fail/output_f1.png) | ![f1 gif](outputs/expected_fail/output_f1.gif) |

**ผลที่คาดหวัง:** หนังสือสกอตวางบนโต๊ะไม้ ปกเรียบไม่มี texture เพียงพอ → ระบบไม่สามารถหา keypoint ได้ → ไม่ detect

---

### f2 — Moving car on road

| Output frame | Output GIF |
|---|---|
| ![f2 detected](outputs/expected_fail/output_f2.png) | ![f2 gif](outputs/expected_fail/output_f2.gif) |

**ผลที่คาดหวัง:** รถเคลื่อนที่บนท้องถนน วัตถุเปลี่ยน viewpoint และมี motion blur → feature ไม่ stable → ไม่ detect

---

### f3 — Blank notebook cover

| Output frame | Output GIF |
|---|---|
| ![f3 detected](outputs/expected_fail/output_f3.png) | ![f3 gif](outputs/expected_fail/output_f3.gif) |

**ผลที่คาดหวัง:** ปกสมุดเรียบ ไม่มี texture → ไม่ detect

---

### f4 — Clear glass bottle

| Output frame | Output GIF |
|---|---|
| ![f4 detected](outputs/expected_fail/output_f4.png) | ![f4 gif](outputs/expected_fail/output_f4.gif) |

**ผลที่คาดหวัง:** ขวดแก้วใส feature เป็นของ background ไม่ใช่วัตถุ → ไม่ detect

---

### f5 — Uniform carpet patch

| Output frame | Output GIF |
|---|---|
| ![f5 detected](outputs/expected_fail/output_f5.png) | ![f5 gif](outputs/expected_fail/output_f5.gif) |

**ผลที่คาดหวัง:** พรมลายซ้ำ keypoint ไม่ stable → ไม่ detect

---

## Unexpected Fail Cases (u1–u5)

วัตถุน่าจะตรวจจับได้ แต่ระบบ fail เพราะปัจจัยที่ไม่คาดคิด

### u1 — Book (motion blur)

| Output frame | Output GIF |
|---|---|
| ![u1 detected](outputs/unexpected_fail/output_u1.png) | ![u1 gif](outputs/unexpected_fail/output_u1.gif) |

**สาเหตุที่ fail:** กล้องส่ายเร็ว → motion blur รุนแรง → keypoint หาย

---

### u2 — Poster (sudden darkness)

| Output frame | Output GIF |
|---|---|
| ![u2 detected](outputs/unexpected_fail/output_u2.png) | ![u2 gif](outputs/unexpected_fail/output_u2.gif) |

**สาเหตุที่ fail:** ไฟดับกลางคลิป → ภาพมืดฉับพลัน → สูญเสีย feature

---

### u3 — Logo crop vs full product

| Output frame | Output GIF |
|---|---|
| ![u3 detected](outputs/unexpected_fail/output_u3.png) | ![u3 gif](outputs/unexpected_fail/output_u3.gif) |

**สาเหตุที่ fail:** Template เป็น logo ขนาด 80×80px, video แสดงสินค้าเต็ม → scale ต่างกันมาก

---

### u4 — Brick wall (repetitive texture)

| Output frame | Output GIF |
|---|---|
| ![u4 detected](outputs/unexpected_fail/output_u4.png) | ![u4 gif](outputs/unexpected_fail/output_u4.gif) |

**สาเหตุที่ fail:** texture ซ้ำกันทำให้ matcher สับสน → homography ผิดพลาด

---

### u5 — Phone back / mirror (reflection)

| Output frame | Output GIF |
|---|---|
| ![u5 detected](outputs/unexpected_fail/output_u5.png) | ![u5 gif](outputs/unexpected_fail/output_u5.gif) |

**สาเหตุที่ fail:** พื้นผิวสะท้อนแสง feature เปลี่ยนตาม viewpoint → matching ไม่ consistent

---

## สรุปผลการทดสอบ

| กลุ่ม | จำนวน | ผลที่คาดหวัง | ผลที่ได้ |
|-------|--------|-------------|---------|
| Easy Success | 5 | ตรวจจับได้ทุก case | ✓ |
| Difficult Success | 5 | ตรวจจับได้แม้มีปัจจัยรบกวน | ✓ |
| Expected Fail | 5 | ไม่ตรวจจับ (ถูกต้อง) | ✓ |
| Unexpected Fail | 5 | ควรตรวจจับได้ แต่ fail | ✓ |

---

## การรันโปรแกรม

```bash
# รัน case เดี่ยว
python run_case.py e2

# รัน case เดี่ยว พร้อม live preview
python run_case.py e2 --show

# จำกัดจำนวน frame (สำหรับทดสอบเร็ว)
python run_case.py e2 --max-frames 60

# รันทุก case และสร้าง results_summary.csv
python run_all.py
```

Output ไฟล์จะอยู่ที่ `outputs/<category>/output_<id>.mp4`, `.png`, `.gif`
