# Challenge 2: Object Detection with Feature Point Matching

**CI 7306 Image Analytics 2/2568**

## 🎓 ข้อมูลผู้จัดทำ

| | |
|---|---|
| **รหัสนักศึกษา** | 6710421004 |
| **ชื่อ** | ชนัญญา เอี่ยมประโคน |

## 🏛️ สถาบัน

- **สถาบัน:** สถาบันบัณฑิตพัฒนบริหารศาสตร์ (NIDA)
- **คณะ:** คณะสถิติประยุกต์
- **สาขา:** วิทยาการคอมพิวเตอร์และระบบสารสนเทศ (CSDT8)

โปรเจกต์นี้เป็นการทดลองใช้ Feature Point Matching เพื่อทำ Object Detection บนไฟล์วิดีโอ โดยใช้เพียงเทคนิค Traditional Image Processing (OpenCV + Python) ทั้งหมด 20 กรณีทดสอบ แบ่งตามระดับความยากและผลลัพธ์ที่ได้

## 📂 ประเภทของกรณีทดสอบ

**กรณีที่สำเร็จ (Success Cases)**
- **Easy Cases (5 วิดีโอ):** วัตถุเป้าหมายตรวจจับได้ง่าย สภาพแสงปกติ พื้นหลังไม่รบกวน
- **Difficult Cases (5 วิดีโอ):** วัตถุเป้าหมายตรวจจับได้ยาก เช่น Contrast ต่ำ หรือวัตถุเบียดทับกัน

**กรณีที่ล้มเหลว (Failed Cases)**
- **Failed as Expected (5 วิดีโอ):** กรณีที่คาดการณ์ไว้ล่วงหน้าแล้วว่าไม่สามารถตรวจจับได้
- **Failed but Unexpected (5 วิดีโอ):** กรณีที่คาดว่าควรจะสำเร็จ แต่ล้มเหลวเนื่องจากข้อจำกัดทางเทคนิคหรือปัจจัยภายนอก

---

# Image Feature Matching — ผลการทดสอบ

ทดลองตรวจจับวัตถุในวิดีโอ โดยใช้ **ภาพต้นแบบ (template)** ไปเทียบกับแต่ละเฟรมของวิดีโอ  
แนวคิดหลักคือให้ระบบมองหา **จุดเด่นของภาพ** เช่น ลาย เส้น ขอบ หรือรายละเอียดบางส่วนของวัตถุ แล้วพยายามจับคู่กับสิ่งที่เห็นในเฟรม

ถ้าระบบเจอจุดที่ตรงกันมากพอ ก็จะสรุปว่าน่าจะเป็นวัตถุชิ้นเดียวกัน และวาด **bounding polygon** ครอบตำแหน่งวัตถุนั้นออกมา

ในแต่ละ case จะมีผลลัพธ์เป็น
- ภาพเฟรมตัวอย่างที่ระบบตรวจจับได้
- GIF ที่แสดงการตีกรอบวัตถุระหว่างที่วัตถุเคลื่อนที่

---

## วิธีที่ใช้โดยรวม

ในการทดลองนี้ ใช้วิธี **feature matching** เป็นหลัก  
พูดง่าย ๆ คือ ระบบจะดึงจุดสำคัญจากภาพต้นแบบและภาพในวิดีโอออกมา แล้วดูว่าจุดไหน “น่าจะเป็นจุดเดียวกัน”

เครื่องมือหลักที่ใช้มีประมาณนี้

- **SIFT** ใช้หาจุดเด่นหรือ **keypoint** จากภาพ
- **CLAHE** ใช้ช่วยเพิ่ม contrast ของภาพในบางบริเวณ ทำให้รายละเอียดบางส่วนชัดขึ้น
- **FLANN matcher** ใช้จับคู่จุดระหว่าง template กับ frame
- **RANSAC / Homography** ใช้คัด match ที่น่าเชื่อถือ และคำนวณตำแหน่งกรอบของวัตถุในเฟรม

จากที่ทดลอง จะเห็นว่าวิธีนี้เหมาะกับวัตถุที่มีลวดลายชัด รูปร่างค่อนข้างคงที่ และพื้นหลังไม่รกมาก  
แต่ถ้าวัตถุเปลี่ยนรูปร่างเยอะ สะท้อนแสงมาก หรือมีวัตถุคล้ายกันหลายชิ้นในฉาก ระบบจะเริ่มมีปัญหา

---

## Easy Success Cases (e1–e5)

กลุ่มนี้เป็นเคสที่ค่อนข้างง่าย  
วัตถุมี texture หรือรายละเอียดชัด มุมมองไม่เปลี่ยนมาก แสงค่อนข้างดี และพื้นหลังไม่ค่อยรบกวน  
เลยทำให้ระบบ detect ได้ค่อนข้างเสถียร

---

### e1 — Spiral Notebook Cover "pplus" (Hand-held Frontal)

| Template | Output GIF |
|---|---|
| ![e1 template](outputs/easy/output_e1.png) | ![e1 gif](outputs/easy/output_e1.gif) |

**ที่มา:** ถ่ายเอง  
**วัตถุเป้าหมาย:** ปกสมุดโน้ต spiral สีน้ำเงิน แบรนด์ "pplus"  
**Template:** `outputs/easy/output_e1.png`  
**Video:** `videos/easy/video_e1.mp4`

**อธิบายผลลัพธ์:**  
ปกสมุดเคสนี้มีรายละเอียดบนภาพค่อนข้างเยอะ ทั้งไอคอน IoT ภาพ cityscape และโลโก้ต่าง ๆ ทำให้ระบบสามารถหา **keypoint** ได้หลายตำแหน่ง โดยเฉพาะตามเส้น ขอบ และลวดลายบนหน้าปก ตัวสมุดยังหันค่อนข้างตรงเข้ากล้องอยู่ตลอด ทำให้ลักษณะของวัตถุในแต่ละเฟรมไม่เปลี่ยนมากเกินไป ส่วนพื้นหลังเป็นผนังเรียบ ๆ ที่มี **texture ต่ำ** เลยช่วยลด **false match** จากฉากหลังได้ค่อนข้างดี การใช้ **CLAHE** ยังช่วยเพิ่ม contrast บริเวณไอคอนสีขาวบนพื้นน้ำเงิน ทำให้ระบบ detect และวาด bounding polygon ครอบสมุดได้ค่อนข้างแม่นตลอดวิดีโอ

---

### e2 — Airbus A380 Approaching Landing

| Template | Output GIF |
|---|---|
| ![e2 template](outputs/easy/output_e2.png) | ![e2 gif](outputs/easy/output_e2.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=d-p1UFcj14U&t=633s  
**วัตถุเป้าหมาย:** เครื่องบิน Airbus A380 กำลังบินเข้าสู่รันเวย์  
**Template:** `outputs/easy/output_e2.png`  
**Video:** `videos/easy/video_e2.mp4`

**อธิบายผลลัพธ์:**  
เครื่องบินในเคสนี้เห็นจากด้านหน้าค่อนข้างชัด ใต้ท้องเครื่องมีรายละเอียดหลายส่วน เช่น เครื่องยนต์ ล้อ และขอบปีก ซึ่งเป็นบริเวณที่เกิด keypoint ได้พอสมควร ขณะเดียวกันพื้นหลังเป็นท้องฟ้าโล่ง ๆ ที่แทบไม่มี texture รบกวน จึงช่วยให้ระบบโฟกัสที่ตัวเครื่องบินได้ง่ายขึ้น ถึงแม้ขนาดของเครื่องบินจะค่อย ๆ ใหญ่ขึ้นเมื่อบินเข้ามาใกล้กล้อง แต่ระบบยัง match กับ template ได้ดี และสามารถตีกรอบวัตถุได้ต่อเนื่องตลอดคลิป

---

### e3 — Joker Playing Card (Overhead on Grey Surface)

| Template | Output GIF |
|---|---|
| ![e3 template](outputs/easy/output_e3.png) | ![e3 gif](outputs/easy/output_e3.gif) |

**ที่มา:** ถ่ายเอง  
**วัตถุเป้าหมาย:** ไพ่ Joker (ภาพดอกกุหลาบ + ใบหน้า)  
**Template:** `outputs/easy/output_e3.png`  
**Video:** `videos/easy/video_e3.mp4`

**อธิบายผลลัพธ์:**  
ไพ่ Joker ใบนี้มีลายเส้นละเอียดค่อนข้างมาก ทั้งรูปใบหน้าและดอกกุหลาบ ทำให้ SIFT หา keypoint ได้หนาแน่นบนตัวไพ่ พื้นหลังเป็นพื้นสีเทาเรียบที่มีรายละเอียดน้อย จึงแทบไม่ดึง match ออกไปจากวัตถุ อีกทั้งตัวไพ่เป็นวัตถุแบนและกล้องมองจากด้านบนค่อนข้างตรง ทำให้การจับคู่ระหว่าง template กับเฟรมเป็นไปได้ง่าย ผลที่ได้คือระบบตีกรอบวัตถุได้ค่อนข้างนิ่งและแม่นตลอดวิดีโอ

---

### e4 — USB-C Hub (Static on White Background)

| Template | Output GIF |
|---|---|
| ![e4 template](outputs/easy/output_e4.png) | ![e4 gif](outputs/easy/output_e4.gif) |

**ที่มา:** ถ่ายเอง  
**วัตถุเป้าหมาย:** USB-C Hub ยี่ห้อ ADAN  
**Template:** `outputs/easy/output_e4.png`  
**Video:** `videos/easy/video_e4.mp4`

**อธิบายผลลัพธ์:**  
USB-C Hub ตัวนี้วางอยู่บนพื้นขาวเรียบ ทำให้ฉากหลังแทบไม่มีจุดรบกวนเลย จุดเด่นของวัตถุจะอยู่บริเวณขอบโลหะ ช่องพอร์ต และโลโก้บนตัวอุปกรณ์ ซึ่งช่วยให้ระบบหา keypoint ได้ในตำแหน่งที่ค่อนข้างเสถียร นอกจากนี้มุมมองของกล้องแทบไม่เปลี่ยน และตัววัตถุก็ไม่ค่อยเคลื่อนไหว จึงทำให้ระบบ detect ได้สม่ำเสมอเกือบทุกเฟรม

---

### e5 — Oreo Snack Wrapper (Hand-held Against White Background)

| Template | Output GIF |
|---|---|
| ![e5 template](outputs/easy/output_e5.png) | ![e5 gif](outputs/easy/output_e5.gif) |

**ที่มา:** ถ่ายเอง  
**วัตถุเป้าหมาย:** ซองขนม Oreo (บรรจุภัณฑ์ภาษาจีน) ถือในมือ  
**Template:** `outputs/easy/output_e5.png`  
**Video:** `videos/easy/video_e5.mp4`

**อธิบายผลลัพธ์:**  
ซอง Oreo มีสีค่อนข้างเด่นและมีทั้งโลโก้กับตัวอักษรที่ให้รายละเอียดชัดเจน ทำให้ระบบหา keypoint ได้ค่อนข้างดี โดยเฉพาะบริเวณขอบตัวอักษรและกราฟิกบนซอง แม้จะถือด้วยมือและมีการขยับเล็กน้อย แต่ตัวซองยังค่อนข้างแบน และมุมมองไม่ได้เปลี่ยนมาก ส่วนพื้นหลังสีขาวก็ช่วยลด false match จากสิ่งรอบข้างได้ดี จึงทำให้ระบบ detect วัตถุได้ต่อเนื่องตลอดวิดีโอ

---

## Difficult Success Cases (d1–d5)

กลุ่มนี้เป็นเคสที่ยากขึ้นจาก easy cases  
แม้สุดท้ายระบบจะยังตรวจจับได้ แต่ก็มีปัจจัยรบกวนเพิ่มเข้ามา เช่น วัตถุโดนบัง พื้นหลังรก แสงน้อย หรือมีวัตถุคล้ายกันอยู่ในฉาก  
จึงต้องปรับค่าบางอย่างให้เข้มขึ้นเล็กน้อยเพื่อกรอง match ที่ไม่ดีออก

---

### d1 — Plaid Notebook (Partial Hand Occlusion on Wooden Table)

| Template | Output GIF |
|---|---|
| ![d1 template](outputs/difficult/output_d1.png) | ![d1 gif](outputs/difficult/output_d1.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=DD7lU3S_jpY  
**วัตถุเป้าหมาย:** สมุดโน้ตลาย plaid (ตาราง) สีน้ำเงิน  
**Template:** `outputs/difficult/output_d1.png`  
**Video:** `videos/difficult/video_d1.mp4`  
**Parameters:** ratio=0.70, min_matches=8, min_inliers=6, ransac_thresh=5.0

**อธิบายผลลัพธ์:**  
ความยากของเคสนี้คือมีมือบังสมุดอยู่บางส่วน ทำให้รายละเอียดบนวัตถุหายไปพอสมควร อีกอย่างคือลายไม้บนโต๊ะมีเส้นบางส่วนที่ดูคล้ายกับลายตารางของสมุด จึงมีโอกาสเกิด false match ได้ง่ายกว่า easy case อย่างไรก็ตาม บริเวณที่ไม่ถูกบังยังมี keypoint เหลือพอให้ระบบใช้จับคู่ได้ และเมื่อปรับ ratio ให้เข้มงวดขึ้น ระบบก็ยังสามารถคัด match ที่น่าเชื่อถือออกมาและตีกรอบสมุดได้ค่อนข้างถูกต้อง

---

### d2 — Pigeons in Flight (Dynamic Cloudy Sky Background)

| Template | Output GIF |
|---|---|
| ![d2 template](outputs/difficult/output_d2.png) | ![d2 gif](outputs/difficult/output_d2.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=wZVbPe5HVvg  
**วัตถุเป้าหมาย:** นกพิราบ 2 ตัวกำลังบิน  
**Template:** `outputs/difficult/output_d2.png`  
**Video:** `videos/difficult/video_d2.mp4`  
**Parameters:** ratio=0.70, min_matches=8, min_inliers=6, ransac_thresh=5.0

**อธิบายผลลัพธ์:**  
เคสนี้ยากตรงที่ฉากหลังไม่ได้นิ่ง เพราะก้อนเมฆมีลักษณะเปลี่ยนไปเรื่อย ๆ ทำให้ background มีผลต่อการจับคู่ นอกจากนี้ตัวนกเองก็มีลายขนที่ค่อนข้างซ้ำกัน และปีกยังขยับตลอดเวลา ทำให้บางจุดไม่คงที่ในทุกเฟรม แต่ในส่วนของลำตัวและโครงหลักของนกยังมีรายละเอียดที่พอใช้เป็นจุดอ้างอิงได้ เมื่อปรับภาพด้วย CLAHE และใช้การคัด match ที่เข้มขึ้น ระบบจึงยัง detect วัตถุได้ แม้จะยากกว่ากลุ่ม easy ชัดเจน

---

### d3 — White Cat in Dark Car Scene (Low Light & Cluttered Background)

| Template | Output GIF |
|---|---|
| ![d3 template](outputs/difficult/output_d3.png) | ![d3 gif](outputs/difficult/output_d3.gif) |

**ที่มา:** YouTube — https://youtu.be/ZH7umQiTBlI?si=gX_j9VFGwV1NfnQ9  
**วัตถุเป้าหมาย:** แมวขาวสวมเสื้อสีทอง ในรถยนต์  
**Template:** `outputs/difficult/output_d3.png`  
**Video:** `videos/difficult/video_d3.mp4`  
**Parameters:** ratio=0.70, min_matches=8, min_inliers=6, ransac_thresh=6.0

**อธิบายผลลัพธ์:**  
ในฉากนี้แสงค่อนข้างน้อย ทำให้รายละเอียดหลายส่วนของภาพไม่ชัดเหมือนเคสอื่น ๆ และในรถยังมีคนกับเบาะที่สร้าง keypoint แข่งกับตัวแมวด้วย ตัวแมวเองก็มีขนสีขาวที่ค่อนข้างเรียบ ไม่ได้มี texture มากนัก ดังนั้นจุดที่ระบบใช้จับคู่จริง ๆ จะไปอยู่ที่ใบหน้าและเสื้อสีทองมากกว่า การใช้ CLAHE ช่วยดึง contrast ในบริเวณมืดให้ดีขึ้น ทำให้ยังพอมี match ที่ใช้งานได้ และสุดท้ายระบบก็ยังตีกรอบแมวได้ในหลายช่วงของวิดีโอ

---

### d4 — Sea Turtle Underwater (Color Cast & Coral Background)

| Template | Output GIF |
|---|---|
| ![d4 template](outputs/difficult/output_d4.png) | ![d4 gif](outputs/difficult/output_d4.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=klK6mX8jnHQ  
**วัตถุเป้าหมาย:** เต่าทะเล (green sea turtle)  
**Template:** `outputs/difficult/output_d4.png`  
**Video:** `videos/difficult/video_d4.mp4`  
**Parameters:** ratio=0.70, min_matches=8, min_inliers=6, ransac_thresh=7.0

**อธิบายผลลัพธ์:**  
ภาพใต้น้ำจะมีข้อจำกัดเรื่องสีและความคมชัด เพราะน้ำทำให้ภาพดูอมฟ้าเขียวและขอบวัตถุไม่ชัดเท่าบนบก อีกทั้งพื้นหลังยังมีปะการังที่มี texture ค่อนข้างเยอะ ทำให้ระบบสับสนได้ง่าย แต่ข้อดีของเคสนี้คือกระดองเต่ามีลายที่ค่อนข้างชัดและมีรูปแบบเฉพาะตัว จึงยังให้ keypoint ที่เสถียรอยู่พอสมควร แม้เต่าจะเปลี่ยนมุมระหว่างว่ายน้ำ แต่เมื่อผ่อน threshold ของการคำนวณกรอบลงเล็กน้อย ระบบก็ยังตามตำแหน่งวัตถุได้สำเร็จ

---

### d5 — Elephant Herd Crossing River (Similar-instance Confusion)

| Template | Output GIF |
|---|---|
| ![d5 template](outputs/difficult/output_d5.png) | ![d5 gif](outputs/difficult/output_d5.gif) |

**ที่มา:** Kaggle — https://www.kaggle.com/code/mistag/play-video-in-notebook/input  
**วัตถุเป้าหมาย:** ช้างตัวหนึ่งในฝูง (ใช้ template ช้างตัวเดียว)  
**Template:** `outputs/difficult/output_d5.png`  
**Video:** `videos/difficult/video_d5.mp4`  
**Parameters:** ratio=0.70, min_matches=8, min_inliers=6, ransac_thresh=5.0

**อธิบายผลลัพธ์:**  
เคสนี้ยากเพราะในภาพมีช้างหลายตัวที่หน้าตาและพื้นผิวใกล้เคียงกันมาก ระบบจึงมีโอกาสสับสนว่าควรจับตัวไหนเป็นเป้าหมายจริง นอกจากนี้สีผิวของช้างยังใกล้กับสีของโคลนและน้ำในฉาก ทำให้ขอบวัตถุไม่เด่นมากเหมือน easy case อย่างไรก็ตาม รายละเอียดตามรอยย่นและพื้นผิวของช้างยังพอช่วยให้ระบบแยก match ที่พอใช้ได้ออกมา เมื่อคุม false match ให้เข้มขึ้น ระบบจึงยังสามารถ detect ช้างตัวเป้าหมายได้ในหลายเฟรม

---

## Expected Fail Cases (f1–f5)

กลุ่มนี้เป็นเคสที่ตั้งแต่ก่อนทดลองก็พอคาดได้ว่าน่าจะไม่เหมาะกับวิธี feature matching มากนัก  
เพราะลักษณะของวัตถุหรือฉากขัดกับแนวคิดของวิธีนี้โดยตรง เช่น วัตถุเปลี่ยนรูปร่างตลอด ไม่มีลวดลายคงที่ หรือมีสิ่งรบกวนมากเกินไป

---

### f1 — Pedestrian on Busy London Street

| Template | Output GIF |
|---|---|
| ![f1 template](outputs/expected_fail/output_f1.png) | ![f1 gif](outputs/expected_fail/output_f1.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=YzcawvDGe4Y  
**วัตถุเป้าหมาย:** ผู้หญิงคนหนึ่ง (เสื้อขาว กางเกงน้ำตาล มองด้านหลัง) ในฝูงชน  
**Template:** `outputs/expected_fail/output_f1.png`  
**Video:** `videos/expected_fail/video_f1.mp4`

**วิธีที่ลองแล้ว:** ใช้ pipeline มาตรฐานของ SIFT + CLAHE + FLANN + RANSAC

**อธิบายผลลัพธ์:**  
ระบบไม่ค่อยเหมาะกับการตามคนในฝูงชน เพราะตัวคนมีการเปลี่ยนท่าทางตลอดเวลา ทั้งแขน ขา และลักษณะการเดิน ทำให้รูปร่างไม่คงที่เหมือนวัตถุแข็ง อีกทั้งฉากถนนยังมีรายละเอียดเยอะมาก เช่น อาคาร ป้ายร้าน พื้นถนน และคนอื่น ๆ ซึ่งสร้าง keypoint มากกว่าตัวเป้าหมายด้วยซ้ำ ผลคือระบบมีแนวโน้มไปจับฉากหลังหรือวัตถุอื่นแทน และเมื่อมีการบังกันในฝูงชน ก็ยิ่งทำให้การ detect ไม่ต่อเนื่อง สรุปว่าเคสนี้ fail ตามที่คาดไว้

---

### f2 — White Van on Highway Traffic

| Template | Output GIF |
|---|---|
| ![f2 template](outputs/expected_fail/output_f2.png) | ![f2 gif](outputs/expected_fail/output_f2.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=nt3D26lrkho&t=22s  
**วัตถุเป้าหมาย:** รถตู้สีขาว (delivery van) บนไฮเวย์  
**Template:** `outputs/expected_fail/output_f2.png`  
**Video:** `videos/expected_fail/video_f2.mp4`

**วิธีที่ลองแล้ว:** ใช้ pipeline มาตรฐานของ SIFT + CLAHE + FLANN + RANSAC

**อธิบายผลลัพธ์:**  
เคสนี้ fail เพราะรถเคลื่อนที่ค่อนข้างเร็ว และอยู่ในฉากไม่นานพอให้ระบบจับได้อย่างมั่นคง นอกจากนี้ยังมีรถตู้สีขาวหลายคันที่มีลักษณะใกล้กันมาก ทำให้ระบบแยกไม่ค่อยออกว่าคันไหนคือคันเป้าหมายจริง อีกด้านหนึ่งฉากบนถนนก็มีเส้น lane ป้าย และแบริเออร์ที่สร้างรายละเอียดรบกวนเข้ามาอีก สุดท้ายจึงไม่สามารถ detect รถเป้าหมายได้อย่างน่าเชื่อถือ

---

### f3 — EU Flag Waving in Wind

| Template | Output GIF |
|---|---|
| ![f3 template](outputs/expected_fail/output_f3.png) | ![f3 gif](outputs/expected_fail/output_f3.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=cAgyPg1gEPA  
**วัตถุเป้าหมาย:** ธงสหภาพยุโรป (EU flag)  
**Template:** `outputs/expected_fail/output_f3.png`  
**Video:** `videos/expected_fail/video_f3.mp4`

**วิธีที่ลองแล้ว:** ใช้ pipeline มาตรฐานของ SIFT + CLAHE + FLANN + RANSAC

**อธิบายผลลัพธ์:**  
ธงเป็นวัตถุที่เปลี่ยนรูปตลอดเวลาเพราะโดนลมพัด บางจังหวะมีการพับ บิด หรือบังกันเอง ทำให้ลวดลายบนธงไม่เหมือนกับภาพต้นแบบแบบต่อเนื่อง ถึงบางเฟรมระบบจะพอวาดกรอบขึ้นมาได้ แต่รูปทรงของกรอบก็มักเพี้ยนและไม่นิ่งมาก จึงถือว่าโดยรวมแล้วไม่สามารถ detect ได้สำเร็จ สาเหตุหลักมาจากวัตถุประเภทผ้าที่ไม่คงรูป ซึ่งไม่ค่อยเหมาะกับการจับคู่แบบ template-based matching

---

### f4 — Shark in Deep Ocean

| Template | Output GIF |
|---|---|
| ![f4 template](outputs/expected_fail/output_f4.png) | ![f4 gif](outputs/expected_fail/output_f4.gif) |

**ที่มา:** YouTube — https://youtu.be/eoTpdTU8nTA?si=N3zjon83FwVY4fNC  
**วัตถุเป้าหมาย:** ฉลาม (shark) ใต้ทะเลลึก  
**Template:** `outputs/expected_fail/output_f4.png`  
**Video:** `videos/expected_fail/video_f4.mp4`

**วิธีที่ลองแล้ว:** ใช้ SIFT + CLAHE แบบปรับเข้มขึ้น + FLANN + RANSAC

**อธิบายผลลัพธ์:**  
สาเหตุที่ fail ชัดที่สุดคือ ตัวฉลามกับฉากใต้น้ำมีโทนสีและความเข้มใกล้กันมาก ทำให้ขอบวัตถุไม่ชัดและเกิด keypoint บนตัวฉลามน้อยมาก ต่อให้เพิ่ม CLAHE ก็ช่วยได้แค่ระดับหนึ่ง เพราะถ้ารายละเอียดต้นทางแทบไม่มีอยู่แล้ว ก็ยากที่จะดึงออกมาได้จริง สุดท้าย keypoint ที่ระบบพบกลับไปอยู่บนพื้นทรายหรือสิ่งอื่นในฉากมากกว่า จึงไม่สามารถ detect ฉลามได้

---

### f5 — Smoke / Steam (Textureless Non-rigid Object)

| Template | Output GIF |
|---|---|
| ![f5 template](outputs/expected_fail/output_f5.png) | ![f5 gif](outputs/expected_fail/output_f5.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=KEN6S2beTc0  
**วัตถุเป้าหมาย:** ควัน/ไอน้ำ (smoke/steam) จากถ้วยกาแฟ  
**Template:** `outputs/expected_fail/output_f5.png`  
**Video:** `videos/expected_fail/video_f5.mp4`

**วิธีที่ลองแล้ว:** ใช้ pipeline มาตรฐานของ SIFT + CLAHE + FLANN + RANSAC

**อธิบายผลลัพธ์:**  
ควันหรือไอน้ำแทบไม่มีลวดลายคงที่เลย และรูปร่างก็เปลี่ยนไปตลอดเวลาในทุกเฟรม ทำให้ระบบหา keypoint ที่ “ซ้ำได้” ระหว่างภาพต้นแบบกับวิดีโอแทบไม่ได้เลย นอกจากนี้ลักษณะของควันยังขึ้นกับพื้นหลังและแสงในแต่ละช่วงด้วย จึงทำให้การ match ไม่เกิดขึ้นจริง สรุปคือเคสนี้ fail แบบชัดเจน เพราะวัตถุประเภทนี้ไม่เหมาะกับการใช้ feature matching ตั้งแต่ต้น

---

## Unexpected Fail Cases (u1–u5)

กลุ่มนี้เป็นเคสที่ตอนแรกคาดว่าน่าจะผ่าน หรืออย่างน้อยน่าจะพอ detect ได้  
เพราะวัตถุดูมีรายละเอียดเยอะ หรือดูเด่นพอสำหรับการจับคู่  
แต่พอลองจริงกลับ fail หรือได้ผลที่ไม่นิ่ง ซึ่งทำให้เห็นข้อจำกัดของวิธีนี้ชัดขึ้นมาก

---

### u1 — Gold Jewelry (Earring/Pendant) — Reflective Surface & 3D Viewpoint Change

| Output frame | Output GIF |
|---|---|
| ![u1 keypoints](outputs/unexpected_fail/output_u1.png) | ![u1 gif](outputs/unexpected_fail/output_u1.gif) |

**ที่มา:** YouTube — https://youtube.com/shorts/hz8xmkeo8qU  
**วัตถุเป้าหมาย:** ต่างหู/จี้ทองแบบ chandelier ประดับ filigree และอัญมณีสีแดง-ม่วง  
**Template:** `templates/unexpected_fail/template_u1.jpg`  
**Video:** `videos/unexpected_fail/video_u1.mp4`  
**จำนวน keypoint บน template:** 1,150 จุด

**อธิบายผลลัพธ์:**  
ตอนแรกเคสนี้ดูน่าจะผ่าน เพราะเครื่องประดับมีรายละเอียดเยอะมาก และระบบก็หา keypoint บน template ได้สูงมากจริง ๆ แต่พอทดลองกับวิดีโอ กลับพบว่าการ detect เกิดขึ้นแค่บางช่วง โดยเฉพาะตอนที่มุมมองและแสงใกล้กับภาพต้นแบบ พอเครื่องประดับหมุนหรือแสงสะท้อนเปลี่ยน ตำแหน่ง highlight บนผิวทองและอัญมณีก็เปลี่ยนตาม ทำให้ descriptor หลายจุดไม่เหมือนเดิมอีกต่อไป อีกประเด็นคือเครื่องประดับเป็นวัตถุ 3 มิติ ไม่ได้แบนเหมือนกระดาษหรือซองขนม ดังนั้นพอเปลี่ยนมุม กลุ่มลายที่เห็นในภาพก็เปลี่ยนตามไปด้วย สรุปคือเคสนี้แสดงให้เห็นว่า **จำนวน keypoint เยอะ ไม่ได้แปลว่าจะ detect ได้เสถียรเสมอไป**

---

### u2 — Orange Fruit — Smooth Curved Surface & Insufficient Gradient

| Output frame | Output GIF |
|---|---|
| ![u2 keypoints](outputs/unexpected_fail/output_u2.png) | ![u2 gif](outputs/unexpected_fail/output_u2.gif) |

**ที่มา:** YouTube — https://youtu.be/GDk7Z9zkFws  
**วัตถุเป้าหมาย:** ส้มผลเดียว บนพื้นหลังเรียบ  
**Template:** `templates/unexpected_fail/template_u2.jpg`  
**Video:** `videos/unexpected_fail/video_u2.mp4`  
**จำนวน keypoint บน template:** 193 จุด

**อธิบายผลลัพธ์:**  
เคสนี้ตอนแรกดูเหมือนง่าย เพราะส้มเป็นวัตถุเด่นและพื้นหลังก็ไม่ซับซ้อน แต่พอลองจริงระบบกลับ detect ไม่ได้เลย สาเหตุหลักคือผิวส้มถึงจะดูมี texture ด้วยตาเปล่า แต่สำหรับระบบแล้วรายละเอียดพวกนั้นค่อนข้างเบาและมีลักษณะซ้ำกันไปทั่วผล ทำให้เกิด keypoint ไม่มาก และหลายจุดก็คล้ายกันเกินไปจนแยกไม่ออก อีกทั้งส้มยังเป็นวัตถุทรงกลม พอขยับหรือหมุน มุมของผิวที่เห็นก็เปลี่ยนไปจาก template ได้ง่าย จึงทำให้การ match ไม่เพียงพอสำหรับการตีกรอบวัตถุ

---

### u3 — Clownfish (Nemo) — Non-rigid Swimming & Coral Background Dominance

| Output frame | Output GIF |
|---|---|
| ![u3 keypoints](outputs/unexpected_fail/output_u3.png) | ![u3 gif](outputs/unexpected_fail/output_u3.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=RCOH9SD5obw&t=6744s  
**วัตถุเป้าหมาย:** ปลา Clownfish (Nemo) ลายส้ม-ขาว-ดำ  
**Template:** `templates/unexpected_fail/template_u3.jpg`  
**Video:** `videos/unexpected_fail/video_u3.mp4`  
**จำนวน keypoint บน template:** 1,293 จุด

**อธิบายผลลัพธ์:**  
ปลาการ์ตูนในเคสนี้มีลายสีเด่นชัด และบน template ก็มี keypoint เยอะมาก จนตอนแรกคิดว่าน่าจะ detect ได้ง่าย แต่ปัญหาจริงกลับอยู่ที่ฉากรอบ ๆ ตัวปลา เพราะปะการังและ anemone มีสีและ texture ใกล้กับตัวปลา ทำให้ระบบดึง match ไปที่พื้นหลังจำนวนมาก บางเฟรมกรอบไปอยู่บนตัวปลา แต่บางเฟรมกลับกระโดดไปครอบส่วนของ anemone แทน นอกจากนี้ตัวปลายังเป็นวัตถุที่เคลื่อนไหวแบบไม่คงรูป มีการงอหาง ขยับครีบ และเปลี่ยนท่าทางตลอดเวลา จึงทำให้การ detect ไม่เสถียร สรุปว่าแม้ตัว template จะดูดีมาก แต่เมื่ออยู่ในฉากจริงที่ซับซ้อน ระบบก็ยัง fail ได้

---

### u4 — Ink Dissolving in Water — Non-rigid Morphing & No Stable Texture

| Output frame | Output GIF |
|---|---|
| ![u4 keypoints](outputs/unexpected_fail/output_u4.png) | ![u4 gif](outputs/unexpected_fail/output_u4.gif) |

**ที่มา:** YouTube — https://www.youtube.com/watch?v=pGbIOC83-So  
**วัตถุเป้าหมาย:** หมึก/สีน้ำสีน้ำเงินกำลังกระจายตัวในน้ำ (ink diffusion)  
**Template:** `templates/unexpected_fail/template_u4.jpg`  
**Video:** `videos/unexpected_fail/video_u4.mp4`  
**จำนวน keypoint บน template:** 822 จุด

**อธิบายผลลัพธ์:**  
นี่เป็นอีกเคสที่ตอนแรกดูเหมือนน่าจะผ่าน เพราะรูปทรงของหมึกใน template ดูซับซ้อนและมีรายละเอียดเยอะมาก แต่ปัญหาคือรายละเอียดเหล่านั้นเป็นแค่ “รูปทรงชั่วขณะ” ของของเหลวเท่านั้น พอเวลาผ่านไปแม้แค่ไม่กี่เฟรม รูปร่างของหมึกก็เปลี่ยนไปหมดแล้ว ทำให้ keypoint ที่เคยเจอใน template ไม่สามารถเอาไป match กับเฟรมถัดไปได้จริง สุดท้ายจึงไม่เกิดการ detect เลย เคสนี้ชัดมากว่าการมี keypoint เยอะไม่ได้ช่วย ถ้าโครงสร้างของวัตถุไม่คงที่พอ

---

### u5 — Ant — Reflective Exoskeleton, Non-rigid Motion & Tiny Scale

| Output frame | Output GIF |
|---|---|
| ![u5 keypoints](outputs/unexpected_fail/output_u5.png) | ![u5 gif](outputs/unexpected_fail/output_u5.gif) |

**ที่มา:** YouTube — https://youtu.be/AKQkuNifoas  
**วัตถุเป้าหมาย:** มดตัวเดียว บนพื้นหลังขาว  
**Template:** `templates/unexpected_fail/template_u5.jpg`  
**Video:** `videos/unexpected_fail/video_u5.mp4`  
**จำนวน keypoint บน template:** 236 จุด

**อธิบายผลลัพธ์:**  
เคสนี้ไม่ได้ fail แบบไม่ detect เลย แต่ fail เพราะ detect ผิดเป้าหมาย กล่าวคือในวิดีโอมีมดมากกว่าหนึ่งตัว และระบบไม่สามารถแยกได้ชัดว่าตัวไหนคือตัวที่ตรงกับ template จริง สุดท้ายกรอบที่ได้จึงขยายไปครอบมดสองตัวพร้อมกันในบางช่วง นอกจากนี้มดยังเป็นวัตถุขนาดเล็กมาก และมีการขยับส่วนต่าง ๆ ของร่างกาย เช่น ขา หนวด และท้องตลอดเวลา ทำให้การจับคู่ไม่เสถียร อีกทั้งพื้นผิวของมดมีความเงาเล็กน้อย จึงยิ่งทำให้ descriptor เปลี่ยนไปตามแสงได้ง่าย สรุปคือระบบ detect ได้ แต่ไม่สามารถรักษา identity ของมดตัวเป้าหมายได้จริง

---

## สรุปภาพรวมผลการทดลอง

จากผลการทดลองทั้งหมด สามารถสรุปได้ว่า **feature matching** เหมาะกับวัตถุที่มีลักษณะประมาณนี้

- มีลวดลายหรือรายละเอียดชัด
- มี keypoint ที่ค่อนข้างเฉพาะตัว
- รูปร่างค่อนข้างคงที่
- มุมมองไม่เปลี่ยนแรงเกินไป
- พื้นหลังไม่รกหรือมี texture ต่ำ

ตัวอย่างที่เหมาะคือ
- สมุด
- ไพ่
- ซองขนม
- อุปกรณ์ที่มีโลโก้หรือขอบชัด
- วัตถุแบนหรือวัตถุที่ไม่ค่อยเปลี่ยนรูป

ส่วนวัตถุที่มักทำให้ระบบ fail จะมีลักษณะประมาณนี้

- เปลี่ยนรูปร่างตลอดเวลา เช่น ควัน หมึก ธง
- เป็นวัตถุ 3 มิติที่เปลี่ยนมุมแล้วหน้าตาเปลี่ยนมาก เช่น เครื่องประดับ
- มีผิวเรียบหรือ texture ซ้ำ ๆ เช่น ส้ม
- มีหลายตัวที่หน้าตาคล้ายกันมาก เช่น มด ช้าง รถ
- อยู่ในฉากที่พื้นหลังเด่นหรือซับซ้อนกว่าวัตถุเป้าหมาย

ดังนั้น ถ้าต้องการใช้งานจริง วิธีนี้จะเหมาะกับการตรวจจับวัตถุที่ “ลายชัด รูปร่างนิ่ง และไม่โดนรบกวนมาก”  
แต่ถ้าจะนำไปใช้กับคน สัตว์ ฝูงวัตถุ หรือสิ่งที่เปลี่ยนรูปตลอดเวลา อาจต้องใช้วิธีอื่นร่วมด้วย เช่น object detection, tracking หรือ segmentation

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