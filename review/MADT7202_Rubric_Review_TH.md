# ผลตรวจ MADT7202 Midterm Update3

ตรวจวันที่ 12 ตุลาคม 2026 จาก Assignment, Sample Reports, รายงาน Update3, Excel ที่แนบ และ MADT7202_repo_Update3.zip โดยใช้ข้อกำหนดในเอกสารเป็นเกณฑ์ประเมิน ไม่ถือเป็นคำสั่งให้ดำเนินการนอกคำขอของผู้ใช้

## ข้อสรุป

รายงานมีโครงสร้างครบและโค้ดรองรับตัวเลขชุดหลักจริง แต่ยังไม่ควรจัดเป็น Advanced ครบทุกด้าน จุดสำคัญที่สุดคือหลักฐานสิทธิ์ใช้ข้อมูลและคำอธิบายแหล่งข้อมูล รองลงมาคือการอธิบาย robustness ให้ตรงกับผล และการเพิ่ม URL ที่เปิดได้จริง

ผู้ใช้ยืนยันว่า ScentSelf เป็น IS ส่วนตัว ไม่ใช่งานกลุ่ม ดังนั้นการเป็น IS ไม่ได้ผิดข้อห้ามใช้ corpus ของทีมโดยตัวมันเอง ส่วนข้อกำหนดคนละอุตสาหกรรมยังต้องเทียบกับหัวข้องานกลุ่มของวิชานี้

## เทียบ Rubric

| เกณฑ์ | ระดับที่หลักฐานรองรับ | สิ่งที่ต้องแก้ |
|---|---|---|
| Business problem framing /6 | เข้าองค์ประกอบ Advanced | มีเจ้าของการตัดสินใจ คำถามเรื่อง paths และกรณีไม่มีผู้ผ่านเกณฑ์ชัดเจน ควรระบุวัน tester round |
| Data sourcing /8 | ยังไม่ผ่านเงื่อนไข Good ครบ | ไม่ได้รับอนุญาต automated access; ช่วงเก็บข้อมูลไม่แน่นอน; อ้างแหล่งเดียวทั้งที่มีโน้ตเสริม Parfumo |
| Graph construction /8 | Good และมีองค์ประกอบ Advanced | node/edge/weight/pruning/size ชัดเจน มีทางเลือก NPMI และ cutoff แต่ควรย่อผลเปรียบเทียบจริงลงหน้า PDF และระบุ distance=1/weight |
| Insight and business action /8 | Good และมีองค์ประกอบ Advanced | ข้อสรุปไม่มีผู้ผ่านเกณฑ์มีตัวเลขรองรับ แต่ control เปลี่ยนในชุดใหญ่; ต้องไม่เหมารวมว่า Lemon robust ทุกวิธี และต้องกำหนดเกณฑ์ตัดสิน tester |

ไม่ให้คะแนนรับรองแทนอาจารย์ เพราะโจทย์ไม่ได้ระบุวิธีหักคะแนนเมื่อผิดกติกาแหล่งข้อมูล และคะแนน Advanced ต้องมีทุกองค์ประกอบของ Good ก่อน

## สิ่งที่ตรวจยืนยันแล้ว

- PDF มี 1 หน้า ขนาด 594.96 × 841.92 pt ใกล้เคียง A4; ตัวอักษร PDF เล็กสุด 10 pt; ขอบข้อความประมาณ 1.59 ซม.ขึ้นไป ภาพกราฟอ่านได้และมี label/legend
- Excel มี 1,788 รายการ = Fragrantica 1,785 + Official Product 3; Fragrantica ไม่มีโน้ต 5 จึงเหลือ 1,780 รายการ
- รัน numerical cells ของ notebook ต้นฉบับกับ Excel และ collection list ในเครื่อง ชุดหลักได้ 209 perfumes, 356 notes, 89 eligible notes, 20 nodes, 23 edges, components 13/3/2/2, 7 positive-betweenness nodes, Spearman 0.66
- ผล bootstrap ชุด 209 ตรงกับรายงาน: Lemon ประมาณ 87%, Peach ประมาณ 24%; ไม่มีโน้ตผ่านเกณฑ์ทั้งหมด
- NPMI ที่ raw cutoff 6 และ NPMI > 0.1 ยังคง bridge เดิม 7/7 แต่มี bridge รวม 9 และอันดับต้นเปลี่ยนเป็น Mandarin Orange แล้ว Lemon
- รูปที่มีอยู่ตรวจจาก PDF; ไม่ได้รันสร้างภาพใหม่ในการตรวจ numerical cells

## แก้ก่อนส่ง เรียงลำดับความสำคัญ

### 1. แก้เงื่อนไขแหล่งข้อมูลด้วยหลักฐานจริง

Assignment กำหนด permitted scraping หรือ documented secondary source พร้อมสิทธิ์ใช้งาน ไม่ใช่เพียงบอกว่าใช้เพื่อการศึกษา

รายงานและ README ระบุว่าไม่ได้รับอนุญาต Fragrantica ToS §5.3 ที่ตรวจจากหน้าเว็บระบุข้อจำกัด automated access ต้องได้รับอนุญาตเป็นลายลักษณ์อักษร จึงยังไม่ผ่านเงื่อนไขโจทย์ การไม่เผยแพร่ raw data ไม่ได้ทำให้การเก็บข้อมูลได้รับอนุญาตย้อนหลัง

ทางแก้คือมีหนังสืออนุญาตที่ครอบคลุมการใช้จริง หรือเปลี่ยนเป็นข้อมูลที่มีสิทธิ์ชัดเจนและรันใหม่ หากขอให้อาจารย์พิจารณาข้อยกเว้น ต้องรายงานตามจริงและแยกออกจากสิทธิ์ของเจ้าของแหล่งข้อมูล ห้ามเปลี่ยนข้อความเป็น “permitted” โดยไม่มีหลักฐาน

แหล่งอ้างอิง: https://www.fragrantica.com/terms-of-service.phtml

### 2. แก้คำอ้าง “one source”

พบ Supplemental Notes Source 36 รายการในชุด Fragrantica ใหญ่ และ 11 รายการในชุด 209 โค้ดใช้ Fragrance Notes (All) จาก workbook ที่รวมข้อมูลแล้วโดยไม่ได้กรองรายการเสริมออก

ควรเขียนว่าใช้ Fragrantica เป็นแหล่งหลัก พร้อม Parfumo supplement ตาม provenance ระดับ field และระบุ 11/209 ให้ชัด หรือย้อนกลับไปใช้ notes snapshot ที่ไม่ได้เสริมแล้วรันใหม่ การมีสองแหล่งไม่ได้แปลว่า triangulation โดยอัตโนมัติ ต้องตรวจความสอดคล้องและผลต่อข้อสรุป

เติมวันที่เก็บ/ช่วงเก็บจริงและ snapshot hash แทน “Before Oct 2026”; README ระบุเพียงประมาณ Jul 2026 ซึ่งยังไม่ใช่บันทึกวันที่ที่ยืนยันได้

### 3. จำกัด robustness ให้ตรงกับสิ่งที่ตรวจ

ข้อความ “Same verdict elsewhere” ใช้ได้กับข้อสรุปว่าไม่มี differentiating anchor ผ่านเกณฑ์ แต่ไม่ควรทำให้เข้าใจว่าตัวเลือก Lemon เหมือนเดิมทุกชุด

ผลบันทึกชุด 1,780 ระบุ fallback เป็น Orange Blossom; Lemon อยู่ betweenness rank 14 และ P(top10) ประมาณ 18% เทียบกับ 87% ในชุดหลัก

ข้อความที่แนะนำ:

> No note meets the differentiation rule in either corpus. Lemon is retained only as the control for the curated 209-perfume catalogue; the larger corpus changes the fallback to Orange Blossom.

สำหรับ NPMI ควรเขียนว่า bridge membership ของเดิมคงอยู่ 7/7 แต่ลำดับเปลี่ยนและมี bridge เพิ่ม 2 รายการ ไม่ใช่อ้างว่าตัวเลือก control หรือ decision rule ทั้งชุดผ่านการทดสอบ NPMI แล้ว

### 4. อธิบาย rank gap และ bootstrap ให้ถูกขอบเขต

- โค้ดเดิมจัด frequency rank ใน 89 eligible notes แต่ betweenness rank ในกราฟ 20 nodes จึงเป็นคนละ ranking universe ควรระบุให้ชัดหรือเปลี่ยนเป็นชุดเดียวแล้วรันกฎใหม่
- เมื่อตรวจใน 20 nodes เดียวกัน Peach มี frequency rank 13, betweenness rank 6, gap 7 ไม่ใช่ 10; ยังผ่าน gap >=5 แต่ไม่ผ่าน stability ตามวิธีเดิม อย่าเปลี่ยนเฉพาะเลขใน PDF โดยไม่แก้ pipeline ให้สอดคล้อง
- `rank()` ใช้อักษรตัดสินอันดับเมื่อค่าบวกหรือ frequency เท่ากัน ส่วน zero betweenness ถูกแก้ให้มี bottom rank ร่วมกันแล้ว ควรระบุ tie policy
- bootstrap เดิมสุ่ม brand blocks จนจำนวนแถวถึง N แล้วตัดแถวเกินทิ้ง จึงตัด cluster สุดท้ายบางส่วนได้ เป็นวิธีดัดแปลงที่ควรอธิบายหรือทดสอบเทียบกับการสุ่มทั้ง cluster โดยไม่ตัด ก่อนถือเปอร์เซ็นต์เป็นข้อสรุปแน่นอน
- ข้อความ frozen 4 Oct มาจาก README/docstring; ไม่พบหลักฐาน timestamp ภายนอก เช่น commit history ที่ยืนยันวัน freeze ใน zip จึงควรใช้ “rule calibrated on exploratory data” จนกว่าจะมีหลักฐาน

### 5. เพิ่มตารางผลขนาดเล็กลงหน้า PDF

Checklist ของ Assignment ถามว่าทุกตัวเลขใน finding ปรากฏในรูปหรือตารางหรือไม่ ปัจจุบัน 87%, 24%, rank และ correlation อยู่ในเนื้อความ แต่กราฟไม่มีค่าตัวเลขเหล่านี้

ตารางที่ควรมี (ระบุว่า frequency rank ตามวิธีเดิมอยู่ใน 89 eligible notes):

| Note | Frequency rank | Betweenness rank | Gap | Bootstrap top-10 |
|---|---:|---:|---:|---:|
| Lemon | 1 | 1 | 0 | 87% |
| Peach | 16 | 6 | 10 | 24% |

ย้ายคำอธิบายเทคนิคยาวไป notebook เพื่อเว้นพื้นที่ โดยรักษาฟอนต์ >=10 pt และ A4 1 หน้า

### 6. ทำ action ให้ใส่ปฏิทินและตัดสินได้

แทน “before testers” ด้วยวันจริง พร้อม owner และกำหนดล่วงหน้าว่า “beats Lemon” หมายถึงอะไร เช่น blind paired preference ที่ควบคุม base/concentration/order หรือ acceptance score ตามเกณฑ์ที่กำหนดก่อนเห็นผล ให้ระบุเป็นแผนทดสอบ ไม่ใช่ผลที่เกิดแล้ว

“Lemon alone” ควรชัดว่าเป็นสูตรฐานเดียวกันที่ใช้ Lemon เป็น control anchor ส่วนอีกสูตรเพิ่ม Peach ไม่ใช่การเปรียบเทียบสูตรที่ต่างกันทุกอย่าง

เพิ่ม limitation ว่า co-occurrence เป็น declared notes ที่ปรากฏร่วมกันใน catalogue ไม่ใช่หลักฐานความชอบผู้ซื้อหรือประสิทธิภาพสูตร

### 7. เพิ่ม URL และความพร้อมของ repo

พบ notebook ต้นฉบับจริงใน zip ไม่จำเป็นต้องใช้ audit notebook ที่เตรียมก่อนพบต้นฉบับเป็นหลักฐานแทน

repo มี code, saved outputs, manifest และ report source แต่ยังขาด requirements และคำสั่ง Windows ที่ใช้ได้ง่าย; ใส่ไฟล์เสริมในชุด Reviewed ให้แล้ว โดยไม่ได้แก้อัลกอริทึมหรือผลเดิม

ไฟล์ raw workbook ยังอยู่นอก repo ตามต้นฉบับ การเปิด repo อ่าน output ได้ไม่เท่ากับ rerun ได้โดยไม่จัดหาข้อมูลที่มีสิทธิ์

URL ออนไลน์ยังไม่ถูกสร้าง: การเปิด GitHub ถูกปฏิเสธด้วยข้อความว่าผู้ใช้ไม่อนุญาตการเข้าถึงเบราว์เซอร์ ต้องอนุญาตช่องทาง GitHub ที่จะใช้ก่อน แล้วจึงอัปโหลดชุดที่เลือกและตรวจลิงก์จริง ไม่ควรกรอก URL ที่คาดเดาลง PDF


หมายเหตุการเผยแพร่: บันทึกข้างต้นเป็นผลตรวจและสถานะก่อนอัปโหลด ต่อมาผู้ใช้สร้าง repo Pornphrom/MADT7202_midterm และอนุญาตให้อัปโหลดชุดนี้ ข้อจำกัดเรื่องการสร้าง URL ในบันทึกเดิมจึงเป็นประวัติการทำงาน ไม่ใช่สถานะปัจจุบัน
